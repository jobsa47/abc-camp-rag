"""KLUE-BERT 임베딩과 ChromaDB를 사용한 도서 벡터 검색 모듈."""

import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

MODEL_NAME = "snunlp/KR-FinBert-SC"
COLLECTION_NAME = "yes24_books"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "chroma_db")

_embedding_fn: embedding_functions.SentenceTransformerEmbeddingFunction | None = None
_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None


def get_embedding_function() -> embedding_functions.SentenceTransformerEmbeddingFunction:
    """KLUE-BERT 기반 임베딩 함수를 반환한다. 캐싱된 인스턴스를 재사용한다."""
    global _embedding_fn
    if _embedding_fn is None:
        _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    return _embedding_fn


def get_or_create_collection(client: chromadb.ClientAPI, ef: embedding_functions.SentenceTransformerEmbeddingFunction) -> chromadb.Collection:
    """ChromaDB 컬렉션을 가져오거나 생성한다."""
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)


def build_documents(df: pd.DataFrame, has_intro: bool) -> tuple[list[str], list[dict], list[str]]:
    """DataFrame을 ChromaDB에 삽입할 문서/메타데이터/ID 목록으로 변환한다.

    Returns:
        (documents, metadatas, ids) 튜플.
    """
    documents = []
    metadatas = []
    ids = []

    for _, row in df.iterrows():
        rank = int(row["순위"])
        title = str(row["도서명"])
        author = str(row["저자"])
        publisher = str(row["출판사"])
        price = int(row["판매가(원)"]) if pd.notna(row["판매가(원)"]) else 0
        rating = float(row["평점"]) if pd.notna(row["평점"]) else 0.0
        reviews = int(row["리뷰수"]) if pd.notna(row["리뷰수"]) else 0
        url = str(row["상세링크"])
        pub_date = str(row["출판일"])

        intro = ""
        if has_intro and "책소개" in row.index and pd.notna(row.get("책소개")):
            intro = str(row["책소개"])[:500]

        doc_text = f"제목: {title} | 저자: {author} | 출판사: {publisher} | 가격: {price}원 | 평점: {rating} | 리뷰: {reviews}건 | 출판일: {pub_date}"
        if intro.strip():
            doc_text += f" | 소개: {intro}"

        documents.append(doc_text)
        metadatas.append({
            "rank": rank,
            "title": title,
            "author": author,
            "publisher": publisher,
            "price": price,
            "rating": rating,
            "reviews": reviews,
            "url": url,
            "pub_date": pub_date,
        })
        ids.append(f"book_{rank}")

    return documents, metadatas, ids


def init_vector_db(df: pd.DataFrame, has_intro: bool) -> chromadb.Collection:
    """ChromaDB를 초기화하고 도서 데이터를 인덱싱한다.

    기존 데이터가 있으면 스킵하고, 없으면 새로 생성한다.
    클라이언트, 임베딩 함수, 컬렉션은 캐싱되어 반복 로딩을 방지한다.

    Returns:
        인덱싱된 ChromaDB Collection.
    """
    global _client, _collection

    if _collection is not None:
        return _collection

    if _client is None:
        _client = chromadb.PersistentClient(path=DB_PATH)

    ef = get_embedding_function()
    _collection = get_or_create_collection(_client, ef)

    if _collection.count() > 0:
        return _collection

    documents, metadatas, ids = build_documents(df, has_intro)

    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        _collection.add(documents=batch_docs, metadatas=batch_meta, ids=batch_ids)

    return _collection


def search_similar(collection: chromadb.Collection, query: str, n_results: int = 8) -> dict:
    """쿼리와 유사한 도서를 벡터 검색으로 찾는다.

    Args:
        collection: ChromaDB 컬렉션.
        query: 검색 쿼리 문자열.
        n_results: 반환할 결과 수.

    Returns:
        ChromaDB 쿼리 결과 딕셔너리 (documents, metadatas, distances 포함).
    """
    if collection.count() == 0:
        return {"documents": [], "metadatas": [], "distances": []}

    results = collection.query(query_texts=[query], n_results=min(n_results, collection.count()))
    return results

"""YES24 IT 베스트셀러 도서 상세 설명(책소개) 데이터 수집 및 병합 모듈.

이 모듈은 기존 수집된 CSV 데이터의 상세링크로 접속하여
책소개(상세설명) 텍스트를 크롤링하고 이를 컬럼으로 병합하여 저장합니다.
"""

import os
import re
import time
import random
import logging
import html
from typing import Generator, Dict, Any
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 실제 브라우저인 것처럼 헤더 설정
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.yes24.com/",
    "Connection": "keep-alive"
}


def clean_html(raw_html: str) -> str:
    """HTML 태그 및 특수 문자를 정제하여 일반 텍스트로 변환한다.

    Args:
        raw_html: HTML 형식이 포함된 원본 문자열.

    Returns:
        HTML 태그와 특수 문자가 제거 및 정제된 깨끗한 텍스트 문자열.
    """
    if not raw_html:
        return ""
    # <br> 이나 <br/> 태그는 줄바꿈(\n)으로 변환
    text = re.sub(r"<br\s*/?>", "\n", raw_html)
    # 나머지 모든 HTML 태그 제거
    text = re.sub(r"<[^>]+>", "", text)
    # HTML 이스케이프 해제 (&amp; -> &, &lt; -> < 등)
    text = html.unescape(text)
    # 연속된 여러 공백과 개행 정리
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def fetch_book_intro(url: str) -> str:
    """상세링크 URL에서 책소개 본문 텍스트를 크롤링하여 반환한다.

    Args:
        url: YES24 도서 상세페이지 URL.

    Returns:
        추출된 책소개 텍스트. 실패하거나 없을 시 빈 문자열을 반환한다.
    """
    if not url or not url.startswith("http"):
        return ""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            logging.warning("상세페이지 요청 실패: URL=%s, Status=%d", url, response.status_code)
            return ""
        # 인코딩 강제
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 1. textarea.txtContentText 클래스가 있는 엘리먼트 검색 (동적 텍스트용 원천 데이터)
        textarea = soup.select_one("#infoset_introduce textarea.txtContentText")
        if textarea:
            return clean_html(textarea.text)
        
        # 2. infoset_introduce 영역 전체를 가져와 '책소개' 타이틀 제거
        intro_div = soup.select_one("#infoset_introduce")
        if intro_div:
            # 내부 텍스트 추출 후 정제
            text = intro_div.get_text()
            # 첫 부분에 제목인 '책소개' 단어가 들어가므로 이를 제거
            text = re.sub(r"^\s*책소개\s*", "", text, flags=re.IGNORECASE)
            return clean_html(text)
            
        return ""
    except Exception as e:
        logging.error("도서 소개 수집 중 예외 발생: URL=%s, Error=%s", url, e)
        return ""


def update_bestseller_descriptions(
    input_csv: str,
    output_csv: str
) -> Generator[Dict[str, Any], None, None]:
    """기존 베스트셀러 CSV 파일에 책소개 상세 데이터를 병합하여 새로운 CSV로 저장한다.

    각 행별로 진행 상황(전체 수량, 현재 인덱스, 상태 등)을 generator 형식으로 반환하여
    외부 프론트엔드나 CLI에서 진행률을 동적으로 추적할 수 있게 한다.

    Args:
        input_csv: 원본 CSV 파일 경로.
        output_csv: 책소개가 병합된 최종 CSV 파일 경로.

    Yields:
        현재 도서의 인덱스, 도서명, 성공 여부 등을 포함하는 딕셔너리.
    """
    if not os.path.exists(input_csv):
        logging.error("입력 파일이 없습니다: %s", input_csv)
        return
        
    df = pd.read_csv(input_csv)
    
    # '책소개' 컬럼 생성
    if "책소개" not in df.columns:
        df["책소개"] = ""
        
    total_books = len(df)
    
    for idx, row in df.iterrows():
        title = row["도서명"]
        url = row["상세링크"]
        
        # 이미 책소개 데이터가 수집되어 채워진 행은 수집 건너뜀
        if pd.notna(row["책소개"]) and str(row["책소개"]).strip() != "":
            yield {
                "total": total_books,
                "current": idx + 1,
                "title": title,
                "status": "skipped"
            }
            continue
            
        # 책소개 크롤링
        intro = fetch_book_intro(url)
        df.at[idx, "책소개"] = intro
        
        # 크롤링한 한 건 단위로 즉시 CSV 저장 (비정상 종료 대비)
        df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        
        yield {
            "total": total_books,
            "current": idx + 1,
            "title": title,
            "status": "success" if intro else "failed"
        }
        
        # 봇 감지 우회를 위한 임의 지연 (0.3 ~ 0.8초)
        time.sleep(random.uniform(0.3, 0.8))

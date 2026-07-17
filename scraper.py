"""YES24 IT/모바일 베스트셀러 도서 목록을 수집하여 CSV 파일로 저장하는 스크래퍼 모듈.

이 모듈은 YES24 베스트셀러 카테고리(IT 모바일 종합)의 전체 페이지를 순회하며
순위, 도서명, 링크, 저자, 출판사, 출판일, 가격, 평점, 리뷰 수를 추출하고,
이를 pandas를 사용하여 CSV 형식의 파일로 내보냅니다.
봇 차단을 방지하기 위해 실제 브라우저 헤더를 사용하고 요청 간 임의의 지연 시간을 둡니다.
"""

import time
import random
import logging
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 로그 설정 (스크래핑 진행 상황 파악을 위해 추가)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_page_html(url: str, headers: Dict[str, str], timeout: int = 10) -> Optional[str]:
    """대상 URL에 HTTP GET 요청을 보내고 HTML 응답 본문을 반환한다.

    Args:
        url: 요청을 보낼 YES24 웹페이지 URL.
        headers: 실제 브라우저 요청처럼 모방하기 위한 HTTP 헤더 사전.
        timeout: 요청 타임아웃 제한 시간 (초 단위).

    Returns:
        성공 시 HTML 텍스트 문자열, 네트워크 오류 또는 에러 발생 시 None.
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        # YES24 페이지 인코딩이 정상적으로 처리되도록 보장
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error("페이지 요청 중 오류 발생: URL=%s, Error=%s", url, e)
        return None


def parse_book_item(item: BeautifulSoup) -> Dict[str, str]:
    """도서 단위 BeautifulSoup 객체에서 개별 도서 정보를 추출하여 딕셔너리로 반환한다.

    Args:
        item: 하나의 도서 영역을 나타내는 BeautifulSoup 객체 (class="itemUnit").

    Returns:
        도서의 세부 정보(순위, 도서명, 상세 링크, 저자, 출판사, 출판일, 판매가, 평점, 리뷰 수)를 담은 딕셔너리.
    """
    # 1. 순위
    rank_elem = item.select_one(".ico.rank")
    rank = rank_elem.text.strip() if rank_elem else ""

    # 2. 도서명 및 상세링크
    title_elem = item.select_one(".gd_name")
    title = title_elem.text.strip() if title_elem else ""
    
    link = ""
    if title_elem and title_elem.get("href"):
        href = title_elem.get("href")
        # 절대 경로로 변환
        link = f"https://www.yes24.com{href}" if href.startswith("/") else href

    # 3. 저자
    # 여러 명의 저자가 있을 수 있으므로 모든 저자 링크 텍스트를 수집하여 결합
    auth_elem = item.select_one(".info_auth")
    if auth_elem:
        auth_links = auth_elem.select("a")
        if auth_links:
            author = ", ".join([a.text.strip() for a in auth_links])
        else:
            # <a> 태그가 없는 경우 텍스트에서 불필요한 공백을 제거하여 정제
            author = auth_elem.text.replace("저", "").strip()
    else:
        author = ""

    # 4. 출판사
    pub_elem = item.select_one(".info_pub a")
    publisher = pub_elem.text.strip() if pub_elem else ""

    # 5. 출판일
    date_elem = item.select_one(".info_date")
    publish_date = date_elem.text.strip() if date_elem else ""

    # 6. 가격
    price_elem = item.select_one(".info_price em.yes_b")
    price = price_elem.text.strip().replace(",", "") if price_elem else ""

    # 7. 평점
    rating_elem = item.select_one(".info_rating .rating_grade em.yes_b")
    rating = rating_elem.text.strip() if rating_elem else ""

    # 8. 리뷰 수
    review_elem = item.select_one(".info_rating .rating_rvCount em.txC_blue")
    review_count = review_elem.text.strip() if review_elem else "0"

    return {
        "순위": rank,
        "도서명": title,
        "상세링크": link,
        "저자": author,
        "출판사": publisher,
        "출판일": publish_date,
        "판매가(원)": price,
        "평점": rating,
        "리뷰수": review_count
    }


def scrape_yes24_bestsellers() -> List[Dict[str, str]]:
    """YES24 IT/모바일 종합 베스트셀러 카테고리의 모든 페이지를 순회하며 도서 목록을 수집한다.

    Returns:
        수집된 모든 도서 정보 딕셔너리의 리스트.
    """
    category_number = "001001003"  # IT 모바일 종합 카테고리 번호
    page_size = 24
    base_url = "https://www.yes24.com/product/category/bestseller"
    
    # 실제 브라우저 요청으로 보이도록 상세 헤더 구성
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.yes24.com/",
        "Connection": "keep-alive"
    }

    all_books: List[Dict[str, str]] = []
    page = 1

    while True:
        url = f"{base_url}?categoryNumber={category_number}&pageNumber={page}&pageSize={page_size}"
        logging.info("%d 페이지 수집 중... URL: %s", page, url)
        
        html = fetch_page_html(url, headers)
        if not html:
            logging.warning("%d 페이지 요청에 실패하여 수집을 중단합니다.", page)
            break

        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".itemUnit")
        
        # 더 이상 수집할 아이템이 없으면 루프를 종료한다.
        if not items:
            logging.info("더 이상 수집할 도서 데이터가 없습니다. 수집을 완료합니다. (총 수집 페이지: %d)", page - 1)
            break

        for item in items:
            book_info = parse_book_item(item)
            # 수집된 도서 정보 저장
            all_books.append(book_info)

        logging.info("%d 페이지 완료: %d개 도서 수집됨", page, len(items))
        
        # 페이지 간 예의 바른 크롤러 작동을 위한 0.5초 ~ 1.5초 임의 딜레이
        time.sleep(random.uniform(0.5, 1.5))
        page += 1

    return all_books


def main() -> None:
    """메인 실행 함수. 베스트셀러를 수집하고 CSV 파일로 저장한다."""
    logging.info("YES24 IT/모바일 베스트셀러 스크래핑을 시작합니다.")
    books_data = scrape_yes24_bestsellers()
    
    if not books_data:
        logging.error("수집된 데이터가 없어 CSV 파일을 생성하지 못했습니다.")
        return

    # pandas DataFrame을 생성하여 데이터를 정돈
    df = pd.DataFrame(books_data)
    
    # 순위 기준으로 정렬 보장 (간혹 순위가 누락되거나 문자열 형태일 수 있으므로 numeric 변환 후 정렬)
    df["순위_num"] = pd.to_numeric(df["순위"], errors="coerce")
    df = df.sort_values(by="순위_num").drop(columns=["순위_num"])
    
    # CSV 저장 (Excel 한글 깨짐 방지를 위해 utf-8-sig 인코딩 적용)
    output_filename = "yes24_it_bestseller.csv"
    df.to_csv(output_filename, index=False, encoding="utf-8-sig")
    logging.info("수집이 완료되었습니다. 저장 파일: %s (총 %d개 도서)", output_filename, len(df))


if __name__ == "__main__":
    main()

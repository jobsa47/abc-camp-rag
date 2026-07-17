# ABC-RAG: YES24 IT 베스트셀러 데이터 분석 대시보드

YES24 IT/모바일 베스트셀러 1,000권을 스크래핑하여 탐색적 데이터 분석(EDA), 벡터 검색, LLM 기반 도서 추천 챗봇을 제공하는 종합 분석 시스템이다.

## 주요 기능

### 1. 데이터 수집 (Scraper)
- YES24 IT/모바일 종합 베스트셀러 전체 페이지를 순회하여 1,000권 데이터를 수집한다
- 수집 항목: 순위, 도서명, 저자, 출판사, 출판일, 판매가, 평점, 리뷰수, 상세링크
- 봇 차단 방지를 위한 랜덤 딜레이 적용
- 도서 상세 페이지에서 책소개 텍스트를 추가로 수집하여 `_with_intro.csv`에 병합한다

### 2. 탐색적 데이터 분석 (EDA) 대시보드
- **Streamlit 기반 웹 대시보드** (`src/app.py`)
- 핵심 지표 카드 (총 도서 수, 평균 평점, 가격, 리뷰수)
- 출판사/저자 Top 10 차트
- 가격 분포 및 평점 분포 히스토그램
- 연도별/월별 출판 추이
- 평점 vs 리뷰수 산점도, 상관관계 히트맵
- 도서 제목 워드클라우드 및 키워드 빈도 분석

### 3. 도서 검색
- 키워드 기반 제목/책소개 검색
- 출판사, 가격 범위, 최소 평점 필터
- 정렬 기준 선택 (순위, 평점, 리뷰수, 가격)
- 도서 상세 정보 표시 및 YES24 링크 제공

### 4. 벡터 검색 RAG 챗봇
- **KLUE-BERT 기반 임베딩** (`snunlp/KR-FinBert-SC`) + **ChromaDB** 벡터 저장소
- **Groq API** (Llama 3.3 70B 등)를 활용한 LLM 추천 챗봇
- 함수 호출(Function Calling) 지원: 가격 통계, 판매 순위 조회, 가격 분위수 분석
- 벡터 유사도 검색으로 관련 도서를 찾아 LLM 컨텍스트로 전달 (RAG 패턴)
- 벡터 DB 미구축 시 키워드 검색으로 자동 폴백

### 5. 엑셀 대시보드
- `src/create_excel_dashboard.py`로 5개 시트를 포함한 엑셀 대시보드 생성
  - 대시보드 (핵심 지표 + 출판사/저자 차트)
  - 가격·평점 분석
  - 출판 추이
  - 키워드 분석
  - 원본 데이터

### 6. PPT 발표 자료
- `create_pptx.js`로 15장짜리 Nordic Modern 테마 발표 자료 자동 생성
- 차트, 메트릭 카드, 2x2 매트릭스 등 시각화 포함
- 각 슬라이드에 발표 노트(스クリ프트) 내장

## 프로젝트 구조

```
ABC-RAG/
├── scraper.py                  # YES24 베스트셀러 스크래퍼
├── analyze_data.py             # 데이터 통계 분석 (JSON 출력)
├── requirements.txt            # Python 의존성
├── package.json                # Node.js 의존성 (pptxgenjs)
├── create_pptx.js              # PPTX 발표 자료 생성 스크립트
├── data/
│   ├── yes24_it_bestseller.csv           # 원본 수집 데이터
│   ├── yes24_it_bestseller_with_intro.csv # 책소개 포함 수집 데이터
│   ├── analysis.json                     # 분석 결과 JSON
│   ├── yes24_it_bestseller_dashboard.xlsx # 엑셀 대시보드
│   └── chroma_db/                        # ChromaDB 벡터 저장소
├── src/
│   ├── app.py                  # Streamlit 메인 대시보드 앱
│   ├── vector_db.py            # ChromaDB + KR-FinBert 벡터 검색 모듈
│   ├── update_data.py          # 책소개 수집 및 CSV 병합 모듈
│   └── create_excel_dashboard.py # 엑셀 대시보드 생성 모듈
└── output/
    └── YES24_IT_Bestseller_Analysis.pptx  # 생성된 발표 자료
```

## 실행 방법

### 환경 설정

```bash
# Python 가상환경 활성화
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Python 의존성 설치
pip install -r requirements.txt

# Node.js 의존성 설치 (PPTX 생성용)
npm install
```

### 1단계: 데이터 수집

```bash
# 베스트셀러 목록 수집 (~5분)
python scraper.py

# 책소개 수집 (~8분, 상세 페이지 크롤링)
python src/update_data.py
# 또는 Streamlit 대시보드에서 사이드바 버튼으로 수집
```

### 2단계: 대시보드 실행

```bash
# Streamlit 대시보드 실행
streamlit run src/app.py
```

- 사이드바에서 Groq API 키를 입력하면 챗봇 기능을 사용할 수 있다
- 벡터 DB 구축 버튼으로 ChromaDB를 초기화할 수 있다 (최초 1회만 필요)

### 3단계: 추가 산출물 생성

```bash
# 데이터 분석 JSON 생성
python analyze_data.py

# 엑셀 대시보드 생성
python src/create_excel_dashboard.py

# PPTX 발표 자료 생성
node create_pptx.js
```

## 기술 스택

| 구분 | 기술 |
|------|------|
| 언어 | Python 3.10+, Node.js |
| 프레임워크 | Streamlit |
| 데이터 수집 | requests, BeautifulSoup4 |
| 데이터 분석 | pandas, plotly, matplotlib, wordcloud |
| 벡터 검색 | ChromaDB, sentence-transformers (KR-FinBert-SC) |
| LLM | Groq API (Llama 3.3 70B / Llama 3.1 8B / Gemma2 9B) |
| 발표 자료 | pptxgenjs (Node.js) |
| 엑셀 | openpyxl |

## 핵심 인사이트 (분석 결과 요약)

- **AI 도서가 전체의 33.9%** (339/1,000권) — IT 출판 시장의 3분의 1 이상이 AI 관련
- **가격 1.5~2.5만원대가 58%** — 2만원대 전략이 시장 적합
- **한빛미디어가 15.1%**로 출판사 1위 — AI/코딩 교재 강세
- **평점 9.7 이상이 56%** — IT 독자 만족도가 매우 높음
- **Claude·에이전트 개발 분야**가 높은 수요 + 낮은 경쟁으로 기회 영역

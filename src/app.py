"""YES24 IT/모바일 베스트셀러 탐색적 데이터 분석(EDA) 및 도서 검색 Streamlit 대시보드."""

import os
import sys
import re
from collections import Counter

import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from update_data import update_bestseller_descriptions

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YES24 IT 베스트셀러 대시보드",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 커스텀 CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .block-container { padding-top: 1.5rem; }

    /* 메트릭 카드 */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px 18px;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #818cf8;
    }
    .metric-card .label {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-card .value {
        font-size: 1.7rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 검색 결과 카드 */
    .book-card {
        background: #1e293b;
        border-left: 5px solid #818cf8;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 14px;
    }
    .book-card .title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }
    .book-card .meta {
        font-size: 0.88rem;
        color: #cbd5e1;
        margin-bottom: 10px;
        line-height: 1.7;
    }
    .book-card .intro-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #a5b4fc;
        margin-top: 8px;
    }
    .book-card .intro-text {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.65;
        white-space: pre-wrap;
        max-height: 300px;
        overflow-y: auto;
    }
    .highlight { background: #fbbf24; color: #000; padding: 0 2px; border-radius: 2px; }

    /* 챗봇 메시지 스타일 */
    .chat-msg {
        background: #1e293b;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-left: 4px solid #818cf8;
    }
    .chat-msg.user {
        border-left-color: #22d3ee;
        background: #0f172a;
    }
    .chat-msg .role {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 6px;
    }
    .chat-msg .role.bot { color: #818cf8; }
    .chat-msg .role.human { color: #22d3ee; }
    .chat-msg .content { font-size: 0.92rem; color: #e2e8f0; line-height: 1.65; }
    .chat-book-link {
        display: inline-block;
        background: #6366f1;
        color: #fff;
        padding: 5px 14px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 6px;
        margin-right: 6px;
    }
    .chat-book-link:hover { background: #818cf8; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── 유틸리티 함수 ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> tuple[pd.DataFrame, bool]:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    enriched = os.path.join(base, "data", "yes24_it_bestseller_with_intro.csv")
    raw = os.path.join(base, "data", "yes24_it_bestseller.csv")

    if os.path.exists(enriched):
        df = pd.read_csv(enriched)
        if "책소개" in df.columns and df["책소개"].notna().sum() > 0:
            return df, True

    if os.path.exists(raw):
        return pd.read_csv(raw), False

    return pd.DataFrame(), False


@st.cache_data
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in ["판매가(원)"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col].astype(str).str.replace(",", ""), errors="coerce")

    for col in ["평점"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    for col in ["리뷰수"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype(int)

    if "순위" in out.columns:
        out["순위"] = pd.to_numeric(out["순위"], errors="coerce")

    if "출판일" in out.columns:
        out["출판년도"] = out["출판일"].astype(str).str.extract(r"(\d{4})년")
        out["출판월"] = out["출판일"].astype(str).str.extract(r"(\d{2})월")
        out["출판년월"] = out["출판년도"] + "-" + out["출판월"]

    return out


def render_metric(label: str, value: str):
    st.markdown(
        f'<div class="metric-card"><div class="label">{label}</div><div class="value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def make_wordcloud(text: str) -> plt.Figure:
    wc = WordCloud(
        font_path="C:/Windows/Fonts/malgun.ttf",
        width=900,
        height=400,
        background_color="white",
        colormap="viridis",
        max_words=120,
        prefer_horizontal=0.7,
    ).generate(text)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout()
    return fig


def extract_keywords(titles: pd.Series) -> list[tuple[str, int]]:
    stopwords = {"의", "에", "를", "이", "은", "는", "가", "와", "과", "도", "로", "으로",
                 "for", "the", "and", "with", "to", "a", "an", "in", "on", "of"}
    words = []
    for t in titles.dropna():
        tokens = re.findall(r"[가-힣]{2,}|[A-Za-z]{3,}", str(t))
        words.extend(w for w in tokens if w.lower() not in stopwords)
    return Counter(words).most_common(30)


def build_book_context(df: pd.DataFrame, has_intro: bool, max_books: int = 50) -> str:
    """도서 데이터를 LLM 프롬프트용 컨텍스트 문자열로 구성한다."""
    cols = ["순위", "도서명", "저자", "출판사", "판매가(원)", "평점", "리뷰수", "상세링크"]
    if has_intro and "책소개" in df.columns:
        cols.append("책소개")

    top = df.sort_values("순위").head(max_books)
    lines = []
    for _, row in top.iterrows():
        parts = [
            f"제목: {row['도서명']}",
            f"저자: {row['저자']}",
            f"출판사: {row['출판사']}",
            f"가격: {int(row['판매가(원)']):,}원",
            f"평점: {row['평점']}" if pd.notna(row['평점']) else "",
            f"리뷰수: {int(row['리뷰수'])}건",
            f"링크: {row['상세링크']}",
        ]
        if has_intro and "책소개" in row.index and pd.notna(row.get("책소개")):
            intro_text = str(row["책소개"])[:300]
            if intro_text.strip():
                parts.append(f"소개: {intro_text}")
        lines.append(" | ".join(p for p in parts if p))
    return "\n".join(lines)


def search_books(df: pd.DataFrame, query: str, has_intro: bool, top_n: int = 10) -> pd.DataFrame:
    """키워드 기반으로 관련 도서를 검색한다."""
    q = query.strip().lower()
    if not q:
        return df.head(top_n)

    if has_intro and "책소개" in df.columns:
        mask = (
            df["도서명"].astype(str).str.lower().str.contains(q, na=False)
            | df["저자"].astype(str).str.lower().str.contains(q, na=False)
            | df["출판사"].astype(str).str.lower().str.contains(q, na=False)
            | df["책소개"].astype(str).str.lower().str.contains(q, na=False)
        )
    else:
        mask = (
            df["도서명"].astype(str).str.lower().str.contains(q, na=False)
            | df["저자"].astype(str).str.lower().str.contains(q, na=False)
            | df["출판사"].astype(str).str.lower().str.contains(q, na=False)
        )
    matched = df[mask]
    return matched.head(top_n) if not matched.empty else df.head(5)


def get_groq_response(client: OpenAI, model: str, system_prompt: str, user_message: str, book_context: str) -> str:
    """Groq API를 호출하여 챗봇 응답을 생성한다."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"[도서 데이터베이스]\n{book_context}\n\n[사용자 질문]\n{user_message}"},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# ── 메인 ──────────────────────────────────────────────────────────────────────
def main():
    st.markdown(
        "<h1 style='text-align:center;color:#818cf8;margin-bottom:0;'>📚 YES24 IT 베스트셀러 대시보드</h1>"
        "<p style='text-align:center;color:#94a3b8;font-size:1.05rem;'>IT/모바일 베스트셀러 데이터 기반 탐색적 데이터 분석 & 도서 검색</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── 데이터 로드 ──────────────────────────────────────────────────────────
    df_raw, has_intro = load_data()
    if df_raw.empty:
        st.error("`data/yes24_it_bestseller.csv` 파일을 찾을 수 없습니다.")
        return
    df = preprocess(df_raw)

    # ── 사이드바 ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.image("https://image.yes24.com/sysimage/renew/gnb/logoN4.png", width=140)
        st.markdown("### 데이터 상태")

        if has_intro:
            st.success("책소개 수집 완료")
            if st.button("책소개 재수집", use_container_width=True):
                base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                raw_csv = os.path.join(base, "data", "yes24_it_bestseller.csv")
                enriched_csv = os.path.join(base, "data", "yes24_it_bestseller_with_intro.csv")
                if os.path.exists(enriched_csv):
                    os.remove(enriched_csv)
                st.cache_data.clear()
                _run_crawler(raw_csv, enriched_csv)
        else:
            st.warning("책소개 미수집 (제목 검색만 가능)")
            if st.button("책소개 수집 시작 (~8분)", use_container_width=True):
                base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                raw_csv = os.path.join(base, "data", "yes24_it_bestseller.csv")
                enriched_csv = os.path.join(base, "data", "yes24_it_bestseller_with_intro.csv")
                _run_crawler(raw_csv, enriched_csv)

        st.divider()
        st.markdown("### 데이터 요약")
        st.markdown(
            f"- 총 도서: **{len(df):,}권**\n"
            f"- 평균 평점: **{df['평점'].mean():.2f}**\n"
            f"- 평균 가격: **{int(df['판매가(원)'].mean()):,}원**\n"
            f"- 총 리뷰: **{df['리뷰수'].sum():,}건**"
        )

        st.divider()
        st.markdown("### Groq API 설정")
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="https://console.groq.com 에서 발급받은 API 키를 입력하세요.",
        )
        groq_model = st.selectbox(
            "모델 선택",
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
            index=0,
        )

    # ── 탭 ────────────────────────────────────────────────────────────────────
    tab_eda, tab_search, tab_chat = st.tabs(["📈 탐색적 데이터 분석 (EDA)", "🔍 도서 검색", "💬 도서 추천 챗봇"])

    # ══════════════════════════════════════════════════════════════════════════
    #  탭 1: EDA
    # ══════════════════════════════════════════════════════════════════════════
    with tab_eda:
        # ── 핵심 지표 ─────────────────────────────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric("총 도서 수", f"{len(df):,}권")
        with c2:
            avg_r = df["평점"].mean()
            render_metric("평균 평점", f"{avg_r:.1f}" if pd.notna(avg_r) else "N/A")
        with c3:
            med_p = df["판매가(원)"].median()
            render_metric("중앙값 가격", f"{int(med_p):,}원")
        with c4:
            render_metric("평균 가격", f"{int(df['판매가(원)'].mean()):,}원")
        with c5:
            render_metric("총 리뷰", f"{df['리뷰수'].sum():,}건")

        st.write("")

        # ── 출판사 / 저자 Top 10 ──────────────────────────────────────────
        st.markdown("### 🏢 출판사 & 저자 영향력")
        col_l, col_r = st.columns(2)

        with col_l:
            pub = df["출판사"].value_counts().head(10).reset_index()
            pub.columns = ["출판사", "도서 수"]
            fig = px.bar(pub, x="도서 수", y="출판사", orientation="h",
                         title="상위 10개 출판사 (베스트셀러 등록 수)",
                         color="도서 수", color_continuous_scale="Viridis",
                         text="도서 수")
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420,
                              template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            auth = df["저자"].value_counts().head(10).reset_index()
            auth.columns = ["저자", "도서 수"]
            fig = px.bar(auth, x="도서 수", y="저자", orientation="h",
                         title="상위 10개 저자 (베스트셀러 등록 수)",
                         color="도서 수", color_continuous_scale="Plasma",
                         text="도서 수")
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420,
                              template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        st.write("")

        # ── 가격 & 평점 분포 ──────────────────────────────────────────────
        st.markdown("### 💰 가격 & 평점 분포")
        col_l, col_r = st.columns(2)

        with col_l:
            fig = px.histogram(df, x="판매가(원)", nbins=25,
                               title="가격 분포 (전체 도서)",
                               color_discrete_sequence=["#818cf8"], opacity=0.85)
            fig.update_layout(xaxis_title="판매가(원)", yaxis_title="도서 수",
                              height=400, template="plotly_dark",
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            df_r = df[df["평점"].notna()]
            fig = px.histogram(df_r, x="평점", nbins=15,
                               title="평점 분포",
                               color_discrete_sequence=["#c084fc"], marginal="box",
                               opacity=0.85)
            fig.update_layout(xaxis_title="평점", yaxis_title="도서 수",
                              height=400, template="plotly_dark",
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        st.write("")

        # ── 출판 추이 ────────────────────────────────────────────────────
        st.markdown("### 📅 출판 추이")
        col_l, col_r = st.columns(2)

        with col_l:
            trend_y = df["출판년도"].value_counts().reset_index()
            trend_y.columns = ["출판년도", "도서 수"]
            trend_y = trend_y.sort_values("출판년도")
            fig = px.bar(trend_y, x="출판년도", y="도서 수",
                         title="연도별 베스트셀러 출시 수",
                         color="도서 수", color_continuous_scale="Teal",
                         text="도서 수")
            fig.update_layout(height=400, template="plotly_dark",
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            recent = df[df["출판년도"].astype(str) >= "2023"]
            if not recent.empty:
                trend_m = recent.groupby("출판년월").size().reset_index(name="도서 수")
                trend_m = trend_m.sort_values("출판년월")
                fig = px.line(trend_m, x="출판년월", y="도서 수",
                              title="월별 추이 (2023년~)", markers=True,
                              color_discrete_sequence=["#22d3ee"])
                fig.update_layout(height=400, template="plotly_dark",
                                  xaxis_tickangle=-45,
                                  margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("2023년 이후 데이터가 없습니다.")

        st.write("")

        # ── 평점 vs 리뷰 산점도 & 상관 히트맵 ────────────────────────────
        st.markdown("### 🔗 변수 간 관계")
        col_l, col_r = st.columns(2)

        with col_l:
            fig = px.scatter(df, x="평점", y="리뷰수",
                             color="판매가(원)", size="리뷰수",
                             hover_data=["도서명", "저자"],
                             title="평점 vs 리뷰 수 (색: 판매가, 크기: 리뷰수)",
                             color_continuous_scale="RdBu")
            fig.update_layout(height=420, template="plotly_dark",
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            num_cols = ["판매가(원)", "평점", "리뷰수"]
            corr = df[num_cols].corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr.values, x=corr.columns, y=corr.columns,
                colorscale="RdBu_r", zmin=-1, zmax=1, text=corr.values.round(2),
                texttemplate="%{text}", textfont={"size": 14},
            ))
            fig.update_layout(title="수치 변수 상관관계 히트맵", height=420,
                              template="plotly_dark",
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        st.write("")

        # ── 도서 제목 워드클라우드 & 키워드 빈도 ──────────────────────────
        st.markdown("### ☁️ 도서 제목 워드클라우드 & 주요 키워드")
        col_l, col_r = st.columns([2, 1])

        with col_l:
            all_titles = " ".join(df["도서명"].dropna().astype(str))
            fig_wc = make_wordcloud(all_titles)
            st.pyplot(fig_wc)

        with col_r:
            kw = extract_keywords(df["도서명"])
            kw_df = pd.DataFrame(kw, columns=["키워드", "빈도"])
            fig = px.bar(kw_df.head(15), x="빈도", y="키워드", orientation="h",
                         title="상위 15개 키워드",
                         color="빈도", color_continuous_scale="Magma",
                         text="빈도")
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420,
                              template="plotly_dark",
                              margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        st.write("")

        # ── 요약 통계 테이블 ──────────────────────────────────────────────
        st.markdown("### 📋 기술 통계 요약")
        desc = df[["판매가(원)", "평점", "리뷰수"]].describe().round(2)
        st.dataframe(desc, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  탭 2: 검색
    # ══════════════════════════════════════════════════════════════════════════
    with tab_search:
        st.markdown("### 🔍 도서 검색")

        # 필터 컨트롤
        q_col, pub_col = st.columns([3, 2])
        with q_col:
            query = st.text_input("키워드 입력 (제목 및 책소개 검색)", "",
                                  placeholder="예: 파이썬, AI, 클로드, 초보, 코딩 ...")
        with pub_col:
            all_pubs = sorted(df["출판사"].dropna().unique().tolist())
            sel_pubs = st.multiselect("출판사 필터", all_pubs)

        p_col, r_col, s_col = st.columns(3)
        with p_col:
            min_p, max_p = int(df["판매가(원)"].min()), int(df["판매가(원)"].max())
            price_range = st.slider("가격 범위 (원)", min_p, max_p, (min_p, max_p))
        with r_col:
            min_rating = st.slider("최소 평점", 0.0, 10.0, 0.0, step=0.1)
        with s_col:
            sort_by = st.selectbox("정렬 기준", ["순위 (오름차순)", "평점 (내림차순)", "리뷰수 (내림차순)", "가격 (오름차순)", "가격 (내림차순)"])

        # 필터링
        result = df.copy()

        if query.strip():
            q = query.strip().lower()
            if has_intro and "책소개" in result.columns:
                mask = (
                    result["도서명"].astype(str).str.lower().str.contains(q, na=False)
                    | result["책소개"].astype(str).str.lower().str.contains(q, na=False)
                )
            else:
                mask = result["도서명"].astype(str).str.lower().str.contains(q, na=False)
            result = result[mask]

        if sel_pubs:
            result = result[result["출판사"].isin(sel_pubs)]

        result = result[
            (result["판매가(원)"] >= price_range[0]) & (result["판매가(원)"] <= price_range[1])
        ]
        result = result[result["평점"] >= min_rating]

        # 정렬
        sort_map = {
            "순위 (오름차순)": ("순위", True),
            "평점 (내림차순)": ("평점", False),
            "리뷰수 (내림차순)": ("리뷰수", False),
            "가격 (오름차순)": ("판매가(원)", True),
            "가격 (내림차순)": ("판매가(원)", False),
        }
        col_name, asc = sort_map[sort_by]
        result = result.sort_values(col_name, ascending=asc, na_position="last")

        # 결과 출력
        st.markdown(f"#### 검색 결과: 총 **{len(result)}**건")

        if result.empty:
            st.info("검색 조건에 맞는 도서가 없습니다. 필터를 조정해 보세요.")
        else:
            display_cols = ["순위", "도서명", "저자", "출판사", "판매가(원)", "평점", "리뷰수"]
            st.dataframe(result[display_cols].reset_index(drop=True), use_container_width=True, height=300)

            st.markdown("---")
            st.markdown("#### 📖 도서 상세 보기")
            selected = st.selectbox("도서 선택", result["도서명"].tolist(), key="detail_select")

            if selected:
                book = result[result["도서명"] == selected].iloc[0]
                rating_val = book["평점"]
                stars = "⭐" * int(rating_val // 2) if pd.notna(rating_val) else "평점 없음"

                intro = ""
                if has_intro and "책소개" in book.index and pd.notna(book["책소개"]) and str(book["책소개"]).strip():
                    intro = str(book["책소개"])
                else:
                    intro = "책소개 데이터가 없습니다. 사이드바에서 '책소개 수집 시작'을 눌러 업데이트하세요."

                # 키워드 하이라이트
                if query.strip():
                    pattern = re.compile(re.escape(query.strip()), re.IGNORECASE)
                    intro = pattern.sub(lambda m: f'<span class="highlight">{m.group()}</span>', intro)
                    title_html = pattern.sub(lambda m: f'<span class="highlight">{m.group()}</span>', str(book["도서명"]))
                else:
                    title_html = str(book["도서명"])

                st.markdown(
                    f"""
                    <div class="book-card">
                        <div class="title">[{int(book['순위'])}위] {title_html}</div>
                        <div class="meta">
                            <b>저자:</b> {book['저자']} &nbsp;|&nbsp;
                            <b>출판사:</b> {book['출판사']} &nbsp;|&nbsp;
                            <b>출판일:</b> {book['출판일']}<br>
                            <b>판매가:</b> {int(book['판매가(원)']):,}원 &nbsp;|&nbsp;
                            <b>평점:</b> {rating_val:.1f} ({stars}) &nbsp;|&nbsp;
                            <b>리뷰:</b> {int(book['리뷰수']):,}건
                        </div>
                        <div class="intro-label">📖 책소개</div>
                        <div class="intro-text">{intro}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.link_button("🌐 YES24 상세 페이지 바로가기", book["상세링크"])

    # ══════════════════════════════════════════════════════════════════════════
    #  탭 3: 챗봇
    # ══════════════════════════════════════════════════════════════════════════
    with tab_chat:
        st.markdown("### 💬 도서 추천 챗봇")
        st.caption("GROQ API를 활용하여 베스트셀러 데이터 기반으로 도서를 추천합니다. 사이드바에서 API 키를 입력하세요.")

        if not groq_api_key:
            st.info("사이드바에서 **Groq API Key**를 입력해 주세요.  \nhttps://console.groq.com 에서 무료로 발급 가능합니다.")
        else:
            # 세션 초기화
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            if "chat_books" not in st.session_state:
                st.session_state.chat_books = []

            # 시스템 프롬프트
            SYSTEM_PROMPT = (
                "당신은 YES24 IT/모바일 베스트셀러 도서 추천 전문가입니다.\n"
                "아래 [도서 데이터베이스]에 있는 도서 정보를 바탕으로 사용자의 질문에 친절하게 답변하세요.\n"
                "도서를 추천할 때는 반드시 아래 형식을 지켜주세요:\n"
                "- 도서명, 저자, 출판사, 가격, 평점, 리뷰수를 포함하세요.\n"
                "- 해당 도서의 YES24 링크를 포함하세요 (링크: https://... 형식).\n"
                "추천할 만한 도서가 없으면 \"현재 데이터베이스에 해당 조건에 맞는 도서가 없습니다.\"라고 솔직하게 답변하세요.\n"
                "답변은 한국어로 작성하고, 친근하고 전문적인 톤으로 대화하세요.\n"
                "마크다운 형식을 활용하여 읽기 쉽게 작성하세요."
            )

            # 이전 대화 표시
            for msg in st.session_state.chat_history:
                role_cls = "user" if msg["role"] == "user" else ""
                role_label = "나" if msg["role"] == "user" else "봇"
                role_color = "human" if msg["role"] == "user" else "bot"
                st.markdown(
                    f'<div class="chat-msg {role_cls}">'
                    f'<div class="role {role_color}">{role_label}</div>'
                    f'<div class="content">{msg["content"]}</div></div>',
                    unsafe_allow_html=True,
                )

            # 이전 추천 도서 링크 버튼 표시
            if st.session_state.chat_books:
                st.markdown("**추천 도서 바로가기:**")
                link_cols = st.columns(min(len(st.session_state.chat_books), 4))
                for i, book in enumerate(st.session_state.chat_books[:8]):
                    with link_cols[i % len(link_cols)]:
                        st.link_button(
                            f"📖 {book['title'][:20]}...",
                            book["url"],
                            use_container_width=True,
                        )

            # 사용자 입력
            user_input = st.chat_input("어떤 종류의 IT 도서를 찾고 계신가요?")

            if user_input:
                # 사용자 메시지 표시
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.markdown(
                    f'<div class="chat-msg user">'
                    f'<div class="role human">나</div>'
                    f'<div class="content">{user_input}</div></div>',
                    unsafe_allow_html=True,
                )

                # 관련 도서 검색
                matched = search_books(df, user_input, has_intro, top_n=10)
                book_context = build_book_context(matched, has_intro, max_books=10)

                # 추천 도서 목록 업데이트
                st.session_state.chat_books = []
                for _, row in matched.iterrows():
                    st.session_state.chat_books.append({
                        "title": row["도서명"],
                        "url": row["상세링크"],
                    })

                # Groq API 호출
                with st.spinner("생각 중..."):
                    try:
                        client = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
                        bot_reply = get_groq_response(client, groq_model, SYSTEM_PROMPT, user_input, book_context)
                    except Exception as e:
                        bot_reply = f"API 호출 중 오류가 발생했습니다: {e}"

                # 봇 응답 표시
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
                st.markdown(
                    f'<div class="chat-msg">'
                    f'<div class="role bot">봇</div>'
                    f'<div class="content">{bot_reply}</div></div>',
                    unsafe_allow_html=True,
                )

                # 추천 도서 링크 버튼
                if st.session_state.chat_books:
                    st.markdown("**추천 도서 바로가기:**")
                    link_cols = st.columns(min(len(st.session_state.chat_books), 4))
                    for i, book in enumerate(st.session_state.chat_books[:8]):
                        with link_cols[i % len(link_cols)]:
                            st.link_button(
                                f"📖 {book['title'][:20]}...",
                                book["url"],
                                use_container_width=True,
                            )

            # 대화 초기화 버튼
            if st.session_state.chat_history:
                if st.button("대화 초기화", use_container_width=True):
                    st.session_state.chat_history = []
                    st.session_state.chat_books = []
                    st.rerun()


def _run_crawler(raw_path: str, enriched_path: str):
    progress = st.progress(0)
    status_text = st.empty()
    counts = {"success": 0, "skipped": 0, "failed": 0}

    for update in update_bestseller_descriptions(raw_path, enriched_path):
        total = update["total"]
        current = update["current"]
        counts[update["status"]] = counts.get(update["status"], 0) + 1
        pct = current / total
        progress.progress(pct)
        status_text.markdown(
            f"**진행:** {current}/{total} ({pct*100:.1f}%)  "
            f"✅ {counts['success']} | ⏭ {counts['skipped']} | ❌ {counts['failed']}"
        )

    st.success("책소개 수집 완료!")
    st.cache_data.clear()
    st.rerun()


if __name__ == "__main__":
    main()

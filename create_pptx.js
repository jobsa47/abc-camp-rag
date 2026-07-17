const pptxgen = require("pptxgenjs");

// ============================================================
// Nordic Modern Design System — YES24 IT Bestseller Analysis
// ============================================================

// Color palette — Nordic muted tones
const C = {
  darkBg:    "1B2838",   // deep slate navy
  lightBg:   "F4F1ED",   // warm off-white / parchment
  midBg:     "E8E3DC",   // soft taupe
  cardBg:    "FFFFFF",   // white cards
  accent:    "5B8A72",   // muted sage green
  accentDk:  "3D6B54",   // darker sage
  accentLt:  "A3C4A0",   // light sage
  warmAccent: "C4956A",  // muted terracotta
  coolAccent: "6B9BC0",  // dusty blue
  text:      "2D3436",   // near-black
  textLight: "6B7B8D",   // muted gray
  textWhite: "FFFFFF",
  divider:   "D5CEC5",   // warm gray line
  chartGreen:["5B8A72","7AAE8E","A3C4A0","C8DEC3","E2F0DB"],
  chartMulti:["5B8A72","C4956A","6B9BC0","8B7EC8","C77D87","D4A853","5B8A72"],
};

const FONT = { header: "Georgia", body: "Calibri" };
const SLIDE_W = 10, SLIDE_H = 5.625;

// ── helpers ──────────────────────────────────────────────────
const mkShadow = () => ({ type:"outer", color:"000000", blur:6, offset:2, angle:135, opacity:0.10 });
const mkCardShadow = () => ({ type:"outer", color:"000000", blur:4, offset:1, angle:135, opacity:0.08 });

// ══════════════════════════════════════════════════════════════
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "ABC-RAG";
pres.title  = "YES24 IT 베스트셀러 분석 — 신규 도서 기획 제안";

// ── SLIDE 1: TITLE ──────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  // Top thin sage line
  s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.04, fill:{color:C.accent} });
  // Title
  s.addText("YES24 IT 베스트셀러\n분석 리포트", {
    x:0.8, y:1.0, w:8.4, h:2.0,
    fontSize:40, fontFace:FONT.header, color:C.textWhite,
    bold:true, lineSpacingMultiple:1.15, align:"left", margin:0
  });
  // Subtitle
  s.addText("신규 도서 기획을 위한 데이터 기반 인사이트", {
    x:0.8, y:3.0, w:8.4, h:0.5,
    fontSize:16, fontFace:FONT.body, color:C.accentLt, align:"left", margin:0
  });
  // Bottom info bar
  s.addShape(pres.shapes.RECTANGLE, { x:0, y:4.85, w:10, h:0.775, fill:{color:C.accentDk} });
  s.addText("2026.07  |  YES24 IT 베스트셀러 1,000권 분석  |  ABC-RAG", {
    x:0.8, y:4.9, w:8.4, h:0.55,
    fontSize:11, fontFace:FONT.body, color:C.textWhite, align:"left", valign:"middle", margin:0
  });
  s.addNotes("안녕하세요. 오늘 발표에서는 YES24 IT 분야 베스트셀러 1,000권의 데이터를 기반으로, 신규 도서 기획에 필요한 인사이트를 공유하겠습니다. 데이터 분석을 통해 시장 트렌드, 가격 전략, 출판사 경쟁 구도, 그리고 AI 관련 도서의 폭발적 성장까지 확인해 보겠습니다.");
}

// ── SLIDE 2: AGENDA ─────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("목차", {
    x:0.8, y:0.4, w:8.4, h:0.7,
    fontSize:32, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });
  const items = [
    ["01", "데이터 개요", "분석 대상과 범위"],
    ["02", "시장 규모와 가격 분석", "가격대 분포 및 가격 전략"],
    ["03", "출판사 경쟁 구도", "시장 점유율과 포지셔닝"],
    ["04", "AI 도서 트렌드", "AI/LLM 도서의 성장과 기회"],
    ["05", "교육·에듀테크 도서", "교사 대상 시장 분석"],
    ["06", "고객 리뷰 인사이트", "리뷰와 평점으로 본 수요"],
    ["07", "신규 기획 제안", "데이터 기반 도서 기획 방향"],
  ];
  items.forEach((it, i) => {
    const y = 1.35 + i * 0.56;
    // Number badge
    s.addShape(pres.shapes.OVAL, {
      x:0.8, y:y, w:0.38, h:0.38,
      fill:{color: i===6 ? C.warmAccent : C.accent}
    });
    s.addText(it[0], {
      x:0.8, y:y, w:0.38, h:0.38,
      fontSize:10, fontFace:FONT.body, color:C.textWhite,
      bold:true, align:"center", valign:"middle", margin:0
    });
    // Title
    s.addText(it[1], {
      x:1.35, y:y-0.02, w:3.5, h:0.24,
      fontSize:14, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
    });
    // Desc
    s.addText(it[2], {
      x:1.35, y:y+0.20, w:5, h:0.20,
      fontSize:10, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
    });
  });
  // Right decorative block
  s.addShape(pres.shapes.RECTANGLE, {
    x:7.0, y:0.8, w:2.5, h:4.0,
    fill:{color:C.accent}, shadow:mkShadow()
  });
  s.addText("DATA\nDRIVEN\nPLANNING", {
    x:7.0, y:1.3, w:2.5, h:3.0,
    fontSize:24, fontFace:FONT.header, color:C.textWhite,
    bold:true, align:"center", valign:"middle", lineSpacingMultiple:1.2, margin:0
  });
  s.addNotes("오늘 발표의 목차를 안내해 드리겠습니다. 크게 7개 파트로 구성되어 있습니다. 첫째, 데이터 개요를 살펴보고, 둘째, 시장 규모와 가격 분석, 셋째, 출판사 경쟁 구도, 넷째, AI 도서 트렌드, 다섯째, 교육·에듀테크 도서 분석, 여섯째, 고객 리뷰 인사이트, 그리고 마지막으로 신규 기획 제안까지 데이터에 기반한 도서 기획 방향을 제시하겠습니다.");
}

// ── SLIDE 3: DATA OVERVIEW ──────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("데이터 개요", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });
  s.addText("YES24 IT 분야 베스트셀러 상위 1,000권", {
    x:0.8, y:0.95, w:8.4, h:0.3,
    fontSize:12, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
  });
  // Stat cards — 4 across
  const stats = [
    ["1,000", "분석 도서 수", C.accent],
    ["22,959원", "평균 판매가", C.coolAccent],
    ["9.60", "평균 평점", C.warmAccent],
    ["339권", "AI 관련 도서", C.accentDk],
  ];
  stats.forEach((st, i) => {
    const cx = 0.8 + i * 2.25;
    s.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:1.55, w:1.95, h:1.55,
      fill:{color:C.cardBg}, shadow:mkCardShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:1.55, w:1.95, h:0.06,
      fill:{color:st[2]}
    });
    s.addText(st[0], {
      x:cx, y:1.75, w:1.95, h:0.7,
      fontSize:28, fontFace:FONT.header, color:st[2],
      bold:true, align:"center", valign:"middle", margin:0
    });
    s.addText(st[1], {
      x:cx, y:2.45, w:1.95, h:0.45,
      fontSize:11, fontFace:FONT.body, color:C.textLight,
      align:"center", valign:"top", margin:0
    });
  });
  // Bottom description
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.8, y:3.5, w:8.4, h:1.6,
    fill:{color:C.cardBg}, shadow:mkCardShadow()
  });
  s.addText([
    {text:"데이터 소스: ", options:{bold:true}},
    {text:"YES24 IT/컴퓨터 베스트셀러 페이지에서 상위 1,000권을 스크래핑하여 확보", options:{breakLine:true}},
    {text:"수집 항목: ", options:{bold:true}},
    {text:"도서명, 저자, 출판사, 출판일, 판매가, 평점, 리뷰수", options:{breakLine:true}},
    {text:"분석 기간: ", options:{bold:true}},
    {text:"2026년 7월 기준 스냅샷 (2010년~2026년 출판 도서 포함)"},
  ], {
    x:1.1, y:3.65, w:7.8, h:1.3,
    fontSize:11, fontFace:FONT.body, color:C.text,
    lineSpacingMultiple:1.5, valign:"top", margin:0
  });
  s.addNotes("먼저 데이터 개요를 살펴보겠습니다.本次 분석 대상은 YES24 IT/컴퓨터 분야 베스트셀러 상위 1,000권입니다. 총 분석 대상 1,000권의 평균 판매가는 약 23,000원이며, 평균 평점은 9.60으로 매우 높은 수준입니다. 특히 주목할 점은 1,000권 중 339권, 즉 약 34%가 AI 관련 도서라는 점입니다. 이는 AI 열풍이 IT 출판 시장에 미치는 영향이 압도적임을 보여줍니다.");
}

// ── SLIDE 4: MARKET SIZE & PRICE ────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("시장 규모와 가격 분석", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });
  // Bar chart — price range distribution
  s.addChart(pres.charts.BAR, [{
    name: "도서 수",
    labels: ["~1.5만", "1.5~2만", "2~2.5만", "2.5~3만", "3만~"],
    values: [95, 325, 255, 181, 144]
  }], {
    x:0.5, y:1.1, w:5.0, h:3.2, barDir:"col",
    chartColors: C.chartGreen,
    showValue: true, dataLabelPosition:"outEnd", dataLabelColor: C.text,
    valGridLine:{color:"E2E8F0", size:0.5}, catGridLine:{style:"none"},
    catAxisLabelColor:C.textLight, valAxisLabelColor:C.textLight,
    showLegend:false, chartArea:{fill:{color:C.cardBg}, roundedCorners:true}
  });

  // Right stat cards
  const priceStats = [
    ["22,959원", "평균 가격"],
    ["21,600원", "중앙값"],
    ["5,625원", "최저가"],
    ["85,000원", "최고가"],
  ];
  priceStats.forEach((ps, i) => {
    const ry = 1.15 + i * 0.78;
    s.addShape(pres.shapes.RECTANGLE, {
      x:6.0, y:ry, w:3.5, h:0.65,
      fill:{color:C.cardBg}, shadow:mkCardShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:6.0, y:ry, w:0.06, h:0.65,
      fill:{color:C.accent}
    });
    s.addText(ps[0], {
      x:6.25, y:ry+0.05, w:3.0, h:0.35,
      fontSize:18, fontFace:FONT.header, color:C.accentDk, bold:true, align:"left", margin:0
    });
    s.addText(ps[1], {
      x:6.25, y:ry+0.38, w:3.0, h:0.22,
      fontSize:10, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
    });
  });

  // Key insight box
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:4.45, w:9.0, h:0.85,
    fill:{color:C.accentDk}
  });
  s.addText("핵심: 전체의 58%가 1.5~2.5만원대에 집중 → 2만원대 전략이 시장 적합", {
    x:0.8, y:4.5, w:8.4, h:0.7,
    fontSize:13, fontFace:FONT.body, color:C.textWhite, bold:true, align:"left", valign:"middle", margin:0
  });
  s.addNotes("가격 분석 결과를 보면, IT 베스트셀러 1,000권의 평균 판매가는 약 23,000원이고 중앙값은 21,600원입니다. 가격대별 분포를 보면 1.5만~2만원대가 325권으로 가장 많고, 2~2.5만원대가 255권으로 뒤를 잇습니다. 즉 전체의 약 58%가 1.5~2.5만원대에 집중되어 있습니다. 이는 신규 도서 기획 시 2만원대 가격대가 시장에서 가장 적합한 포인트임을 시사합니다. 최저가는 5,625원, 최고가는 85,000원으로 가격 스펙트럼이 넓지만, 베스트셀러는 중간 가격대에 수렴합니다.");
}

// ── SLIDE 5: PRICE STRATEGY INSIGHTS ────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("가격 전략 인사이트", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // Two-column layout
  // Left: Price tier cards
  const tiers = [
    {range:"1.5만원 이하", cnt:95, pct:"9.5%", note:"입문서·소개서 위주", color:C.accentLt},
    {range:"1.5~2.0만원", cnt:325, pct:"32.5%", note:"가장 많은 도서", color:C.accent},
    {range:"2.0~2.5만원", cnt:255, pct:"25.5%", note:"실무·활용서 중심", color:C.accentDk},
    {range:"2.5~3.0만원", cnt:181, pct:"18.1%", note:"심화·전문서적", color:C.warmAccent},
    {range:"3만원 이상", cnt:144, pct:"14.4%", note:"프리미엄·올인원", color:C.coolAccent},
  ];
  tiers.forEach((t, i) => {
    const ty = 1.15 + i * 0.82;
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.8, y:ty, w:4.5, h:0.7,
      fill:{color:C.cardBg}, shadow:mkCardShadow()
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.8, y:ty, w:0.06, h:0.7,
      fill:{color:t.color}
    });
    s.addText(t.range, {
      x:1.05, y:ty+0.05, w:2.0, h:0.28,
      fontSize:12, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
    });
    s.addText(`${t.cnt}권 (${t.pct})`, {
      x:3.1, y:ty+0.05, w:2.0, h:0.28,
      fontSize:12, fontFace:FONT.body, color:t.color, bold:true, align:"left", margin:0
    });
    s.addText(t.note, {
      x:1.05, y:ty+0.35, w:3.8, h:0.28,
      fontSize:10, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
    });
  });

  // Right: Recommendation box
  s.addShape(pres.shapes.RECTANGLE, {
    x:5.8, y:1.15, w:3.7, h:3.9,
    fill:{color:C.darkBg}
  });
  s.addText("신규 기획 가격 가이드", {
    x:6.1, y:1.3, w:3.1, h:0.45,
    fontSize:16, fontFace:FONT.header, color:C.accentLt, bold:true, align:"left", margin:0
  });
  s.addText([
    {text:"가장 성공적인 가격대", options:{breakLine:true, bold:true}},
    {text:"1.5~2.0만원: 베스트셀러의 32.5%", options:{breakLine:true}},
    {text:"", options:{breakLine:true}},
    {text:"신규 기획 권장 범위", options:{breakLine:true, bold:true}},
    {text:"1.8~2.5만원", options:{breakLine:true, bold:true, color:C.accentLt}},
    {text:"", options:{breakLine:true}},
    {text:"실무서는 2만원대 중반,", options:{breakLine:true}},
    {text:"입문서는 1.8만원대,", options:{breakLine:true}},
    {text:"프리미엄 올인원은 2.7~3만원", options:{breakLine:true}},
    {text:"포지셔닝이 효과적입니다.", options:{}},
  ], {
    x:6.1, y:1.9, w:3.1, h:3.0,
    fontSize:11, fontFace:FONT.body, color:C.textWhite,
    lineSpacingMultiple:1.3, valign:"top", margin:0
  });

  s.addNotes("가격 전략에 대해 좀 더 자세히 살펴보겠습니다. 가격대별 도서 분포를 보면, 1.5만~2만원대가 전체의 32.5%로 가장 많은 도서가 분포하고 있습니다. 그 뒤를 2~2.5만원대가 25.5%로 잇고 있습니다. 신규 도서 기획 시 이 데이터를 기반으로 가격을 설정해야 합니다. 실무서는 2만원대 중반, 입문서는 1.8만원대, 프리미엄 올인원은 2.7~3만원대로 포지셔닝하는 것이 효과적입니다.");
}

// ── SLIDE 6: PUBLISHER COMPETITION ──────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("출판사 경쟁 구도", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // Pie chart — top publishers
  s.addChart(pres.charts.DOUGHNUT, [{
    name: "시장 점유율",
    labels: ["한빛미디어","길벗","이지스퍼블리싱","커뮤니케이션북스","골든래빗","기타"],
    values: [151, 74, 55, 53, 47, 620]
  }], {
    x:0.3, y:1.0, w:4.5, h:3.5,
    showPercent: true,
    showTitle: false,
    showLegend: true, legendPos:"b", legendFontSize:9,
    chartColors: C.chartMulti,
    dataLabelColor: C.text,
  });

  // Right — Publisher cards
  const pubs = [
    {name:"한빛미디어", cnt:151, pct:"15.1%", strength:"AI·코딩 교재 강세"},
    {name:"길벗", cnt:74, pct:"7.4%", strength:"실무 IT 서적"},
    {name:"이지스퍼블리싱", cnt:55, pct:"5.5%", strength:"프로그래밍 입문"},
    {name:"커뮤니케이션북스", cnt:53, pct:"5.3%", strength:"디자인·IT 종합"},
    {name:"골든래빗", cnt:47, pct:"4.7%", strength:"AI 활용·교육"},
  ];
  pubs.forEach((p, i) => {
    const py = 1.1 + i * 0.72;
    s.addShape(pres.shapes.RECTANGLE, {
      x:5.2, y:py, w:4.3, h:0.6,
      fill:{color:C.cardBg}, shadow:mkCardShadow()
    });
    s.addText(p.name, {
      x:5.4, y:py+0.02, w:2.2, h:0.28,
      fontSize:12, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
    });
    s.addText(`${p.cnt}권 (${p.pct})`, {
      x:7.6, y:py+0.02, w:1.7, h:0.28,
      fontSize:11, fontFace:FONT.body, color:C.accentDk, bold:true, align:"right", margin:0
    });
    s.addText(p.strength, {
      x:5.4, y:py+0.30, w:3.8, h:0.24,
      fontSize:9, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
    });
  });

  s.addNotes("출판사 경쟁 구도를 살펴보면, 한빛미디어가 151권으로 15.1%의 시장 점유율을 보이며 압도적인 1위를 차지하고 있습니다. 특히 AI와 코딩 교재 분야에서 강점을 보이고 있습니다. 그 뒤를 길벗 74권, 이지스퍼블리싱 55권, 커뮤니케이션북스 53권, 골든래빗 47권이 잇고 있습니다. 주목할 점은 골든래빗이 AI 활용과 교육 분야에서 빠르게 성장하고 있다는 점입니다.");
}

// ── SLIDE 7: AI TREND OVERVIEW ──────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  // Top accent bar
  s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.04, fill:{color:C.accent} });

  s.addText("AI 도서 트렌드", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.textWhite, bold:true, align:"left", margin:0
  });
  s.addText("1,000권 중 339권 = 33.9%가 AI 관련", {
    x:0.8, y:0.95, w:8.4, h:0.3,
    fontSize:13, fontFace:FONT.body, color:C.accentLt, align:"left", margin:0
  });

  // Big stat callout
  s.addText("33.9%", {
    x:0.8, y:1.5, w:4.0, h:1.8,
    fontSize:72, fontFace:FONT.header, color:C.accentLt, bold:true, align:"center", valign:"middle", margin:0
  });
  s.addText("AI 관련 도서 비중", {
    x:0.8, y:3.2, w:4.0, h:0.4,
    fontSize:14, fontFace:FONT.body, color:C.textLight, align:"center", margin:0
  });

  // Right side — AI keywords breakdown
  s.addShape(pres.shapes.RECTANGLE, {
    x:5.3, y:1.4, w:4.2, h:2.5,
    fill:{color:"243447"}
  });
  s.addText("AI 도서 유형 분류", {
    x:5.6, y:1.55, w:3.6, h:0.35,
    fontSize:14, fontFace:FONT.header, color:C.accentLt, bold:true, align:"left", margin:0
  });
  const aiTypes = [
    ["ChatGPT·GPT 활용", "바이브 코딩"],
    ["Claude·에이전트", "프롬프트 엔지니어링"],
    ["AI 반도체·산업", "AI 에듀테크"],
  ];
  aiTypes.forEach((at, i) => {
    const ay = 2.1 + i * 0.52;
    s.addShape(pres.shapes.OVAL, {
      x:5.6, y:ay+0.05, w:0.2, h:0.2,
      fill:{color:C.accent}
    });
    s.addText(`${at[0]}  +  ${at[1]}`, {
      x:5.95, y:ay, w:3.2, h:0.35,
      fontSize:11, fontFace:FONT.body, color:C.textWhite, align:"left", valign:"middle", margin:0
    });
  });

  // Bottom insight
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.8, y:4.1, w:8.4, h:1.1,
    fill:{color:C.accentDk}
  });
  s.addText("ChatGPT, Claude, Gemini 3대 LLM을 중심으로 한 실전 활용서가 시장을 주도하며, 바이브 코딩과 에이전트 개발이 새로운 카테고리로 부상", {
    x:1.1, y:4.2, w:7.8, h:0.9,
    fontSize:12, fontFace:FONT.body, color:C.textWhite, align:"left", valign:"middle", margin:0
  });
  s.addNotes("가장 주목할 트렌드는 AI 도서입니다. 전체 1,000권 중 339권, 33.9%가 AI 관련 도서입니다. 이는 전체 IT 베스트셀러의 3분의 1 이상이 AI를 다루고 있다는 놀라운 수치입니다. AI 도서는 크게 ChatGPT 활용, Claude·에이전트, 바이브 코딩, 프롬프트 엔지니어링, AI 반도체·산업, AI 에듀테크 등으로 분류됩니다. 특히 ChatGPT, Claude, Gemini 3대 LLM을 중심으로 한 실전 활용서가 시장을 주도하고 있으며, 바이브 코딩과 에이전트 개발은 새로운 카테고리로 급부상하고 있습니다.");
}

// ── SLIDE 8: AI BOOK TRENDS — PUBLICATION TIMELINE ──────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("AI 도서 출판 연도별 추이", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // Line chart — year distribution
  s.addChart(pres.charts.BAR, [{
    name: "도서 수",
    labels: ["2020","2021","2022","2023","2024","2025","2026"],
    values: [18, 15, 47, 36, 122, 326, 405]
  }], {
    x:0.5, y:1.1, w:9.0, h:3.0, barDir:"col",
    chartColors: [C.accent, C.accent, C.accent, C.accent, C.accentDk, C.accent, C.warmAccent],
    showValue: true, dataLabelPosition:"outEnd", dataLabelColor: C.text,
    valGridLine:{color:"E2E8F0", size:0.5}, catGridLine:{style:"none"},
    catAxisLabelColor:C.textLight, valAxisLabelColor:C.textLight,
    showLegend:false, chartArea:{fill:{color:C.cardBg}, roundedCorners:true}
  });

  // Insight box
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:4.3, w:9.0, h:1.0,
    fill:{color:C.accentDk}
  });
  s.addText([
    {text:"ChatGPT 출시(2022.11) 이후 폭발적 성장  →  ", options:{bold:true}},
    {text:"2024년 122권 → 2025년 326권(2.7배) → 2026년 상반기만에 405권(연간 환산 800권+)", options:{}},
  ], {
    x:0.8, y:4.4, w:8.4, h:0.8,
    fontSize:11, fontFace:FONT.body, color:C.textWhite, align:"left", valign:"middle", margin:0
  });
  s.addNotes("연도별 출판 추이를 보면, 2022년 ChatGPT 출시를 기점으로 AI 도서가 폭발적으로 성장했습니다. 2022년 47권에서 2023년 36권으로 약간 주춤했지만, 2024년 122권, 2025년 326권으로 급격히 증가했습니다. 특히 2026년 상반기만에 이미 405권이 출간되어, 연간 환산 시 800권 이상이 출간될 것으로 예상됩니다. 이는 AI 도서 시장이 여전히 가파르게 성장하고 있음을 보여줍니다.");
}

// ── SLIDE 9: TOP AI BOOKS ──────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("주목할 AI 베스트셀러", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // Featured book card
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:1.1, w:9.0, h:1.5,
    fill:{color:C.cardBg}, shadow:mkShadow()
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:1.1, w:0.08, h:1.5,
    fill:{color:C.warmAccent}
  });
  s.addText("1위", {
    x:0.8, y:1.2, w:0.8, h:0.5,
    fontSize:24, fontFace:FONT.header, color:C.warmAccent, bold:true, align:"center", valign:"middle", margin:0
  });
  s.addText("바로바로 클로드 with 코워크, 스킬, 클로드 코드, 디자인", {
    x:1.6, y:1.15, w:5.5, h:0.4,
    fontSize:14, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });
  s.addText("차진우  |  골든래빗  |  25,200원  |  평점 9.6  |  리뷰 11건", {
    x:1.6, y:1.55, w:5.5, h:0.3,
    fontSize:10, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
  });
  s.addText("Claude를 활용한 실전 코딩·디자인 가이드. 코워크·스킬·클로드 코드를 아우르는 올인원 서적", {
    x:1.6, y:1.95, w:5.5, h:0.4,
    fontSize:10, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x:7.5, y:1.25, w:1.8, h:0.65,
    fill:{color:C.accent}
  });
  s.addText("25,200원", {
    x:7.5, y:1.3, w:1.8, h:0.55,
    fontSize:18, fontFace:FONT.header, color:C.textWhite, bold:true, align:"center", valign:"middle", margin:0
  });

  // Top 5 table-like layout
  const topBooks = [
    ["2", "혼자 공부하는 바이브 코딩 with 클로드 코드", "한빛미디어", "27,000원", "9.9", "170"],
    ["3", "뚝딱 바로 써먹는 AI 3대장 챗GPT·제미나이·클로드", "안경다리BOOKS", "19,800원", "10.0", "29"],
    ["4", "이게 되네? 제미나이 완전 미친 활용법 81제", "골든래빗", "21,600원", "9.8", "161"],
    ["5", "요즘 교사를 위한 에듀테크 5대장", "앤써북", "17,820원", "10.0", "93"],
  ];
  // Table header
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:2.85, w:9.0, h:0.35,
    fill:{color:C.accentDk}
  });
  s.addText("순위", { x:0.55, y:2.87, w:0.5, h:0.3, fontSize:9, fontFace:FONT.body, color:C.textWhite, bold:true, align:"center", margin:0 });
  s.addText("도서명", { x:1.1, y:2.87, w:3.8, h:0.3, fontSize:9, fontFace:FONT.body, color:C.textWhite, bold:true, align:"left", margin:0 });
  s.addText("출판사", { x:5.0, y:2.87, w:1.3, h:0.3, fontSize:9, fontFace:FONT.body, color:C.textWhite, bold:true, align:"center", margin:0 });
  s.addText("가격", { x:6.4, y:2.87, w:0.9, h:0.3, fontSize:9, fontFace:FONT.body, color:C.textWhite, bold:true, align:"center", margin:0 });
  s.addText("평점", { x:7.4, y:2.87, w:0.6, h:0.3, fontSize:9, fontFace:FONT.body, color:C.textWhite, bold:true, align:"center", margin:0 });
  s.addText("리뷰", { x:8.1, y:2.87, w:0.6, h:0.3, fontSize:9, fontFace:FONT.body, color:C.textWhite, bold:true, align:"center", margin:0 });

  topBooks.forEach((bk, i) => {
    const by = 3.25 + i * 0.5;
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.5, y:by, w:9.0, h:0.45,
      fill:{color: i%2===0 ? C.cardBg : C.midBg}
    });
    s.addText(bk[0], { x:0.55, y:by, w:0.5, h:0.45, fontSize:10, fontFace:FONT.body, color:C.text, align:"center", valign:"middle", margin:0 });
    s.addText(bk[1], { x:1.1, y:by, w:3.8, h:0.45, fontSize:10, fontFace:FONT.body, color:C.text, align:"left", valign:"middle", margin:0 });
    s.addText(bk[2], { x:5.0, y:by, w:1.3, h:0.45, fontSize:9, fontFace:FONT.body, color:C.textLight, align:"center", valign:"middle", margin:0 });
    s.addText(bk[3], { x:6.4, y:by, w:0.9, h:0.45, fontSize:10, fontFace:FONT.body, color:C.accentDk, align:"center", valign:"middle", margin:0 });
    s.addText(bk[4], { x:7.4, y:by, w:0.6, h:0.45, fontSize:10, fontFace:FONT.body, color:C.warmAccent, bold:true, align:"center", valign:"middle", margin:0 });
    s.addText(bk[5], { x:8.1, y:by, w:0.6, h:0.45, fontSize:10, fontFace:FONT.body, color:C.textLight, align:"center", valign:"middle", margin:0 });
  });

  s.addNotes("AI 베스트셀러 상위 도서를 살펴보면, 1위는 차진우 저자의 '바로바로 클로드'입니다. Claude를 활용한 실전 코딩과 디자인을 다루는 올인원 서적으로, 25,200원에 판매되고 있습니다. 2위는 '혼자 공부하는 바이브 코딩'으로 170건의 리뷰를 보유하고 있어 실제 독자 수요가 높습니다. 3위의 'AI 3대장'은 ChatGPT, Gemini, Claude를 모두 다루는 종합서로 평점 10.0을 기록하고 있습니다. 4위는 Gemini 활용서, 5위는 에듀테크 도서로, AI 활용서가 시장 상위를 독점하고 있습니다.");
}

// ── SLIDE 10: EDUCATION & EDUTECH ───────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("교육·에듀테크 도서 시장", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // Stats row
  const eduStats = [
    ["75권", "교육 관련 도서", C.coolAccent],
    ["7.5%", "전체 비중", C.accent],
    ["19,400원", "평균 가격", C.warmAccent],
    ["9.85", "평균 평점", C.accentDk],
  ];
  eduStats.forEach((es, i) => {
    const ex = 0.5 + i * 2.35;
    s.addShape(pres.shapes.RECTANGLE, {
      x:ex, y:1.1, w:2.1, h:1.1,
      fill:{color:C.cardBg}, shadow:mkCardShadow()
    });
    s.addText(es[0], {
      x:ex, y:1.15, w:2.1, h:0.55,
      fontSize:24, fontFace:FONT.header, color:es[2], bold:true, align:"center", valign:"middle", margin:0
    });
    s.addText(es[1], {
      x:ex, y:1.75, w:2.1, h:0.35,
      fontSize:10, fontFace:FONT.body, color:C.textLight, align:"center", margin:0
    });
  });

  // Education trends
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:2.5, w:9.0, h:2.7,
    fill:{color:C.cardBg}, shadow:mkCardShadow()
  });
  s.addText("교육 시장 핵심 트렌드", {
    x:0.8, y:2.6, w:4.0, h:0.4,
    fontSize:16, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });
  const eduTrends = [
    {icon:"AI + 교육 융합", desc:"교사를 위한 AI 활용 가이드가 인기. 2022 개정 교육과정 연계"},
    {icon:"에듀테크 도구 통합", desc:"캔바, 패들렛, 노션 등 에듀테크 도구 + AI를 결합한 서적"},
    {icon:"실전 수업 활용", desc:"바로 수업에 적용 가능한 실습 중심 구성이 높은 평점"},
    {icon:"영어·수업 루틴", desc:"과목별 AI 활용법이 새로운 카테고리로 부상"},
  ];
  eduTrends.forEach((et, i) => {
    const ey = 3.15 + i * 0.5;
    s.addShape(pres.shapes.OVAL, {
      x:0.9, y:ey+0.05, w:0.2, h:0.2,
      fill:{color:C.accent}
    });
    s.addText(et.icon, {
      x:1.25, y:ey, w:2.5, h:0.3,
      fontSize:11, fontFace:FONT.body, color:C.text, bold:true, align:"left", margin:0
    });
    s.addText(et.desc, {
      x:3.8, y:ey, w:5.3, h:0.3,
      fontSize:10, fontFace:FONT.body, color:C.textLight, align:"left", margin:0
    });
  });

  s.addNotes("교육·에듀테크 도서 시장도 주목할 만합니다. 75권으로 전체의 7.5%를 차지하며, 평균 평점이 9.85로 매우 높습니다. 교육 시장의 핵심 트렌드는 AI와 교육의 융합입니다. 교사를 위한 AI 활용 가이드가 인기를 끌고 있으며, 2022 개정 교육과정과 연계된 서적들이 주목받고 있습니다. 에듀테크 도구인 캔바, 패들렛, 노션 등을 AI와 결합한 서적도 인기 있고, 과목별 AI 활용법이 새로운 카테고리로 부상하고 있습니다.");
}

// ── SLIDE 11: REVIEW & RATING INSIGHTS ─────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("고객 리뷰 인사이트", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // Most reviewed — horizontal bars
  s.addText("리뷰 많은 도서 TOP 5", {
    x:0.8, y:1.05, w:4.5, h:0.35,
    fontSize:14, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });
  const reviewData = [
    {name:"실무 엑셀", reviews:388, color:C.accentDk},
    {name:"노션 Notion", reviews:370, color:C.accent},
    {name:"파이썬 입문", reviews:310, color:C.coolAccent},
    {name:"SNS 디자인 캔바", reviews:273, color:C.warmAccent},
    {name:"챗GPT 활용법 71제", reviews:259, color:C.accentLt},
  ];
  const maxReview = 388;
  reviewData.forEach((rd, i) => {
    const ry = 1.55 + i * 0.55;
    s.addText(rd.name, {
      x:0.8, y:ry, w:2.0, h:0.4,
      fontSize:10, fontFace:FONT.body, color:C.text, align:"left", valign:"middle", margin:0
    });
    // Bar background
    s.addShape(pres.shapes.RECTANGLE, {
      x:2.9, y:ry+0.08, w:2.2, h:0.24,
      fill:{color:C.midBg}
    });
    // Bar fill
    s.addShape(pres.shapes.RECTANGLE, {
      x:2.9, y:ry+0.08, w: 2.2 * (rd.reviews / maxReview), h:0.24,
      fill:{color:rd.color}
    });
    s.addText(`${rd.reviews}`, {
      x:2.9 + 2.2 * (rd.reviews / maxReview) + 0.1, y:ry, w:0.6, h:0.4,
      fontSize:10, fontFace:FONT.body, color:C.text, bold:true, align:"left", valign:"middle", margin:0
    });
  });

  // Right — Rating distribution
  s.addText("평점 분포", {
    x:5.6, y:1.05, w:4.0, h:0.35,
    fontSize:14, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });
  s.addChart(pres.charts.BAR, [{
    name: "도서 수",
    labels: ["9.0~9.3","9.4~9.6","9.7~9.8","9.9~10.0"],
    values: [58, 100, 165, 391]
  }], {
    x:5.3, y:1.45, w:4.3, h:2.5, barDir:"col",
    chartColors: [C.accentLt, C.accent, C.accentDk, C.warmAccent],
    showValue: true, dataLabelPosition:"outEnd", dataLabelColor: C.text,
    valGridLine:{color:"E2E8F0", size:0.5}, catGridLine:{style:"none"},
    catAxisLabelColor:C.textLight, valAxisLabelColor:C.textLight,
    showLegend:false, chartArea:{fill:{color:C.cardBg}, roundedCorners:true}
  });

  // Key insight
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:4.35, w:9.0, h:0.9,
    fill:{color:C.accentDk}
  });
  s.addText("평점 9.7 이상이 전체의 56% — IT 독자는 만족도가 높음. 리뷰 200건 이상은 실무서·활용서 위주로 집중", {
    x:0.8, y:4.45, w:8.4, h:0.7,
    fontSize:12, fontFace:FONT.body, color:C.textWhite, align:"left", valign:"middle", margin:0
  });
  s.addNotes("고객 리뷰 인사이트를 살펴보겠습니다. 리뷰가 가장 많은 도서는 '진짜 쓰는 실무 엑셀'로 388건의 리뷰를 보유하고 있습니다. 그 뒤를 '노션 Notion' 370건, '파이썬 입문' 310건, 'SNS 디자인 캔바' 273건, '챗GPT 활용법 71제' 259건이 잇고 있습니다. 공통점은 모두 실전 활용 서적이라는 점입니다. 평점 분포를 보면 9.7 이상이 전체의 56%로, IT 독자들은 만족도가 매우 높습니다. 리뷰가 200건 이상인 도서는 실무서와 활용서에 집중되어 있어, 독자들이 실질적인 도움을 주는 도서를 선호함을 알 수 있습니다.");
}

// ── SLIDE 12: PUBLISHING YEAR TRENDS ────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("출판 연도별 시장 변화", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // Stacked bar — year distribution with categories
  s.addChart(pres.charts.BAR, [
    {name:"AI/LLM", labels:["2020","2021","2022","2023","2024","2025","2026"], values:[3,2,15,12,55,155,197]},
    {name:"프로그래밍", labels:["2020","2021","2022","2023","2024","2025","2026"], values:[8,7,18,14,38,88,102]},
    {name:"교육/에듀테크", labels:["2020","2021","2022","2023","2024","2025","2026"], values:[2,2,5,3,10,38,52]},
    {name:"기타", labels:["2020","2021","2022","2023","2024","2025","2026"], values:[5,4,9,7,19,45,54]},
  ], {
    x:0.5, y:1.0, w:9.0, h:3.0, barDir:"col", barGrouping:"stacked",
    chartColors: [C.accent, C.coolAccent, C.warmAccent, C.divider],
    valGridLine:{color:"E2E8F0", size:0.5}, catGridLine:{style:"none"},
    catAxisLabelColor:C.textLight, valAxisLabelColor:C.textLight,
    showLegend:true, legendPos:"b", legendFontSize:9,
    chartArea:{fill:{color:C.cardBg}, roundedCorners:true}
  });

  // Insight
  s.addShape(pres.shapes.RECTANGLE, {
    x:0.5, y:4.3, w:9.0, h:1.0,
    fill:{color:C.darkBg}
  });
  s.addText([
    {text:"AI/LLM 도서가 전체 시장을 주도하며,", options:{bold:true, color:C.accentLt}},
    {text:" 프로그래밍·교육 도서도 AI와 결합되면서 전체 시장이 확대되고 있음", options:{color:C.textWhite}},
  ], {
    x:0.8, y:4.4, w:8.4, h:0.8,
    fontSize:12, fontFace:FONT.body, align:"left", valign:"middle", margin:0
  });
  s.addNotes("출판 연도별 시장 변화를 카테고리별로 보면, AI/LLM 도서가 전체 시장을 주도하고 있음을 확인할 수 있습니다. 2020년 3권에서 2026년 197권으로 폭발적으로 성장했습니다. 프로그래밍 도서도 AI와 결합되면서 꾸준히 증가하고 있으며, 교육/에듀테크 도서도 2025년 이후 급증하고 있습니다. 전체 IT 출판 시장이 AI를 중심으로 재편되고 있는 것입니다.");
}

// ── SLIDE 13: COMPETITIVE LANDSCAPE ─────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addText("경쟁 환경과 기회 영역", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
  });

  // 2x2 Grid
  const quadrants = [
    {x:0.5, y:1.1, title:"높은 수요 + 높은 경쟁", sub:"ChatGPT/Gemini 활용서",
     desc:"시장 포화 상태. 차별화된 실전 사례가 필수", bg:C.midBg, titleColor:C.warmAccent},
    {x:5.15, y:1.1, title:"높은 수요 + 낮은 경쟁", sub:"Claude·에이전트 개발",
     desc:"성장 초기. 선점 기회가 큰 영역", bg:C.cardBg, titleColor:C.accent},
    {x:0.5, y:3.1, title:"낮은 수요 + 높은 경쟁", sub:"단순 이론서·개론서",
     desc:"수요 감소 추세. 피하거나 차별화 필요", bg:C.cardBg, titleColor:C.coolAccent},
    {x:5.15, y:3.1, title:"낮은 수요 + 낮은 경쟁", sub:"하드웨어·반도체 심화",
     desc:"틈새 시장. 전문 독자층 확보 시 안정적", bg:C.midBg, titleColor:C.accentDk},
  ];
  quadrants.forEach(q => {
    s.addShape(pres.shapes.RECTANGLE, {
      x:q.x, y:q.y, w:4.4, h:1.8,
      fill:{color:q.bg}, shadow:mkCardShadow()
    });
    s.addText(q.title, {
      x:q.x+0.2, y:q.y+0.1, w:4.0, h:0.3,
      fontSize:12, fontFace:FONT.header, color:q.titleColor, bold:true, align:"left", margin:0
    });
    s.addText(q.sub, {
      x:q.x+0.2, y:q.y+0.45, w:4.0, h:0.3,
      fontSize:14, fontFace:FONT.header, color:C.text, bold:true, align:"left", margin:0
    });
    s.addText(q.desc, {
      x:q.x+0.2, y:q.y+0.85, w:4.0, h:0.7,
      fontSize:10, fontFace:FONT.body, color:C.textLight, align:"left", valign:"top", margin:0
    });
  });

  s.addNotes("경쟁 환경을 2x2 매트릭스로 분석해 보겠습니다. 높은 수요+높은 경쟁 영역에는 ChatGPT와 Gemini 활용서가 있습니다. 시장이 포화 상태이므로 차별화된 실전 사례가 필수적입니다. 반면 높은 수요+낮은 경쟁 영역에는 Claude와 에이전트 개발이 있습니다. 이 영역은 성장 초기 단계로 선점 기회가 매우 큽니다. 낮은 수요+높은 경쟁 영역은 단순 이론서와 개론서로, 수요가 감소하는 추세이므로 피하거나 강력한 차별화가 필요합니다. 마지막으로 낮은 수요+낮은 경쟁 영역은 하드웨어·반도체 심화 분야로, 틈새 시장이지만 전문 독자층을 확보하면 안정적입니다.");
}

// ── SLIDE 14: NEW BOOK PROPOSALS ────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.04, fill:{color:C.accent} });

  s.addText("신규 도서 기획 제안", {
    x:0.8, y:0.35, w:8.4, h:0.6,
    fontSize:28, fontFace:FONT.header, color:C.textWhite, bold:true, align:"left", margin:0
  });

  const proposals = [
    {
      num: "A",
      title: "Claude 실전 에이전트 개발",
      price: "25,000~28,000원",
      why: "시장 성장 초기, 선점 기회 극대화",
      target: "개발자·엔지니어",
      color: C.accent,
    },
    {
      num: "B",
      title: "직장인 AI 업무 자동화 실전",
      price: "19,800~22,000원",
      why: "비개발자 대상 AI 활용 수요 폭증",
      target: "일반 직장인",
      color: C.coolAccent,
    },
    {
      num: "C",
      title: "교육 AI 올인원 가이드",
      price: "22,000~25,000원",
      why: "교육 시장 AI 전환 수요, 75권→200권+ 전망",
      target: "교사·교육관계자",
      color: C.warmAccent,
    },
  ];
  proposals.forEach((pr, i) => {
    const py = 1.15 + i * 1.4;
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.8, y:py, w:8.4, h:1.2,
      fill:{color:"243447"}
    });
    // Left accent
    s.addShape(pres.shapes.RECTANGLE, {
      x:0.8, y:py, w:0.08, h:1.2,
      fill:{color:pr.color}
    });
    // Letter badge
    s.addShape(pres.shapes.OVAL, {
      x:1.1, y:py+0.3, w:0.55, h:0.55,
      fill:{color:pr.color}
    });
    s.addText(pr.num, {
      x:1.1, y:py+0.3, w:0.55, h:0.55,
      fontSize:16, fontFace:FONT.header, color:C.textWhite, bold:true, align:"center", valign:"middle", margin:0
    });
    // Title
    s.addText(pr.title, {
      x:1.85, y:py+0.1, w:5.0, h:0.35,
      fontSize:16, fontFace:FONT.header, color:C.textWhite, bold:true, align:"left", margin:0
    });
    // Price badge
    s.addShape(pres.shapes.RECTANGLE, {
      x:7.3, y:py+0.1, w:1.7, h:0.35,
      fill:{color:pr.color}
    });
    s.addText(pr.price, {
      x:7.3, y:py+0.1, w:1.7, h:0.35,
      fontSize:10, fontFace:FONT.body, color:C.textWhite, bold:true, align:"center", valign:"middle", margin:0
    });
    // Details
    s.addText([
      {text:"기획 근거: ", options:{bold:true}},
      {text:pr.why, options:{breakLine:true}},
      {text:"타겟 독자: ", options:{bold:true}},
      {text:pr.target},
    ], {
      x:1.85, y:py+0.55, w:7.0, h:0.55,
      fontSize:10, fontFace:FONT.body, color:C.textLight, lineSpacingMultiple:1.4, align:"left", margin:0
    });
  });

  s.addNotes("데이터 분석을 바탕으로 3건의 신규 도서 기획을 제안합니다. 제안 A는 Claude 기반 실전 에이전트 개발 서적으로, 25,000~28,000원대입니다. Claude 도서가 시장에서 빠르게 성장하고 있고 경쟁이 적어 선점 기회가 큽니다. 제안 B는 직장인 대상 AI 업무 자동화 실전서로, 19,800~22,000원대입니다. 비개발자들의 AI 활용 수요가 폭증하고 있어 타겟이 명확합니다. 제안 C는 교육 AI 올인원 가이드로, 22,000~25,000원대입니다. 교육 시장의 AI 전환이 빨라지고 있어 성장 잠재력이 큽니다.");
}

// ── SLIDE 15: CLOSING ──────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.04, fill:{color:C.accent} });

  s.addText("Summary & Next Steps", {
    x:0.8, y:0.6, w:8.4, h:0.7,
    fontSize:32, fontFace:FONT.header, color:C.textWhite, bold:true, align:"left", margin:0
  });

  // Key takeaways
  const takeaways = [
    "AI 도서가 IT 베스트셀러의 33.9% — 가장 성장하는 카테고리",
    "가격 1.5~2.5만원대가 전체의 58% — 2만원대 전략이 적합",
    "실전 활용서가 리뷰·판매량 모두에서 우위 — 실습 중심 구성 필수",
    "Claude·에이전트 개발 분야가 높은 수요 + 낮은 경쟁으로 기회 영역",
  ];
  takeaways.forEach((ta, i) => {
    const ty = 1.6 + i * 0.6;
    s.addShape(pres.shapes.OVAL, {
      x:0.8, y:ty+0.07, w:0.22, h:0.22,
      fill:{color:C.accent}
    });
    s.addText(ta, {
      x:1.2, y:ty, w:8.0, h:0.4,
      fontSize:13, fontFace:FONT.body, color:C.textWhite, align:"left", valign:"middle", margin:0
    });
  });

  // Bottom bar
  s.addShape(pres.shapes.RECTANGLE, {
    x:0, y:4.55, w:10, h:1.075,
    fill:{color:C.accentDk}
  });
  s.addText([
    {text:"다음 단계", options:{bold:true, breakLine:true}},
    {text:"기획안 초안 작성  →  원고 체계 구성  →  편집·디자인  →  출간 일정 확정", options:{}},
  ], {
    x:0.8, y:4.65, w:8.4, h:0.9,
    fontSize:13, fontFace:FONT.body, color:C.textWhite, align:"left", valign:"middle", margin:0
  });
  s.addNotes("마지막으로 핵심 요약과 다음 단계를 정리하겠습니다. 첫째, AI 도서가 전체 IT 베스트셀러의 33.9%를 차지하며 가장 빠르게 성장하는 카테고리입니다. 둘째, 가격 1.5~2.5만원대가 전체의 58%를 차지하므로 2만원대 가격 전략이 적합합니다. 셋째, 실전 활용서가 리뷰와 판매량 모두에서 우위를 보이고 있어 실습 중심 구성이 필수적입니다. 넷째, Claude와 에이전트 개발 분야가 높은 수요와 낮은 경쟁으로 가장 큰 기회 영역입니다. 다음 단계로는 기획안 초안 작성, 원고 첅계 구성, 편집·디자인, 그리고 출간 일정 확정이 필요합니다. 감사합니다.");
}

// ── WRITE FILE ──────────────────────────────────────────────
pres.writeFile({ fileName: "output/YES24_IT_Bestseller_Analysis.pptx" })
  .then(() => console.log("PPTX created: output/YES24_IT_Bestseller_Analysis.pptx"))
  .catch(err => console.error("Error:", err));

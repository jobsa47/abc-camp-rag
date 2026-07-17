"""YES24 IT bestseller 데이터 분석 스크립트."""
import json
import pandas as pd

df = pd.read_csv('data/yes24_it_bestseller.csv')

cols = list(df.columns)
print("Columns:", cols)

# Basic stats
print(f"\n=== BASIC STATS ===")
print(f"Total books: {len(df)}")
print(f"Avg price: {df[cols[6]].mean():.0f}")
print(f"Max/Min price: {df[cols[6]].max()} / {df[cols[6]].min()}")
print(f"Avg rating: {df[cols[7]].mean():.2f}")
print(f"Avg reviews: {df[cols[8]].mean():.1f}")
print(f"Median price: {df[cols[6]].median():.0f}")

# Publisher distribution
print(f"\n=== TOP PUBLISHERS ===")
pub_counts = df[cols[4]].value_counts().head(10)
for pub, cnt in pub_counts.items():
    print(f"  {pub}: {cnt}권 ({cnt/len(df)*100:.1f}%)")

# Price ranges
print(f"\n=== PRICE RANGES ===")
bins = [0, 15000, 20000, 25000, 30000, 999999]
labels = ['<15K', '15-20K', '20-25K', '25-30K', '30K+']
df['price_range'] = pd.cut(df[cols[6]], bins=bins, labels=labels)
for p, c in df['price_range'].value_counts().sort_index().items():
    print(f"  {p}: {c}권")

# Top rated (10.0)
print(f"\n=== TOP RATED (10.0) ===")
top = df[df[cols[7]] == 10.0]
print(f"  Count: {len(top)}")
for _, row in top.head(8).iterrows():
    print(f"  {row[cols[1]]} ({row[cols[4]]}) - reviews: {row[cols[8]]}")

# Most reviewed
print(f"\n=== MOST REVIEWED ===")
mr = df.sort_values(cols[8], ascending=False).head(10)
for _, row in mr.iterrows():
    print(f"  {row[cols[1]]}: {row[cols[8]]} reviews, rating={row[cols[7]]}")

# AI related keywords
print(f"\n=== AI RELATED ===")
ai_kw = ['AI', 'GPT', 'claude', 'Claude', 'vibe', 'Vibe', 'agent', 'Agent', 'LLM', 'prompt']
ai = df[df[cols[1]].str.contains('|'.join(ai_kw), case=False, na=False)]
print(f"  Count: {len(ai)}")
print(f"  Avg price: {ai[cols[6]].mean():.0f}")
print(f"  Avg rating: {ai[cols[7]].mean():.2f}")
print(f"  Avg reviews: {ai[cols[8]].mean():.1f}")
for _, row in ai.head(10).iterrows():
    print(f"  {row[cols[1]]} ({row[cols[4]]}) - {row[cols[6]]}원")

# Education related
print(f"\n=== EDUCATION RELATED ===")
edu_kw = ['교사', '수업', '교육', '에듀']
edu = df[df[cols[1]].str.contains('|'.join(edu_kw), case=False, na=False)]
print(f"  Count: {len(edu)}")
for _, row in edu.head(5).iterrows():
    print(f"  {row[cols[1]]} ({row[cols[4]]})")

# Price distribution stats
print(f"\n=== PRICE DISTRIBUTION ===")
print(f"  25th percentile: {df[cols[6]].quantile(0.25):.0f}")
print(f"  50th percentile: {df[cols[6]].quantile(0.50):.0f}")
print(f"  75th percentile: {df[cols[6]].quantile(0.75):.0f}")

# Rating distribution
print(f"\n=== RATING DISTRIBUTION ===")
rating_dist = df[cols[7]].value_counts().sort_index()
for r, c in rating_dist.items():
    print(f"  {r}: {c}권")

# Publish date analysis
print(f"\n=== PUBLISHER DATE ANALYSIS ===")
# Extract year-month from出版일
df['pub_year'] = df[cols[5]].str.extract(r'(\d{4})')[0].astype(float)
df['pub_year_month'] = df[cols[5]].str.extract(r'(\d{4}년 \d{2}월)')[0]
year_counts = df['pub_year'].value_counts().sort_index()
for y, c in year_counts.items():
    if pd.notna(y):
        print(f"  {int(y)}년: {c}권")

# Export JSON for presentation
data = {
    'total': len(df),
    'avg_price': round(df[cols[6]].mean()),
    'median_price': round(df[cols[6]].median()),
    'max_price': int(df[cols[6]].max()),
    'min_price': int(df[cols[6]].min()),
    'avg_rating': round(df[cols[7]].mean(), 2),
    'avg_reviews': round(df[cols[8]].mean(), 1),
    'ai_count': len(ai),
    'edu_count': len(edu),
    'top_publishers': [(p, int(c)) for p, c in pub_counts.head(5).items()],
    'price_ranges': {str(p): int(c) for p, c in df['price_range'].value_counts().sort_index().items()},
    'top_rated_count': len(top),
    'top_reviewed': [(row[cols[1]][:30], int(row[cols[8]]), float(row[cols[7]])) for _, row in mr.head(5).iterrows()],
    'ai_books': [(row[cols[1]][:40], row[cols[4]], int(row[cols[6]])) for _, row in ai.head(10).iterrows()],
}

with open('data/analysis.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nExported analysis.json")

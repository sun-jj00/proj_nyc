import pandas as pd
import nycflights13 as flights

# 항공편 데이터 (main dataset)
df_flights = flights.flights
df_airlines = flights.airlines
df_airports = flights.airports
df_planes = flights.planes
df_weather = flights.weather

#code1 (항공사별-공항별 출발지연률)
# 1. 분석 대상 항공사 필터링
airlines_filter = ['AA', 'AS', 'B6', 'DL', 'HA', 'OO', 'UA', 'US', 'WN']
df_filtered = df_flights[df_flights['carrier'].isin(airlines_filter)].copy()

# 2. 결측치가 하나라도 있는 행 제거
df_filtered = df_filtered.dropna()

# 3. 지연 여부 컬럼 생성 ()
def classify_delay(delay):
    if delay <= -10:
        return '10분 이상 일찍 출발'
    elif delay >= 60:
        return '1시간 이상 출발지연'
    elif delay >= 10:
        return '10분~1시간 출발지연'
    else:
        return '정시 또는 ±10분'

df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay)
df_filtered

# 4. 전체 건수 기준으로 그룹화
delay_counts = (
    df_filtered
    .groupby(['origin', 'carrier', 'classify_delay'])
    .size()
    .reset_index(name='count')
)

#5. 총 편수 구하기 
total_counts = (
    df_filtered
    .groupby(['origin', 'carrier'])
    .size()
    .reset_index(name='total')
)

# 6. 지연률 퍼센트화
delay_merged = pd.merge(delay_counts, total_counts, on=['origin', 'carrier'])
delay_merged['delay_pct'] = (delay_merged['count'] / delay_merged['total'] * 100).round(2)

# 7. 피벗테이블 출력
pivot = delay_merged.pivot_table(
    index=['origin', 'carrier'],
    columns='classify_delay',
    values='delay_pct',
    fill_value=0
).reset_index()
pivot


df_flights.info()

#그래프 만들기

import matplotlib.pyplot as plt

# 지연 구간 색상 매핑
colors = {
    '빠른출발 및 정시출발(10분이내)': 'gray',
    '10분~1시간 출발지연': 'skyblue',
    '1시간 이상 출발지연': 'red'
}

fig, ax = plt.subplots(figsize=(12, 6))
width = 0.25
x = range(len(carriers))

for i, delay in enumerate(delay_types):
    subset = delay_merged[delay_merged['classify_delay'] == delay]
    subset = subset.set_index('carrier').reindex(carriers).fillna(0)
    heights = subset['delay_pct']
    positions = [p + width * i for p in x]
    
    bars = ax.bar(
        positions,
        heights,
        width=width,
        label=delay,
        color=colors.get(delay, 'lightgray')  # fallback color
    )
    
    # 막대 위에 텍스트 표시
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2,
                height + 0.5,
                f'{height:.1f}%',
                ha='center',
                va='bottom',
                fontsize=9
            )

# x축 정렬
ax.set_xticks([p + width for p in x])
ax.set_xticklabels(carriers)

# 기타 설정
ax.set_title('항공사별 출발 지연률')
ax.set_ylabel('지연률 (%)')
ax.set_xlabel('항공사')
ax.legend(title='지연 구간')
plt.tight_layout()
plt.show()



################
#항공사별 출발지연률 (code2)
def classify_delay_new(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'

# 필터링 + 결측 제거
airlines_filter = ['AA', 'AS', 'B6', 'DL', 'HA', 'OO', 'UA', 'US', 'WN']
df_filtered = df_flights[df_flights['carrier'].isin(airlines_filter)].copy()
df_filtered = df_filtered.dropna()
df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_new)

# 항공사별 전체 지연률 계산
delay_counts_total = (
    df_filtered
    .groupby(['carrier', 'classify_delay'])
    .size()
    .reset_index(name='count')
)

total_counts_total = (
    df_filtered
    .groupby('carrier')
    .size()
    .reset_index(name='total')
)

merged_total = pd.merge(delay_counts_total, total_counts_total, on='carrier')
merged_total['delay_pct'] = (merged_total['count'] / merged_total['total'] * 100).round(2)
merged_total

# 공항별 - 항공사별 지연률
delay_counts_origin = (
    df_filtered
    .groupby(['origin', 'carrier', 'classify_delay'])
    .size()
    .reset_index(name='count')
)

total_counts_origin = (
    df_filtered
    .groupby(['origin', 'carrier'])
    .size()
    .reset_index(name='total')
)

merged_origin = pd.merge(delay_counts_origin, total_counts_origin, on=['origin', 'carrier'])
merged_origin['delay_pct'] = (merged_origin['count'] / merged_origin['total'] * 100).round(2)
merged_origin
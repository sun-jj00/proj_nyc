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

plt.figure(figsize=(16,8))
plt.subplot(221)
# classify_delay 종류 추출 (정렬도 자동화)
delay_types = sorted(df_filtered['classify_delay'].unique())

# 각 delay_type별 carrier별 지연률 추출
carriers = delay_merged['carrier'].unique()
origin_list = delay_merged['origin'].unique()

for origin in origin_list:
    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.2
    x = range(len(carriers))

    for i, delay in enumerate(delay_types):
        # origin 기준 필터
        subset = delay_merged[(delay_merged['classify_delay'] == delay) & (delay_merged['origin'] == origin)]
        subset = subset.set_index('carrier').reindex(carriers).fillna(0)
        ax.bar(
            [p + width * i for p in x],
            subset['delay_pct'],
            width=width,
            label=delay
        )

    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(carriers)
    ax.set_title(f'{origin} 출발 항공사별 출발지연률')
    ax.set_ylabel('지연률 (%)')
    ax.set_xlabel('항공사')
    ax.legend(title='지연 구간')
    plt.tight_layout()
plt.subplot(222)







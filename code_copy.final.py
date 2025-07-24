import pandas as pd
import nycflights13 as flights

df_flights.info()
# 항공편 데이터 (main dataset)
df_flights = flights.flights
df_airlines = flights.airlines
df_airports = flights.airports
df_planes = flights.planes
df_weather = flights.weather

#code1 (항공사별-공항별 출발지연률)
# 1. 분석 대상 항공사 필터링
airlines_filter = ['AA', 'AS', 'B6', 'DL', 'HA', 'OO', 'UA', 'US', 'WN']
df_filtered = df_flights[df_flights['carrier'].isin(airlines_filter)]

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

###공항-항공사별 출발지연률 시각화
import matplotlib.pyplot as plt

# 1. 새로운 범주 정의 함수
def classify_delay_new(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'

# 2. 적용
df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_new)

# 3. delay_counts & total_counts 재생성
delay_counts = (
    df_filtered
    .groupby(['origin', 'carrier', 'classify_delay'])
    .size()
    .reset_index(name='count')
)

total_counts = (
    df_filtered
    .groupby(['origin', 'carrier'])
    .size()
    .reset_index(name='total')
)

# 4. 병합 및 퍼센트 계산
delay_merged = pd.merge(delay_counts, total_counts, on=['origin', 'carrier'])
delay_merged['delay_pct'] = (delay_merged['count'] / delay_merged['total'] * 100).round(2)

# 5. 고정된 carrier 리스트로 누락 방지
carriers = ['AA', 'AS', 'B6', 'DL', 'HA', 'OO', 'UA', 'US', 'WN']
origin_list = delay_merged['origin'].unique()
delay_types = ['빠른출발 및 정시출발(10분이내)', '10분~1시간 출발지연', '1시간 이상 출발지연']
colors = ['gray', 'orange', 'red']  # 범주별 색상 지정

# 6. 시각화
for origin in origin_list:
    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.25
    x = range(len(carriers))

    for i, (delay, color) in enumerate(zip(delay_types, colors)):
        subset = delay_merged[(delay_merged['classify_delay'] == delay) & (delay_merged['origin'] == origin)]
        subset = subset.set_index('carrier').reindex(carriers).fillna(0)

        bar_positions = [p + width * i for p in x]
        bars = ax.bar(
            bar_positions,
            subset['delay_pct'],
            width=width,
            label=delay,
            color=color
        )

        # 막대 위에 지연률 % 표시
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.5,
                    f'{height:.1f}%',
                    ha='center',
                    va='bottom',
                    fontsize=9
                )

    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(carriers)
    ax.set_title(f'{origin} 출발 항공사별 출발지연률')
    ax.set_ylabel('지연률 (%)')
    ax.set_xlabel('항공사')

    ax.legend(title='지연 구간', loc='lower right')

    plt.tight_layout()
    plt.show()

### 항공사별 출발지연률 시각화
import matplotlib.pyplot as plt

# 1. 지연 구간 재정의 함수 (이미 정의했다면 생략 가능)
def classify_delay_new(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'


# 2. 지연 구간 컬럼 적용
df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_new)

# 3. 그룹화 (공항 제거하고 항공사만 기준으로)
delay_counts = (
    df_filtered
    .groupby(['carrier', 'classify_delay'])
    .size()
    .reset_index(name='count')
)

total_counts = (
    df_filtered
    .groupby('carrier')
    .size()
    .reset_index(name='total')
)

# 4. 병합 및 지연률 계산
delay_merged = pd.merge(delay_counts, total_counts, on='carrier')
delay_merged['delay_pct'] = (delay_merged['count'] / delay_merged['total'] * 100).round(2)

# 5. 시각화용 세팅
carriers = ['AA', 'AS', 'B6', 'DL', 'HA', 'OO', 'UA', 'US', 'WN']
delay_types = ['빠른출발 및 정시출발(10분이내)', '10분~1시간 출발지연', '1시간 이상 출발지연']

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
ax.legend(
    title='지연 구간',
    bbox_to_anchor=(1.02, 0),
    loc="lower left",
    frameon=False
)
plt.tight_layout()
plt.show()



# 결측치가 제거
df_filtered = df_filtered.dropna()

# 지연 여부 컬럼 생성 및 범위구간 만들기
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

# 전체 건수 기준으로 그룹화
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
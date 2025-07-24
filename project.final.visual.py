##------------ Code1:항공사별-공항별 출발지연률
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


##### Code2: 산점도 

import matplotlib.pyplot as plt

# 1. 새로운 지연 구간 분류 함수
def classify_delay_v2(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'

# 2. 적용
df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_v2)

# 3. 그룹화
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

# 4. 병합 및 정시율 계산
delay_merged = pd.merge(delay_counts, total_counts, on=['origin', 'carrier'])
delay_merged['delay_pct'] = (delay_merged['count'] / delay_merged['total'] * 100).round(2)

# 5. 피벗 (정시율만 뽑기)
pivot = delay_merged.pivot_table(
    index=['origin', 'carrier'],
    columns='classify_delay',
    values='delay_pct',
    fill_value=0
).reset_index()

# 6. 시각화: 항공사별 산점도
plt.figure(figsize=(12, 6))

for origin in pivot['origin'].unique():
    subset = pivot[pivot['origin'] == origin]
    plt.scatter(
        subset['carrier'],
        subset['빠른출발 및 정시출발(10분이내)'],
        label=origin,
        alpha=0.7,
        s=100  # 점 크기
    )

plt.title('항공사별 공항 출발 정시율 산점도')
plt.xlabel('항공사 (carrier)')
plt.ylabel('정시율 (%)')
plt.legend(title='출발 공항 (origin)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(True)
plt.show()

###########################################

##### Code 3: 바둑판식형 산점도
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 지연 구간 분류 함수
def classify_delay_v2(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'

# 2. 필터링 및 전처리
df_filtered = df_flights[df_flights['carrier'].isin(airlines_filter)].dropna()
df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_v2)

# 3. 지연률 계산
delay_counts = df_filtered.groupby(['origin', 'carrier', 'classify_delay']).size().reset_index(name='count')
total_counts = df_filtered.groupby(['origin', 'carrier']).size().reset_index(name='total')
merged = pd.merge(delay_counts, total_counts, on=['origin', 'carrier'])
merged['delay_pct'] = (merged['count'] / merged['total'] * 100).round(2)

# 4. 피벗: 정시율만 뽑기
pivot = merged[merged['classify_delay'] == '빠른출발 및 정시출발(10분이내)']
heatmap_data = pivot.pivot(index='carrier', columns='origin', values='delay_pct')

# 5. 시각화: 히트맵
plt.figure(figsize=(10, 6))
sns.heatmap(
    heatmap_data,
    annot=True,         # 셀 안에 숫자 표시
    fmt='.1f',          # 소수점 1자리
    cmap='YlGnBu',      # 색상 그라데이션
    linewidths=0.5,
    linecolor='gray',
    cbar_kws={'label': '정시출발 비율 (%)'}
)

plt.title('공항별 항공사 정시출발율')
plt.xlabel('공항 (origin)')
plt.ylabel('항공사 (carrier)')
plt.tight_layout()
plt.show()

##################################################
###### Code 4: 정시출발률 (채택)
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 지연 구간 분류 함수
def classify_delay_v2(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'

# 2. 필터링 및 전처리
df_filtered = df_flights[df_flights['carrier'].isin(airlines_filter)].dropna()
df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_v2)

# 3. 지연률 계산
delay_counts = df_filtered.groupby(['origin', 'carrier', 'classify_delay']).size().reset_index(name='count')
total_counts = df_filtered.groupby(['origin', 'carrier']).size().reset_index(name='total')
merged = pd.merge(delay_counts, total_counts, on=['origin', 'carrier'])
merged['delay_pct'] = (merged['count'] / merged['total'] * 100).round(2)

# 4. 피벗: 정시율만 뽑기
pivot = merged[merged['classify_delay'] == '빠른출발 및 정시출발(10분이내)']
heatmap_data = pivot.pivot(index='carrier', columns='origin', values='delay_pct')

# 5. 시각화: 히트맵
plt.figure(figsize=(10, 6))
sns.heatmap(
    heatmap_data,
    annot=True,         # 셀 안에 숫자 표시
    fmt='.1f',          # 소수점 1자리
    cmap='YlGnBu',      # 색상 그라데이션
    linewidths=0.5,
    linecolor='gray',
    cbar_kws={'label': '정시출발 비율 (%)'}
)

plt.title('공항별 항공사의 빠른/정시 출발률', fontsize=14)
plt.xlabel('출발 공항', fontsize=12)
plt.ylabel('항공사', fontsize=12)
plt.tight_layout()
plt.show()

#############################################
###### Code 5: 항공사별 출발지연률
import matplotlib.pyplot as plt
import pandas as pd

# 1. 필터링 및 결측 제거
airlines_filter = ['AA', 'AS', 'B6', 'DL', 'HA', 'OO', 'UA', 'US', 'WN']
df_filtered = df_flights[df_flights['carrier'].isin(airlines_filter)].dropna()

# 2. 지연 구간 분류 함수
def classify_delay_v2(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'

# 3. 지연 구간 컬럼 추가
df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_v2)

# 4. 그룹별 건수 및 퍼센트 계산
grouped = df_filtered.groupby(['carrier', 'classify_delay']).size().reset_index(name='count')
total = df_filtered.groupby('carrier').size().reset_index(name='total')
merged = pd.merge(grouped, total, on='carrier')
merged['pct'] = (merged['count'] / merged['total'] * 100).round(2)

# 5. 피벗테이블 변환 및 순서 고정
pivot = merged.pivot(index='carrier', columns='classify_delay', values='pct').fillna(0)
pivot = pivot[['빠른출발 및 정시출발(10분이내)', '10분~1시간 출발지연', '1시간 이상 출발지연']]
pivot = pivot.sort_values(by='1시간 이상 출발지연', ascending=False)

# 6. 색상 지정
colors = ['gray', 'blue', 'red']

# 7. 시각화
fig, ax = plt.subplots(figsize=(10, 6))
left = [0] * len(pivot)
carriers = pivot.index.tolist()

for i, col in enumerate(pivot.columns):
    bar = ax.barh(carriers, pivot[col], left=left, color=colors[i], label=col)

    for j, rect in enumerate(bar):
        width = rect.get_width()
        if width > 3:
            ax.text(rect.get_x() + width / 2, rect.get_y() + rect.get_height() / 2,
                    f'{width:.1f}%', ha='center', va='center', color='white', fontsize=9)

    left = [l + w for l, w in zip(left, pivot[col])]

# 8. 마무리
ax.set_xlabel('비율 (%)')
ax.set_title('항공사별 출발지연 구간 비율')
ax.legend(loc='lower right', frameon=False)
plt.tight_layout()
plt.show()


###### Code6: 투명 범주 추가 (채택)
import matplotlib.pyplot as plt
import pandas as pd

# 1. 항공사 필터링 및 결측치 제거
airlines_filter = ['AA', 'AS', 'B6', 'DL', 'HA', 'OO', 'UA', 'US', 'WN']
df_filtered = df_flights[df_flights['carrier'].isin(airlines_filter)].dropna()

# 2. 지연 구간 분류 함수
def classify_delay_v2(delay):
    if delay <= 10:
        return '빠른출발 및 정시출발(10분이내)'
    elif delay < 60:
        return '10분~1시간 출발지연'
    else:
        return '1시간 이상 출발지연'

df_filtered['classify_delay'] = df_filtered['dep_delay'].apply(classify_delay_v2)

# 3. 그룹별 건수 및 퍼센트 계산
grouped = df_filtered.groupby(['carrier', 'classify_delay']).size().reset_index(name='count')
total = df_filtered.groupby('carrier').size().reset_index(name='total')
merged = pd.merge(grouped, total, on='carrier')
merged['pct'] = (merged['count'] / merged['total'] * 100).round(2)

# 4. 피벗테이블 생성 및 정렬
pivot = merged.pivot(index='carrier', columns='classify_delay', values='pct').fillna(0)
pivot = pivot[['빠른출발 및 정시출발(10분이내)', '10분~1시간 출발지연', '1시간 이상 출발지연']]
pivot = pivot.sort_values(by='1시간 이상 출발지연', ascending=False)

# 5. 색상 설정
colors = ['gray', 'blue', 'red']

# 6. 시각화
fig, ax = plt.subplots(figsize=(10, 6))
left = [0] * len(pivot)
carriers = pivot.index.tolist()

for i, col in enumerate(pivot.columns):
    bar = ax.barh(carriers, pivot[col], left=left, color=colors[i], label=col)

    for j, rect in enumerate(bar):
        width = rect.get_width()
        if width > 3:
            ax.text(
                rect.get_x() + width / 2,
                rect.get_y() + rect.get_height() / 2,
                f'{width:.1f}%',
                ha='center',
                va='center',
                fontsize=9,
                bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2')
            )

    left = [l + w for l, w in zip(left, pivot[col])]

# 7. 꾸미기
ax.set_xlabel('비율 (%)')
ax.set_title('항공사별 출발지연 구간 비율')
ax.legend(
    title='지연 구간',
    loc='upper right',
    bbox_to_anchor=(1.0, 1.3),
    ncol=1,
    frameon=True,
    edgecolor="lightgray"
)
plt.tight_layout()
plt.show()
 
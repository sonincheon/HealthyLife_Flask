import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


# 파일가져오기
data = pd.read_csv('../data/life_expectancy_data.csv', sep=',', encoding='utf-8')

# # 데이터프레임의 요약 통계 정보 출력
# print(data.describe())
# # 데이터프레임의 쿨럼값
# print(data.columns)
# # 쿨럼값의 타입
# print(data.dtypes)

# 숫자형 열만 선택
numeric_data = data.select_dtypes(include=['number'])

# 결측치 처리
# numeric_data에 대해 결측치를 중간값으로 대체
numeric_data = numeric_data.fillna(numeric_data.median())

print(numeric_data.dtypes)
print(numeric_data.columns)

# 특성과 타겟 나누기
X = numeric_data[['AdultMortality', 'infantdeaths', 'Alcohol', 'BMI', 'under-fivedeaths', 'Polio', 'Totalexpenditure', 'Diphtheria', 'HIV/AIDS', 'GDP', 'Population', 'thinness1-19years', 'thinness5-9years', 'Incomecompositionofresources', 'Schooling']]
y = numeric_data['Lifeexpectancy']


# X는 입력 특성, y는 예측할 타겟 변수
# test_size는 테스트 데이터의 비율을 나타냄 (여기서는 20%)
# random_state는 난수 생성 시드로, 같은 시드를 사용하면 항상 같은 결과가 나옴
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# n_estimators는 생성할 트리의 개수를 나타냄
# random_state는 난수 생성 시드로, 같은 시드를 사용하면 항상 같은 결과가 나옴
model = RandomForestRegressor(n_estimators=100, random_state=42)
# 훈련 데이터를 사용하여 모델을 훈련
model.fit(X_train, y_train)
# 모델 저장
joblib.dump(model, 'life_expectancy_model.joblib')

# 모델 불러오기
loaded_model = joblib.load('life_expectancy_model.joblib')


# # 실제값과 예측값 시각화
# plt.scatter(y_test, y_pred, label='실제 vs 예측')
# plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], '--', color='red', label='예상 라인')
# plt.xlabel("실제 Life Expectancy")
# plt.ylabel("예측 Life Expectancy")
# plt.title("실제값 vs 예측값")
# plt.legend()
# plt.show()

# 예측할 때도 동일한 순서와 이름의 특성을 사용
new_data_example = pd.DataFrame({
    'AdultMortality': [np.random.randint(20, 100)],
    'infantdeaths': [np.random.randint(0, 50)],
    'Alcohol': [np.random.uniform(0, 20)],
    'BMI': [np.random.uniform(10, 40)],
    'under-fivedeaths': [np.random.randint(0, 30)],
    'Polio': [np.random.uniform(20, 100)],
    'Totalexpenditure': [np.random.uniform(0, 20)],
    'Diphtheria': [np.random.uniform(20, 100)],
    'HIV/AIDS': [np.random.uniform(0, 10)],
    'GDP': [np.random.uniform(0, 20000)],
    'Population': [np.random.uniform(0, 2000000000)],
    'thinness1-19years': [np.random.uniform(0, 30)],
    'thinness5-9years': [np.random.uniform(0, 30)],
    'Incomecompositionofresources': [np.random.uniform(0, 1)],
    'Schooling': [np.random.uniform(0, 20)]
})


# 새로운 데이터에 대한 예측 수행
new_data_predictions = loaded_model.predict(new_data_example)

# 예측 결과 출력
print("Life Expectancy Predictions for the New Data:")
print(new_data_predictions)


# # 연도를 나타내는 정수형 열
# 'Year': int64,
# # 기대 수명을 나타내는 부동소수점형 열
# 'Life expectancy': float64,
# # 성인 사망률을 나타내는 부동소수점형 열
# 'Adult Mortality': float64,
# # 영아 사망 수를 나타내는 정수형 열
# 'infant deaths': int64,
# # 알콜 소비량을 나타내는 부동소수점형 열
# 'Alcohol': float64,
# # 백분율 지출을 나타내는 부동소수점형 열
# 'percentage expenditure': float64,
# # B형 간염 예방 접종률을 나타내는 부동소수점형 열
# 'Hepatitis B': float64,
# # 홍역 발병 건수를 나타내는 정수형 열
# 'Measles': int64,
# # 체질량 지수(BMI)를 나타내는 부동소수점형 열
# 'BMI': float64,
# # 5세 미만 사망 수를 나타내는 정수형 열
# 'under-five deaths': int64,
# # 소아마비 예방 접종률을 나타내는 부동소수점형 열
# 'Polio': float64,
# # 총 의료비 지출을 나타내는 부동소수점형 열
# 'Total expenditure': float64,
# # 디프테리아 예방 접종률을 나타내는 부동소수점형 열
# 'Diphtheria': float64,
# # HIV/AIDS 감염률을 나타내는 부동소수점형 열
# 'HIV/AIDS': float64,
# # 국내총생산(GDP)을 나타내는 부동소수점형 열
# 'GDP': float64,
# # 인구 수를 나타내는 부동소수점형 열
# 'Population': float64,
# # 1-19세의 고립도 정도를 나타내는 부동소수점형 열
# 'thinness  1-19 years': float64,
# # 5-9세의 고립도 정도를 나타내는 부동소수점형 열
# 'thinness 5-9 years': float64,
# # 자원 구성 비율을 나타내는 부동소수점형 열
# 'Income composition of resources': float64,
# # 교육 수준을 나타내는 부동소수점형 열
# 'Schooling': float64


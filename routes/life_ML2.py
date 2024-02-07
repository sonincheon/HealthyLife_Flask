import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
# 파일가져오기
data = pd.read_csv('../data/life_expectancy_data.csv', sep=',', encoding='utf-8')

# 숫자형 열만 선택
numeric_data = data.select_dtypes(include=['number'])

# 결측치 처리
numeric_data = numeric_data.fillna(numeric_data.median())

# 특성과 타겟 나누기
X = numeric_data[['AdultMortality', 'BMI']]
y = numeric_data['Lifeexpectancy']

# 학습 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 생성 및 학습
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 모델 저장
joblib.dump(model, 'life_expectancy_model.joblib1')
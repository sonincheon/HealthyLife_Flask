from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app, origins=['*'])

# 모델 불러오기
loaded_model = joblib.load('./routes/life_expectancy_model.joblib1')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 클라이언트로부터 JSON 형식의 데이터를 받음
        data = request.get_json()
        print(data)

        # 받은 데이터를 DataFrame으로 변환
        try:
            new_data = pd.DataFrame(data, index=[0])  # 인덱스를 [0]으로 지정
            print("DataFrame from JSON:", new_data)
        except Exception as e:
            print("Error creating DataFrame:", str(e))

        # 특성 선택: AdultMortality와 BMI만 사용
        new_data = new_data[['AdultMortality', 'BMI']]
        print(new_data)

        # 모델로 예측
        predictions = loaded_model.predict(new_data)

        # 예측 결과를 JSON 형식으로 반환
        response = {'predictions': predictions.tolist()}
        return jsonify(response)

    except Exception as e:
        # 예외가 발생하면 에러 메시지 반환
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

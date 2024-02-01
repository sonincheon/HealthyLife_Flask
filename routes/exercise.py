import mysql.connector
import requests
from bs4 import BeautifulSoup as bs
import re

# MySQL 연결 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'khb3187923!',
    'database': 'test3'
}

# MySQL 연결
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# food 테이블에서 모든 음식의 name 가져오기
query = "SELECT name FROM exercise_tb"
cursor.execute(query)
exercises = cursor.fetchall()

# 각 음식에 대한 이미지 URL 추출
for exercise in exercises:
    name = exercise[0]
    url = f'https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q={name}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    html_text = response.text
    soup = bs(html_text, 'html.parser')

    image_url_match = re.search(r'url:\s*"(https://[^"]+)"', str(soup))

    if image_url_match:
        image_url = image_url_match.group(1)
        print(f"{name}: {image_url}")

        # 이미지 URL을 해당하는 name에 맞춰 업데이트
        update_query = "UPDATE exercise_tb SET image = %s WHERE name = %s"
        update_data = (image_url, name)
        cursor.execute(update_query, update_data)
        conn.commit()

        print(f"{name}: 이미지 URL을 업데이트하였습니다.")
    else:
        print(f"{name}: 이미지 URL을 찾을 수 없습니다.")

# 연결 종료
cursor.close()
conn.close()

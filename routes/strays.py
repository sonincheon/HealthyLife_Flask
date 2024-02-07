import json
import requests
from bs4 import BeautifulSoup
import time


def parsing_healthy_medicines(key_word=None):
    start = time.time()
    base_url = "https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }
    int_page = 1
    medicine_list = []
    print("크롤링 시작 ! ! ! ! !")
    while True:
        for attempt in range(3):
            try:
                res = requests.get(f"{base_url}+{key_word}", headers=headers)
                print(res)
                res.raise_for_status()
                break
            except requests.RequestException as e:
                print(f"네트워크 오류 (페이지 {int_page}, 시도 {attempt + 1}): {e}")
                if attempt == 2:  # 마지막 시도에서도 실패한 경우
                    print(f"페이지 {int_page}에 대한 모든 재시도 실패. 크롤링을 계속합니다.")
                    int_page += 1
                    continue
                time.sleep(5)  # 재시도 간 간단한 지연
        soup = BeautifulSoup(res.text, 'html.parser')
        print(soup)
        no_content = soup.find('div', string=lambda text: text and '검색결과가 없습니다.' in text)

        if no_content:
            print("페이지 끝까지 순회완료.")
            print("문자열 가공 함수 실행중...")
            print("크롤링 종료.")
            break

        div_items = soup.find_all('div', class_='items')
        print(div_items)
        print(f"{int_page}페이지 접근완료")
        for div in div_items:
            title = div.find('div', class_='title').get_text(strip=True) if div.find('div', class_='title') else None
            functionality = div.find('div', class_='functionality').get_text(strip=True) if div.find('div',
                                                                                                     class_='functionality') else None
            company = div.find('div', class_='company').get_text(strip=True) if div.find('div',
                                                                                         class_='company') else None

            medicine_list.append({'title': title, 'functionality': functionality, 'company': company})

        int_page += 1

    end = time.time()
    print(f"크롤링 시간: {end - start}초")

    for medicine_data in medicine_list:
        print(medicine_data)

    json_medicines = json.dumps(medicine_list, ensure_ascii=False, indent=5)
    return json_medicines


# 사용 예시
result = parsing_healthy_medicines()
for data in result:
    print(data)

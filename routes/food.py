import requests
from bs4 import BeautifulSoup as bs
import re

# step3. 입력받은 query가 포함된 url 주소(네이버 뉴스 검색 결과 페이지) 저장
url = 'https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q=감자튀김'

# step4. requests 패키지를 이용해 'url'의 html 문서 가져오기
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)

html_text = response.text

# step5. beautifulsoup 패키지로 파싱 후, 'soup' 변수에 저장
soup = bs(html_text, 'html.parser')

# 정규 표현식을 사용하여 이미지 URL 추출
image_url_match = re.search(r'url:\s*"(https://[^"]+)"', str(soup))

if image_url_match:
    image_url = image_url_match.group(1)
    print(image_url)
else:
    print("이미지 URL을 찾을 수 없습니다.")
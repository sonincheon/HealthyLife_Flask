import json
import time

from googletrans import Translator
import mysql.connector

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

# Google Translate 객체 생성
translator = Translator()

cache_file = 'translation_cache.json'

# 캐시 로드
try:
    with open(cache_file, 'r') as f:
        translation_cache = json.load(f)
except FileNotFoundError:
    translation_cache = {}

translator.raise_Exception = True
translator.raise_exception = True


# exercise_tb에서 모든 운동 정보 가져오기
query = "SELECT * FROM exercise_tb"
cursor.execute(query)
exercises = cursor.fetchall()

# 각 운동 정보를 번역하여 업데이트
for exercise in exercises:
    # 번역 대상 열: name, description 등
    exercise_exercise_id = exercise[0]
    exercise_difficulty_en = exercise[1]  # 영어로 된 운동 난이도
    exercise_equipment_en = exercise[2]  # 영어로 된 운동 장비
    exercise_instructions_en = exercise[4]  # 영어로 된 운동 설명
    exercise_muscle_en = exercise[5]  # 영어로 된 운동 부위
    exercise_name_en = exercise[6]  # 영어로 된 운동 이름
    exercise_type_en = exercise[7]  # 영어로 된 운동 종류


    if exercise_instructions_en is None:
        translated_instructions = None
    else:
        translated_instructions = translator.translate(exercise_instructions_en, dest='ko').text

    time.sleep(0.5)

    if exercise_difficulty_en == 'beginner':
        translated_difficulty = '초급자'
    elif exercise_difficulty_en == 'intermediate':
        translated_difficulty = '중급자'
    elif exercise_difficulty_en == 'expert':
        translated_difficulty = '상급자'
    elif exercise_difficulty_en is None:
        translated_difficulty = None
    else:
        translated_difficulty = exercise_difficulty_en

    if exercise_type_en == 'cardio':
        translated_type = '유산소'
    elif exercise_type_en == 'olympic_weightlifting':
        translated_type = '올림픽_역도'
    elif exercise_type_en == 'plyometrics':
        translated_type = '플라이오메트릭'
    elif exercise_type_en == 'powerlifting':
        translated_type = '파워리프팅'
    elif exercise_type_en == 'strength':
        translated_type = '근력'
    elif exercise_type_en == 'stretching':
        translated_type = '스트레칭'
    elif exercise_type_en == 'strongman':
        translated_type = '스트롱맨'
    elif exercise_type_en == 'strength':
        translated_type = '근력'
    elif exercise_type_en is None:
        translated_type = None
    else:
        translated_type = exercise_type_en

    if exercise_equipment_en == 'body_only':
        translated_equipment = '맨몸운동'
    elif exercise_equipment_en == 'kettlebells':
        translated_equipment = '케틀벨'
    elif exercise_equipment_en == 'None':
        translated_equipment = '없음'
    elif exercise_equipment_en == 'barbell':
        translated_equipment = '바벨'
    elif exercise_equipment_en == 'dumbbell':
        translated_equipment = '덤벨'
    elif exercise_equipment_en == 'other':
        translated_equipment = '기타'
    elif exercise_equipment_en == 'machine':
        translated_equipment = '머신'
    elif exercise_equipment_en == 'cable':
        translated_equipment = '케이블'
    elif exercise_equipment_en == 'e-z_curl_bar':
        translated_equipment = '이지컬바'
    elif exercise_equipment_en is None:
        translated_equipment = None
    else:
        translated_equipment = exercise_equipment_en

    if exercise_muscle_en == 'abdominals':
        translated_muscle = '복근'
    elif exercise_muscle_en == 'abductors':
        translated_muscle = '외전근'
    elif exercise_muscle_en == 'adductors':
        translated_muscle = '내전근'
    elif exercise_muscle_en == 'biceps':
        translated_muscle = '이두근'
    elif exercise_muscle_en == 'calves':
        translated_muscle = '종아리'
    elif exercise_muscle_en == 'chest':
        translated_muscle = '가슴'
    elif exercise_muscle_en == 'glutes':
        translated_muscle = '엉덩이'
    elif exercise_muscle_en == 'hamstrings':
        translated_muscle = '햄스트링'
    elif exercise_muscle_en == 'lats':
        translated_muscle = '광배근'
    elif exercise_muscle_en == 'lower_back':
        translated_muscle = '허리'
    elif exercise_muscle_en == 'middle_back':
        translated_muscle = '등'
    elif exercise_muscle_en == 'neck':
        translated_muscle = '목'
    elif exercise_muscle_en == 'quadriceps':
        translated_muscle = '대퇴사두근'
    elif exercise_muscle_en == 'traps':
        translated_muscle = '승모근'
    elif exercise_muscle_en == 'triceps':
        translated_muscle = '삼두근'
    elif exercise_muscle_en == 'forearms':
        translated_muscle = '팔뚝'
    elif exercise_muscle_en == 'shoulders':
        translated_muscle = '어깨'
    elif exercise_muscle_en is None:
        translated_muscle = None
    else:
        translated_muscle = exercise_muscle_en

    # 번역된 결과를 데이터베이스에 업데이트
    update_query = "UPDATE exercise_tb SET difficulty = %s, instructions = %s, equipment = %s, muscle = %s, type = %s WHERE exercise_id = %s"
    update_data = (translated_difficulty, translated_instructions, translated_equipment, translated_muscle, translated_type, exercise_exercise_id)
    cursor.execute(update_query, update_data)
    conn.commit()

    print(f"운동 ID {exercise_name_en} 번역 완료")

# 캐시 파일 업데이트
with open(cache_file, 'w') as f:
    json.dump(translation_cache, f)

# 연결 종료
cursor.close()
conn.close()

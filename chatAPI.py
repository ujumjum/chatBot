# import sqlite3 DB
import openai
import os

from datetime import datetime


# model, key 받아오는 부분
class OpenAI_Client:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def chat_completion(self, model, messages, max_tokens):
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        
# 사용자 채팅 - 일상생활 대화:0, 식단평가 문의:1로 분류
binary_model = 'ft:gpt-3.5-turbo-1106:personal::8dab18BV'
# settings.py, secrets.json .gitignore 사용 키보관
API_KEY1 = settings.API_KEY1
key1 = OpenAI_Client(API_KEY1)

# 대화 이진 분류 -> 결과 반환 함수 
def chatGPT(inputText, key1):
    response = key1.chaht_completion(
        model = binary_model,
        messages = [
            {"role": "system", "content": "너는 식단을 평가해주는 챗봇이야"},
            {"role": "user", "content": inputText},
        ],
        max_tokens = 150,
    )
    
    # 0또는 1로 분류된 결과
    result = response["choices"][0]["message"]["content"]
    
    # dummy DB
    example = """date	carbs	protein	fat	sugar	result
      2023-12-27  100 80 48 88 bad
      2023-12-26	100	10	450	20	good
      2023-12-25	300	100	100	10	normal
      2023-12-20	300	100	400	50	not bad
      2023-12-22	40	100	124	123	perfect장ㄱ
      2023-12-03	120	300	40	25	perfect
      2023-12-15	90	800	400	50	bad"""
    
    today = datetime.now()
      
    # 식단 평가 대화 : 1
    if result == 1:
        # 사용자 식단 DB 정보
        # user_diet_info = fetch_diet_db('2023-12-03')
        # diet_response = create_diet_prompt(user_diet_info)
        # return diet_response
        diet_response = key1.chat_completion(
        model = 'gpt-4',
        messages = [
            {"role": "system", "content": "너는 max_tokens가 있어도 문장을 뚝 끊지 않고 자연스럽게 마무리해주는 식단 평가 결과 분석 챗봇이야."},
            {"role": "user", "content": inputText},
            # 사용자의 채팅에서 날짜 추출 assistant
            {"role":"assistant",
            "content": f"너는 식단 평가 결과를 궁금해 하는 사용자와 대화하는 친절한 결과 분석 챗봇이야. 사용자의 데이터는 {user_meals} 이걸 참고해줘. 날짜, 탄수화물, 당, 단백질, 지방, 식단 평가 결과, 총칼로리가 포함되어 있다. 
            오늘은 {today.strftime('%Y-%m-%d')}이다.  사용자 입력 문장에서 (어제, 하루 전, 1일전, 하루전, 이틀 전, 이틀전, 2일전, 2일 전, 그저께, 엊그제, 엊그저께, 3일전, 3일 전, 일주일전, 일주일 전, 저번 주) 등을 포착해서 사용자가 요구하는 날짜가 출력하고 해당 날짜의 식단 평가 결과를 분석해줘. 
            문장 속에서 날짜를 찾을 수 없다면 '구체적인 날짜를 입력해주세요' 출력하고, 특정 날짜의 정보가 존재하지 않으면 ''특정 날짜'의 식단 정보가 존재하지 않습니다'라고 출력해줘."},
        ],
        # 최대 토큰 수 제한
        max_tokens = 300,
        )
        # 식단 평가 분석 질문에 대한 답변
        diet_result = diet_response["choices"][0]["message"]["content"]
        # diet_result를 front에 전달
        return diet_result
    
    # 3. 일상 생활 대화 : 0
    else:
        daily_response = key1.chat_completion(
        model = 'gpt-4',
        messages = [
            {"role": "system", "content": "너는 max_tokens가 있어도 문장을 뚝 끊지 않고 마무리해주는 사용자 맞춤형 챗봇이야."},
            {"role": "user", "content": inputText},
        ],
        # 최대 토큰 수 제한
        max_tokens = 150,
        )
        # 일상 대화에 대한 답변
        daily_result = daily_response["choices"][0]["message"]["content"]
        # daily_result 반환
        return daily_result

# TEST : 실제 앱에서는 inputText 사용자한테 받아와서 동작
inputText = input("질문을 입력하세요: ")

# chatGPT 함수를 사용하여 결과 얻기
result = chatGPT(inputText, key1)

# 결과 출력 : 실제 앱에서는 사용자한테 보냄
print("결과:", result)

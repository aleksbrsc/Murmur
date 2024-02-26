import pyperclip
import requests
import json
import time

with open('key.txt', 'r') as file:
    API_KEY = file.read().strip()
API_URL = 'https://api.openai.com/v1/chat/completions'

GPT_3_5_TURBO_MODEL = 'gpt-3.5-turbo-1106'
GPT_4_MODEL = 'gpt-4'
GPT_4_TURBO_PREVIEW_MODEL = 'gpt-4-turbo-preview'
GPT_MODEL = GPT_3_5_TURBO_MODEL

BRIEF_PROMPT = "give a super brief answer to this question:"
DEPTH_PROMPT = "give a detailed answer to this complex question:"

def send_to_chatgpt(question):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'model': GPT_MODEL,
        'messages': [
            {
                'role': 'user',
                'content': BRIEF_PROMPT + question
            }
        ]
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response_json = response.json()
    return response_json['choices'][0]['message']['content']

def check_clipboard():
        previous_text = pyperclip.paste()
        response_copied = False
        while True:
            current_text = pyperclip.paste()
            if current_text != previous_text and not response_copied:
                if current_text is not None:
                    if len(current_text) == 1:
                        if current_text == '3':
                            GPT_MODEL = GPT_3_5_TURBO_MODEL
                            print("now using GPT-3.5-turbo-1106")
                            pyperclip.copy("disabled")
                        elif current_text == '4':
                            GPT_MODEL = GPT_4_MODEL
                            print("now using GPT-4")
                            pyperclip.copy("disabled")
                        elif current_text == '5':
                            GPT_MODEL = GPT_4_TURBO_PREVIEW_MODEL
                            print("now using GPT-4-turbo-preview")
                            pyperclip.copy("disabled")
                        else:
                            print("clipboard disabled for 5 seconds")
                            time.sleep(5)
                            print("clipboard enabled")
                            pyperclip.copy("disabled")
                    elif current_text != "disabled":
                        response = send_to_chatgpt(current_text)
                        pyperclip.copy(response)
                        response_copied = True
            elif current_text == previous_text:
                response_copied = False
            previous_text = current_text

check_clipboard()
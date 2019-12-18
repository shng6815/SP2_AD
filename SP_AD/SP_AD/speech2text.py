import sys
import requests
from ast import literal_eval
client_id = "1qyp1wma23"
client_secret = "qbkttReoCLucEZMb5ifW5od4JrhBTb8tRCc0zOgz"
lang = "Kor" # 언어 코드 ( Kor, Jpn, Eng, Chn )
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

def sp2te():
    data = open('output.wav', 'rb')
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url, data=data, headers=headers)
    rescode = response.status_code
    if (rescode == 200):
        print(response.text)
    else:
        print("Error : " + response.text)
    dictionary = literal_eval(response.text)
    return dictionary['text']
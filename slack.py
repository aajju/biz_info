import requests
import json
import config


def send_message(message):

    webhook_url = config.SLACK_WEBHOOK_PROJECT_URL

    payload = {"text": message}
    headers = {"Content-type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("메시지가 성공적으로 전송되었습니다.")
    else:
        print("메시지 전송 실패. 오류 코드:", response.status_code)

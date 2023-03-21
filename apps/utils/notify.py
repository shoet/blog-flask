import requests


def slack_post(bot_token, channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {bot_token}"}
    data  = {
        'channel': channel,
        'text': message,
    }
    result = requests.post(url, headers=headers, data=data)
    if '' in result.json():
        raise Exception('failed SlackPost()')

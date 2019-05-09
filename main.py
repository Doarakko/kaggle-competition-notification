import os
import json
import datetime
import requests
from logging import StreamHandler, INFO, DEBUG, Formatter, FileHandler, getLogger

# import dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

# dotenv.load_dotenv('.env')
POST = os.environ['POST']

if POST == 'slack':
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
elif POST == 'line':
    LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']

logger = getLogger(__name__)
log_fmt = Formatter(
    '%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)s] %(message)s')
# info
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(log_fmt)
logger.addHandler(handler)
logger.setLevel(INFO)
# debug
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(log_fmt)
logger.addHandler(handler)
logger.setLevel(DEBUG)


def get_new_competitions_list():
    try:
        api = KaggleApi()
        api.authenticate()

        competitions_list = []
        for info in api.competitions_list():
            start_date = getattr(info, 'enabledDate')

            # assume to run once a day
            pre_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)

            if start_date >= pre_date:
                competitions_list.append(info)
        return competitions_list
    except Exception as e:
        logger.error(e)


def post_slack(info):
    title = getattr(info, 'title')
    value = getattr(info, 'url')

    payload = {
        'username': 'Kaggle Competition Notification',
        'icon_url': 'https://avatars0.githubusercontent.com/u/1336944',
        'attachments': [{
            'fallback': 'New competition launch',
            'color': '#D00000',
            'fields': [{
                'title': title,
                'value': value,
            }]
        }]
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
        logger.debug('Post Slack')
    except Exception as e:
        logger.error(e)


def post_line(info):
    message = '\n{}\n{}'.format(getattr(info, 'title'), getattr(info, 'url'))

    headers = {
        'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN
    }
    payload = {
        'message': message
    }

    try:
        requests.post('https://notify-api.line.me/api/notify',
                      data=payload, headers=headers)
        logger.debug('Post LINE')
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    competitions_list = get_new_competitions_list()

    for competition in competitions_list:
        if POST == 'slack':
            post_slack(competition)
        elif POST == 'line':
            post_line(competition)

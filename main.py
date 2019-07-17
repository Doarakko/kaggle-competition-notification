import os
import json
import datetime
import requests
from logging import StreamHandler, INFO, DEBUG, Formatter, FileHandler, getLogger

# import dotenv
from kaggle import KaggleApi


DO_NOT_NOTIFY = 'Do not notify this competition'
NEW_COMPETITION = 'New kaggle competition is launched'

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


# Plan to create reminder
class Competition:
    def __init__(self, info):
        self.title = getattr(info, 'title')
        self.url = getattr(info, 'url')
        self.start_date = getattr(info, 'enabledDate')
        self.end_date = getattr(info, 'deadline')
        self.user_enter = getattr(info, 'userHasEntered')

        # assume to run once every 10 minutes
        now = datetime.datetime.utcnow()
        if self.start_date >= now - datetime.timedelta(minutes=10):
            self.notify_message = NEW_COMPETITION
        else:
            self.notify_message = DO_NOT_NOTIFY


def get_notify_competitions_list():
    try:
        api = KaggleApi()
        api.authenticate()

        competitions_list = []
        for info in api.competitions_list(sort_by='recentlyCreated'):
            competition = Competition(info)
            
            if competition.notify_message != DO_NOT_NOTIFY:
                competitions_list.append(competition)

        return competitions_list
    except Exception as e:
        logger.error(e)


def post_slack(competition):
    title = competition.notify_message
    value = '{}\n{}'.format(competition.title, competition.url)

    payload = {
        'username': 'Kaggle Competition Notification',
        'icon_url': 'https://avatars0.githubusercontent.com/u/1336944',
        'attachments': [{
            'fallback': competition.notify_message,
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


def post_line(competition):
    message = '\n{}\n{}\n{}'.format(
        competition.notify_message, competition.title, competition.url)

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
    competitions_list = get_notify_competitions_list()
    
    if competitions_list is not None:
        for competition in competitions_list:
            if POST == 'slack':
                post_slack(competition)
            elif POST == 'line':
                post_line(competition)
            else:
                logger.error('POST is invalid')

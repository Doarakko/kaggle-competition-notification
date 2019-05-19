import os
import json
import datetime
import requests
from logging import StreamHandler, INFO, DEBUG, Formatter, FileHandler, getLogger

# import dotenv
from kaggle import KaggleApi


DO_NOT_NOTIFY = 'Do not notify this competition'
NEW_COMPETITION = 'New competition is launched'
ONE_MONTH_BEFORE = '1 month before the end of this competition'
ONE_WEEK_BEFORE = '1 week before the end of this competition'
THREE_DAYS_BEFORE = '3 days before the end of this competition'
ONE_DAY_BEFORE = '1 day before the end of this competition'
ONE_DAY = 1
THREE_DAYS = 3
ONE_WEEK = 7
ONE_MONTH = 30

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


class Competition:
    def __init__(self, info):
        self.title = getattr(info, 'title')
        self.url = getattr(info, 'url')
        self.start_date = getattr(info, 'enabledDate')
        self.end_date = getattr(info, 'deadline')
        self.user_enter = getattr(info, 'userHasEntered')

        # assume to run once a day
        now = datetime.datetime.utcnow()
        if self.start_date >= now - datetime.timedelta(days=ONE_DAY):
            self.notify_message = NEW_COMPETITION

        elif self.end_date <= now + datetime.timedelta(days=ONE_DAY):
            self.notify_message = ONE_DAY_BEFORE

        elif self.end_date <= now + datetime.timedelta(days=THREE_DAYS) and self.end_date >= now + datetime.timedelta(days=THREE_DAYS-1):
            self.notify_message = THREE_DAYS_BEFORE

        elif self.end_date <= now + datetime.timedelta(days=ONE_WEEK) and self.end_date >= now + datetime.timedelta(days=ONE_WEEK-1):
            self.notify_message = ONE_WEEK_BEFORE

        elif self.end_date <= now + datetime.timedelta(days=ONE_MONTH) and self.end_date >= now + datetime.timedelta(days=ONE_MONTH-1):
            self.notify_message = ONE_MONTH_BEFORE

        else:
            self.notify_message = DO_NOT_NOTIFY


def get_notify_competitions_list():
    try:
        api = KaggleApi()
        api.authenticate()

        competitions_list = []
        for info in api.competitions_list():
            competition = Competition(info)

            if competition.user_enter and competition.notify_message != DO_NOT_NOTIFY:
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

    for competition in competitions_list:
        if POST == 'slack':
            post_slack(competition)
        elif POST == 'line':
            post_line(competition)
        else:
            logger.error('POST(Notification destination) is invalid')

# Kaggle Competition Notification
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Notify new [kaggle](https://kaggle.com) competition to Slack or LINE without coding.

## Requirements
- Kaggle API
- Heroku
- Credit card
    - It does not take money, to sign up and deploy heroku
- [Slack](https://api.slack.com/incoming-webhooks) or [LINE](https://notify-bot.line.me)

## Usage
### 1. Press button(`Deploy to Heroku`) and enter environment variables
You need to enter your credit card information to use [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler).  
Standard plan is free, so please don't worry.

![](img/enter-config-vars.png)

### 2. Set task on Heroku
![](img/select-scheduler.png)

Set `Schedule` with `Every 10 minutes`.

![](img/set-schedule.png)

```
# assume to run once every 10 minutes
now = datetime.datetime.utcnow()
if self.start_date >= now - datetime.timedelta(minutes=10):
    self.notify_message = NEW_COMPETITION
else:
    self.notify_message = DO_NOT_NOTIFY
```

## Sample
- Slack

![](img/slack-sample.png)

- LINE

![](img/line-sample.png)

## Contribution
Welcome issue and pull request.

## License
MIT

## Author
Doarakko
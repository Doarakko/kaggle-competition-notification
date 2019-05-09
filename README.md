# Kaggle Competition Notification
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Notify new competition to Slack or LINE using Kaggle API and Heroku.

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

Set `FREQUENCY` with `Daily`.

![](img/set-schedule.png)


```
# assume to run once a day
pre_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
```

If you get at short intervals, please fork and correct the program.

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
# !/usr/bin/env python
# coding=utf-8
# by hython.com

import os
import time
from datetime import datetime
import functools
import schedule
import pymsteams


MYTIM_LINK = os.environ.get("MYTIM_LINK")
ACCESS_KEY = os.environ.get("ACCESS_KEY")


class MsgContent:
    content_10 = "🐶 出勤打刻、忘れていませんか"
    content_17 = "🐵 残業申請なら、今でしょう！"


# Logging decorator can be applied to
def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        return result
    return wrapper


@with_logging
def push_mytim_msg(msg):
    """
    push alert msg to teams
    """
    content = msg
    message = pymsteams.connectorcard(ACCESS_KEY)
    message.http_timeout = 100
    message.title("打刻アラーム🕑")
    message.text(content)
    message.color('#FF0000')
    message.addLinkButton("👉こちら", MYTIM_LINK)
    try:
        message.send()
    except Exception as e:
        pass


def weekday_job(x, msg, t=None):
    week = datetime.today().weekday()
    if t is not None and week < 5:
        schedule.every().day.at(t).do(x, msg=msg)


def schedule_set():
    weekday_job(push_mytim_msg, MsgContent.content_10, '10:00')
    weekday_job(push_mytim_msg, MsgContent.content_17, '17:30')


def main():
    schedule_set()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

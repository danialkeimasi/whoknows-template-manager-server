import os
import time
import schedule

from modules.command_line_interface import app
from config import SETTINGS


def reload():
    app.test_client().post('/dataset/load', json={})


if not os.path.isdir(SETTINGS.dir.dataset):
    reload()


def run_schedule():
    print('data reload is activated!')
    while True:
        schedule.run_pending()
        time.sleep(1)
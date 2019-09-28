import os
import time

import schedule

from config import SETTINGS
from modules.command_line_interface import cli, app


if not os.path.isdir(SETTINGS.dir.dataset):
    app.test_client().post('/dataset/load', json={})


def reload():
    app.test_client().post('/dataset/load', json={})


schedule.every(SETTINGS.reload_period).minutes.do(reload)


if __name__ == "__main__":
    cli()

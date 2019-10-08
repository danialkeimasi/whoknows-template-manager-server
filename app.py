from threading import Thread

import schedule
import modules.data_reload

from modules.command_line_interface import cli, app
from config import SETTINGS


if SETTINGS.data_reload:
    schedule.every(SETTINGS.reload_period).minutes.do(modules.data_reload.reload)
    t = Thread(target=modules.data_reload.run_schedule)
    t.start()


if __name__ == "__main__":
    cli()

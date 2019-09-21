import os

from config import SETTINGS
from modules.command_line_interface import cli, app


if not os.path.isdir(SETTINGS.dir.dataset):
    app.test_client().post('/dataset/load', json={})


if __name__ == "__main__":
    cli()

import os

from modules.command_line_interface import cli, app

if not os.path.isdir('datasets/'):
    app.test_client().post('/dataset/load', json={})

if __name__ == "__main__":
    cli()

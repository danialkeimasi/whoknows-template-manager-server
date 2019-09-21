from modules.command_line_interface import cli, app

app.test_client().post('/dataset/load', json={})

if __name__ == "__main__":
    cli()

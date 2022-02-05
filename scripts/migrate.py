
from tool_kit.external import Database

import typer

app = typer.Typer()


@app.command()
def curriculum():
    typer.echo('Starting curriculum migration...')


if __name__ == '__main__':
    app()

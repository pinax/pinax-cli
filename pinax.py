import json

from pip.commands import install

import click
import requests


class Config(object):
    def __init__(self):
        self.url = "https://gist.githubusercontent.com/paltman/32c6e4c3a4abd61a5751/raw/65fa0cbffc3ce9822133d01086cb3ac304c1ba33/projects.json"


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--url", type=str, required=False, help="url to project data source")
@pass_config
def main(config, url):
    if url:
        config.url = url


@main.command()
@click.option("--start", type=str, required=False, help="kind of project to start")
@click.argument("name", type=str, default="", required=False)
@pass_config
def projects(config, start, name):
    """
    List available projects to start
    """
    projects = requests.get(config.url).json()
    if start and name:
        url = projects[start]["url"]
        startprojectargs = projects[start]["args"]
        command = install.InstallCommand()
        opts, args = command.parser.parse_args([])
        click.echo("Installing Django...")
        command.run(opts, ["Django"])
        from django.core.management import call_command
        click.echo("Starting {} project from Pinax".format(start))
        call_command("startproject", name, startprojectargs, template=url)
        click.echo("Finished")
        click.echo("""You now should:

1. cd {}
2. pip install -r requirements.txt
3. chmod +x manage.py
4. ./manage.py migrate
5. ./manage.py runserver
""")
    else:
        for project in projects:
            click.echo(project)

import json
import os
import shutil

from pip.commands import install

import click
import requests


class Config(object):
    def __init__(self):
        self.url = "https://gist.githubusercontent.com/paltman/32c6e4c3a4abd61a5751/raw/b1c344175a5f2ba827f7b930032c649553826746/projects.json"


pass_config = click.make_pass_decorator(Config, ensure=True)



def pip_install(package):
    command = install.InstallCommand()
    opts, args = command.parser.parse_args([])
    click.echo("Installing {}...".format(package))
    command.run(opts, [package])


def start_project(project, name):
    from django.core.management import call_command
    click.echo("Starting project from Pinax")
    kwargs = dict(
        template=project["template"],
        files=project["files"]
    )
    call_command("startproject", name, **kwargs)


def output_instructions(project, name):
    if "instructions" in project:
        click.echo(project["instructions"])


def cleanup(name):
    # @@@ Should this be indicated in the project dict instead of hard coded?
    os.remove(os.path.join(name, "LICENSE"))
    os.remove(os.path.join(name, "CONTRIBUTING.md"))
    os.remove(os.path.join(name, "README.md"))
    shutil.move(os.path.join(name, "PROJECT_README.md"), os.path.join(name, "README.md"))


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
        pip_install("Django")
        start_project(projects[start], name)
        click.echo("Finished")
        output_instructions(projects[start], name)
        cleanup(name)
    else:
        for project in projects:
            click.echo(project)

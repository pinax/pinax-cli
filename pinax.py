import json
import os
import shutil

from pip.commands import install

import click
import requests


class Config(object):
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/pinax/pinax/master/projects.json"


pass_config = click.make_pass_decorator(Config, ensure=True)



def pip_install(package):
    command = install.InstallCommand()
    opts, args = command.parser.parse_args([])
    click.echo("Installing {}...".format(package))
    command.run(opts, [package])


def start_project(project, name, dev):
    from django.core.management import call_command
    click.echo("Starting project from Pinax")
    template = project["url"] if dev else max(project["releases"])
    kwargs = dict(
        template=template,
        files=project["process-files"]
    )
    call_command("startproject", name, **kwargs)


def output_instructions(project, name):
    if "instructions" in project:
        click.echo(project["instructions"])


def cleanup(name):
    # @@@ Should this be indicated in the project dict instead of hard coded?
    os.remove(os.path.join(name, "LICENSE"))
    os.remove(os.path.join(name, "CONTRIBUTING.md"))


@click.group()
@click.option("--url", type=str, required=False, help="url to project data source")
@click.version_option()
@pass_config
def main(config, url):
    if url:
        config.url = url


@main.command()
@click.option("--start", type=str, required=False, help="kind of project to start")
@click.option("--dev", is_flag=True)
@click.argument("name", type=str, default="", required=False)
@pass_config
def projects(config, start, dev, name):
    """
    List available projects to start
    """
    payload = requests.get(config.url).json()
    if payload.get("version") == 1:
        projects = payload.get("projects")
        if start and name:
            if dev or len(projects[start]["releases"]) > 0:
                pip_install("Django")
                start_project(projects[start], name, dev)
                click.echo("Finished")
                output_instructions(projects[start], name)
                cleanup(name)
            else:
                click.echo("There are no releases for {}. You need to specify the --dev flag to use.".format(start))
        else:
            click.echo("{} {}".format("Release".rjust(7), "Project"))
            click.echo("------- ---------------")
            for project in projects:
                if projects[project]["releases"]:
                    release = max([
                        x.split("/")[-1].replace(".tar.gz", "")
                        for x in projects[project]["releases"]
                    ]).split("-")[-1]
                else:
                    release = ""
                click.echo("{} {}".format(release.rjust(7), project))
    else:
        click.echo("The projects manifest you are trying to consume will not work: \n{}".format(config.url))

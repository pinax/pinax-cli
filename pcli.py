import os
import stat
import sys

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
    from django.core.management import call_command, CommandError
    click.echo("Starting project from Pinax")
    template = project["url"] if dev else max(project["releases"])
    kwargs = dict(
        template=template,
        files=project["process-files"]
    )
    try:
        call_command("startproject", name, **kwargs)
    except CommandError as e:
        click.echo(click.style("Error: ", fg="red") + str(e))
        sys.exit(1)


def output_instructions(project, name):
    if "instructions" in project:
        click.echo(project["instructions"])


def cleanup(name):
    # @@@ Should this be indicated in the project dict instead of hard coded?
    os.remove(os.path.join(name, "LICENSE"))
    os.remove(os.path.join(name, "CONTRIBUTING.md"))
    os.remove(os.path.join(name, "update.sh"))
    managepy = os.path.join(name, "manage.py")
    st = os.stat(managepy)
    os.chmod(managepy, st.st_mode | stat.S_IEXEC)


@click.group()
@click.option("--url", type=str, required=False, help="url to project data source")
@click.version_option()
@pass_config
def main(config, url):
    if url:
        config.url = url


@main.command()
@pass_config
def projects(config):
    payload = requests.get(config.url).json()
    if payload.get("version") == 1:
        projects = payload.get("projects")
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


@main.command()
@click.option("--dev", is_flag=True, help="use latest development branch instead of release")
@click.argument("project", type=str, required=True)
@click.argument("name", type=str, required=True)
@pass_config
def start(config, dev, project, name):
    payload = requests.get(config.url).json()
    if payload.get("version") == 1:
        projects = payload.get("projects")
        try:
            if dev or len(projects[project]["releases"]) > 0:
                pip_install("Django")
                start_project(projects[project], name, dev)
                click.echo("Finished")
                output_instructions(projects[project], name)
                cleanup(name)
            else:
                click.echo("There are no releases for {}. You need to specify the --dev flag to use.".format(project))
        except KeyError:
            click.echo("There are no releases for {}.".format(project))
    else:
        click.echo("The projects manifest you are trying to consume will not work: \n{}".format(config.url))

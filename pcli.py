import os
import stat
import sys

import click
import requests
from pip.commands import install


class Config(object):
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/pinax/pinax/master/projects.json"
        self.apps_url = "https://raw.githubusercontent.com/pinax/pinax/master/distributions.json"


pass_config = click.make_pass_decorator(Config, ensure=True)


def pip_install(package):
    command = install.InstallCommand()
    opts, args = command.parser.parse_args([])
    click.echo("Installing {}...".format(package))
    command.run(opts, [package])


def start_project(project, name, dev, location):
    from django.core.management import call_command, CommandError
    click.echo("Starting project from Pinax")
    template = project["url"] if dev else max(project["releases"])
    kwargs = dict(
        template=template,
        files=project["process-files"]
    )
    args = [name]
    if location:
        args.append(location)
    try:
        call_command("startproject", *args, **kwargs)
    except CommandError as e:
        click.echo(click.style("Error: ", fg="red") + str(e))
        sys.exit(1)


def output_instructions(project):
    if "instructions" in project:
        click.echo(project["instructions"])


def cleanup(name, location):
    if not location:
        # if location was not specified, start_project used `name` for new subdir
        location = name
    os.remove(os.path.join(location, "LICENSE"))
    os.remove(os.path.join(location, "CONTRIBUTING.md"))
    os.remove(os.path.join(location, "update.sh"))
    managepy = os.path.join(location, "manage.py")
    st = os.stat(managepy)
    os.chmod(managepy, st.st_mode | stat.S_IEXEC)


@click.group()
@click.option("--url", type=str, required=False, help="url to project data source")
@click.option("--apps_url", type=str, required=False, help="url to application data source")
@click.version_option()
@pass_config
def main(config, url, apps_url):
    if url:
        config.url = url
    if apps_url:
        config.apps_url = apps_url


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


def show_distribution_section(config, title, section_name):
    """
    Obtain distribution data and display latest distribution section,
    i.e. "demos" or "apps" or "themes".
    """
    payload = requests.get(config.apps_url).json()
    distributions = sorted(payload.keys(), reverse=True)
    latest_distribution = payload[distributions[0]]
    click.echo("{} {}".format("Release".rjust(7), title))
    click.echo("------- ---------------")
    section = latest_distribution[section_name]
    names = sorted(section.keys())
    for name in names:
        click.echo("{} {}".format(section[name].rjust(7), name))


@main.command()
@pass_config
def apps(config):
    show_distribution_section(config, "Application", "apps")


@main.command()
@pass_config
def demos(config):
    show_distribution_section(config, "Demo", "demos")


@main.command()
@pass_config
def themes(config):
    show_distribution_section(config, "Theme", "themes")


@main.command()
@pass_config
def tools(config):
    show_distribution_section(config, "Tool", "tools")


@main.command()
@click.option("--dev", is_flag=True, help="use latest development branch instead of release")
@click.option("--location", type=str, default="", help="specify where project is created")
@click.argument("project", type=str, required=True)
@click.argument("name", type=str, required=True)
@pass_config
def start(config, dev, location, project, name):
    payload = requests.get(config.url).json()
    if payload.get("version") == 1:
        projects = payload.get("projects")
        try:
            if dev or len(projects[project]["releases"]) > 0:
                pip_install("Django")
                start_project(projects[project], name, dev, location)
                click.echo("Finished")
                output_instructions(projects[project])
                cleanup(name, location)
            else:
                click.echo("There are no releases for {}. You need to specify the --dev flag to use.".format(project))
        except KeyError:
            click.echo("There are no releases for {}.".format(project))
    else:
        click.echo("The projects manifest you are trying to consume will not work: \n{}".format(config.url))

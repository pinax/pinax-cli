import os
import stat
import sys

import click
import django
from django.core.management import call_command, CommandError
import requests

from .utils import format_help, order_manually


class Config(object):
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/pinax/pinax/master/projects.json"
        self.apps_url = "https://raw.githubusercontent.com/pinax/pinax/master/distributions.json"


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
pass_config = click.make_pass_decorator(Config, ensure=True)


class PinaxGroup(click.Group):
    """Custom Group class with specially formatted help"""

    def list_commands(self, ctx):
        """Override for showing commands in particular order"""
        commands = super(PinaxGroup, self).list_commands(ctx)
        return [cmd for cmd in order_manually(commands)]

    def get_help_option(self, ctx):
        """Override for showing formatted main help via --help and -h options"""
        help_options = self.get_help_option_names(ctx)
        if not help_options or not self.add_help_option:
            return

        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                if not ctx.invoked_subcommand:
                    # pinax main help
                    click.echo(format_help(ctx.get_help()))
                else:
                    # pinax sub-command help
                    click.echo(ctx.get_help(), color=ctx.color)
                ctx.exit()
        return click.Option(
            help_options,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help='Show this message and exit.')


@click.group(cls=PinaxGroup, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--url", type=str, required=False, help="url to project data source")
@click.option("--apps_url", type=str, required=False, help="url to application data source")
@click.version_option()
@pass_config
@click.pass_context
def main(ctx, config, url, apps_url):
    if url:
        config.url = url
    if apps_url:
        config.apps_url = apps_url
    if ctx.invoked_subcommand is None:
        # Display help to user if no commands were passed.
        click.echo(format_help(ctx.get_help()))


@main.command(short_help="Display Pinax starter projects")
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


@main.command(short_help="Display Pinax apps")
@pass_config
def apps(config):
    show_distribution_section(config, "Application", "apps")


@main.command(short_help="Display Pinax demo projects")
@pass_config
def demos(config):
    show_distribution_section(config, "Demo", "demos")


@main.command(short_help="Display Pinax themes")
@pass_config
def themes(config):
    show_distribution_section(config, "Theme", "themes")


@main.command(short_help="Display Pinax tools")
@pass_config
def tools(config):
    show_distribution_section(config, "Tool", "tools")


@main.command(short_help="Create a new project based on a Pinax starter project")
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
                validate_django_compatible_with_python()
                start_project(projects[project], name, dev, location)
                click.echo("Finished")
                output_instructions(projects[project])
                cleanup(name, location)
            else:
                click.echo("There are no releases for {}. You need to specify the --dev flag to use.".format(project))
        except KeyError:
            click.echo("Project {} is not found.".format(project))
    else:
        click.echo("The projects manifest you are trying to consume will not work: \n{}".format(config.url))


def validate_django_compatible_with_python():
    """
    Verify Django 1.11 is present if Python 2.7 is active

    Installation of pinax-cli requires the correct version of Django for
    the active Python version. If the developer subsequently changes
    the Python version the installed Django may no longer be compatible.
    """
    python_version = sys.version[:5]
    django_version = django.get_version()
    if sys.version_info == (2, 7) and django_version >= "1.12":
        click.BadArgumentUsage("Please install Django v1.11 for Python {}, or switch to Python >= v3.4".format(python_version))


def start_project(project, name, dev, location):
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

import crayons


def order_manually(sub_commands):
    """Order sub-commands for display"""
    order = [
        "start",
        "projects",
    ]
    ordered = []
    commands = dict(zip([cmd for cmd in sub_commands], sub_commands))
    for k in order:
        ordered.append(commands.get(k, ""))
        if k in commands:
            del commands[k]

    # Add commands not present in `order` above
    for k in commands:
        ordered.append(commands[k])

    return ordered


def format_help(help):
    """Format the help string."""
    help = help.replace('Options:', str(crayons.black('Options:', bold=True)))

    help = help.replace('Usage: pinax', str('Usage: {0}'.format(crayons.black('pinax', bold=True))))

    help = help.replace('  start', str(crayons.green('  start', bold=True)))
    help = help.replace('  apps', str(crayons.yellow('  apps', bold=True)))
    help = help.replace('  demos', str(crayons.yellow('  demos', bold=True)))
    help = help.replace('  projects', str(crayons.yellow('  projects', bold=True)))
    help = help.replace('  themes', str(crayons.yellow('  themes', bold=True)))
    help = help.replace('  tools', str(crayons.yellow('  tools', bold=True)))

    additional_help = \
        """Usage Examples:
Create new project based on Pinax 'account' starter project:
$ {0}

Create new project based on development version of 'blog' starter project
$ {6}

View all Pinax starter projects:
$ {1}

View all Pinax demo projects:
$ {2}

View all Pinax apps:
$ {3}

View all Pinax tools:
$ {4}

View all Pinax themes:
$ {5}

Commands:""".format(
            crayons.red('pinax start account my_project'),
            crayons.red('pinax projects'),
            crayons.red('pinax demos'),
            crayons.red('pinax apps'),
            crayons.red('pinax tools'),
            crayons.red('pinax themes'),
            crayons.red('pinax start --dev blog my_project')
        )

    help = help.replace('Commands:', additional_help)

    return help

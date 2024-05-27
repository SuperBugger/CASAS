import click
from core import PluginManager

manager = PluginManager()
manager.load_plugins()


@click.command()
@click.argument('szi_name', type=click.Choice(manager.plugins.keys()), metavar='SZI_NAME')
@click.argument('command', type=click.Choice(['status', 'info', 'list']), metavar='COMMAND')
def cli(szi_name, command):
    """Security application CLI."""
    if command == 'list':
        click.echo("Available SZIs:")
        for szi in manager.plugins.keys():
            click.echo(szi)
    else:
        result = manager.run_plugin(szi_name, command)
        click.echo(result)

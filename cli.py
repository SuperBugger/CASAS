import click
from core import PluginManager
import json as json_module

manager = PluginManager()
manager.load_plugins()


@click.group()
def cli():
    """Security application CLI."""
    pass


@cli.command(name='list')
def list_szis():
    """List all available SZIs."""
    click.echo("Available SZIs:")
    for key in manager.plugins.keys():
        click.echo(key)


def create_szi_command(szi_name):
    @click.command(name=szi_name)
    @click.argument('command', type=click.Choice(['status', 'info']), metavar='COMMAND')
    @click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
    def szi_command(command, output_json):
        """Execute a command on a specified SZI."""
        result = manager.run_plugin(szi_name, command, output_json)
        click.echo(result)

    return szi_command


for szi in manager.plugins.keys():
    cli.add_command(create_szi_command(szi))

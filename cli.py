import click
from core import PluginManager

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
    @click.option('--directory', '-d', type=click.Path(exists=True, file_okay=False), default='/home/',
                  help='Directory to check for integrity status (only for integrity_check)')
    @click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
    def szi_command(command, directory, output_json):
        """Execute a command on a specified SZI."""
        if szi_name == 'integrity_check' and command == 'status':
            result = manager.run_plugin(szi_name, command, output_json, directory=directory)
        else:
            result = manager.run_plugin(szi_name, command, output_json)
        click.echo(result)

    return szi_command


for szi in manager.plugins.keys():
    cli.add_command(create_szi_command(szi))



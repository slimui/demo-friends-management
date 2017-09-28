import click
import json
from os import path
from app.graphql import schema


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option(
    '--write/--no-write', default=True, help="Write to default file location")
def graphql(write=True):
    "Print GraphQL schema"
    data = {
        'data': schema.introspect()
    }
    output = json.dumps(data, indent=2)
    if write:
        cwd = path.dirname(path.realpath(__file__))
        filepath = path.join(cwd, 'schema', 'schema.json')
        click.echo('Writing schema to `{}`'.format(filepath))
        with open(filepath, 'w') as fp:
            fp.write(output)
    else:
        click.echo(output)


if __name__ == '__main__':
    cli(obj={})

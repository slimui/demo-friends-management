import click
import json
from os import path
from app.graphql import schema
from app.models import db
from app.samples import load_samples
from app import create_app


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


@cli.command()
def initdb():
    """Initialize database."""
    click.echo(
        'Preparing recreate the database, all existing data will be lost.')
    if not click.confirm('Do you want to continue?'):
        return
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        load_samples()
        db.session.commit()
        click.echo('Done!')


if __name__ == '__main__':
    cli(obj={})

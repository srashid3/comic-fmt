import click

from comics import Comic
from cli.common import error_handler, process_path


@click.command(
    no_args_is_help=True,
    help="Uncompress file archive."
)
@click.argument("path")
@click.pass_context
@error_handler
def uncompress(ctx, path):
    paths = process_path(path)

    for path in paths:
        c = Comic(path)
        c.uncompress()
        print(f'Uncompressed {path}')

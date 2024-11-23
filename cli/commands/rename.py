import click

from comics import Comic, utils
from cli.common import error_handler, process_path


@click.command(
    no_args_is_help=True,
    help="Rename file archive."
)
@click.option(
    "--order",
    "-o",
    help="Order volumes or issues."
)
@click.option(
    "--cleanup",
    "-c",
    is_flag=True,
    help="Remove extra characters from title."
)
@click.argument("path")
@click.pass_context
@error_handler
def rename(ctx, path, order, cleanup):
    paths = process_path(path)

    title = None
    padding = utils.zero_padded(len(paths))

    for idx, path in enumerate(paths):
        c = Comic(path)

        if order:
            title = f'{order}{idx + 1:{padding}}'

        c.rename(title=title, cleanup=cleanup)

        print(f'Renamed {path} to {c.archive.filename}')

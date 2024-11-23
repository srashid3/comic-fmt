import click

from comics import Comic
from cli.common import error_handler, process_path


@click.command(
    no_args_is_help=True,
    short_help="Format page names.",
    help=(
        "Format the pages within a file archive using a standard naming "
        "convention. By default, numbered files are considered pages."
    )
)
@click.option(
    "--pagename",
    "-p",
    help="Name of page."
)
@click.option(
    "--regex",
    "-r",
    metavar="PATTERN",
    default=r"\d+",
    help="Regular expression for finding pages."
)
@click.option(
    "--flatten",
    "-f",
    is_flag=True,
    help="Move all pages to root directory."
)
@click.option(
    "--remove",
    "-r",
    is_flag=True,
    help="Remove all other files."
)
@click.argument("path")
@click.pass_context
@error_handler
def pages(ctx, path, pagename, regex, flatten, remove):
    paths = process_path(path)

    for path in paths:
        c = Comic(path)

        if flatten:
            c.flatten()

        if pagename:
            c.format_pages(pagename, regex, remove)

        c.save()

        print(f'Formatted {path}')

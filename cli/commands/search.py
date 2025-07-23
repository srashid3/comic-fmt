import click

from comics import Comic
from cli.common import error_handler, process_path


@click.command(
    no_args_is_help=True,
    help="Search file archive."
)
@click.option(
    "--query",
    "-q",
    help="Search query"
)
@click.argument("path")
@click.pass_context
@error_handler
def search(ctx, path, query):
    paths = process_path(path)

    for path in paths:
        c = Comic(path)
        results = c.search(query)

        if not results:
            continue

        print_results(path, results)

        if path is not paths[-1]:
            print()


def print_results(path, results):
    print(f'{path} ({len(results)})')

    for result in results:
        print(f'|_ {result}')

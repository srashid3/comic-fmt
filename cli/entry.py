import click

from cli.commands.cbz import cbz
from cli.commands.pages import pages
from cli.commands.rename import rename
from cli.commands.search import search
from cli.commands.uncompress import uncompress


@click.group(
    help=(
        "Manage file archives for comic books.\n\n"
        "If the PATH for a command is a directory, then the operation is "
        "automatically applied to all file archives within the directory."
    )
)
@click.pass_context
def entry(ctx):
    ctx.ensure_object(dict)


entry.add_command(cbz)
entry.add_command(pages)
entry.add_command(rename)
entry.add_command(search)
entry.add_command(uncompress)

import sys
import os
import click
from collections import deque

DEFAULT_LINES = 10

def process_file(filepath, num_lines):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = deque(file, maxlen=num_lines)
            for line in lines:
                print(line.rstrip())
    except FileNotFoundError:
        click.echo(f"Error: File '{filepath}' not found.", err=True)
    except Exception as e:
        click.echo(f"An error occurred while processing '{filepath}': {e}", err=True)

@click.command()
@click.argument('file_paths', nargs=-1, required=False)
@click.option('--lines', '-n', type=int, default=DEFAULT_LINES, help="Number of lines to display (default: 10)")
def tail(file_paths, lines):
    if file_paths:
        for filepath in file_paths:
            if len(file_paths) > 1:
                click.echo(f"\n==> {os.path.basename(filepath)} <==")
            process_file(filepath, lines)
    else:
        process_file(sys.stdin, lines + 7)

if __name__ == "__main__":
    tail()


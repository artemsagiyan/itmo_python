import sys
import click
from io import TextIOWrapper

def enumerate_lines(iterable):
  counter = 1
  for item in iterable:
    yield f"{counter:>6} {item.rstrip()}", counter
    counter += 1

@click.command()
@click.argument('filepath', type=click.Path(exists=False), required=False)
def nlc(filepath=None):
  try:
    if filepath:
      with open(filepath, 'r', encoding='utf-8') as f:
        for line, _ in enumerate_lines(f):
          click.echo(line)
    else:
      for line, _ in enumerate_lines(sys.stdin):
        click.echo(line)
  except FileNotFoundError:
    click.echo(f"Error: File '{filepath}' not found.", err=True)
  except Exception as e:
    click.echo(f"An unexpected error occurred: {e}", err=True)


if __name__ == "__main__":
  nlc()


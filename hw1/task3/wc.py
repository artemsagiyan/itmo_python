import os
import click

@click.command()
@click.argument('file_paths', nargs=-1, required=False)
def wc(file_paths=None):
  
  total_lines = 0
  total_words = 0
  total_bytes = 0

  if not file_paths: 
    file_paths = ["-"] 

  for file_path in file_paths:
    try:
      with open(file_path, 'rb') as f: 
        contents = f.read()
        lines = contents.count(b'\n') + (1 if contents else 0) 
        words = len(contents.split())
        bytes = len(contents)

        total_lines += lines
        total_words += words
        total_bytes += bytes


        filename = file_path if file_path == "-" else os.path.basename(file_path)
        print(f"{lines:>8}{words:>8}{bytes:>8} {filename}")

    except FileNotFoundError:
      click.echo(f"Error: File '{file_path}' not found.", err=True)
    except Exception as e:
      click.echo(f"An error occurred while processing '{file_path}': {e}", err=True)


  if len(file_paths) > 1:
    print(f"{total_lines:>8}{total_words:>8}{total_bytes:>8} total")

if __name__ == "__main__":
  wc()


import sys
from io import TextIOWrapper
import argparse

def enumerate_lines(iterable):
  counter = 1
  for item in iterable:
    yield f"{counter:>6} {item.rstrip()}", counter
    counter += 1

def process_input(input_stream):
  for line, _ in enumerate_lines(input_stream):
    print(line)


def main():
 parser = argparse.ArgumentParser(description="Number lines from file or stdin.")
 parser.add_argument("file", nargs="?", help="Path to input file. If omitted, reads from stdin.")
 args = parser.parse_args()

 try:
  if args.file:
    with open(args.file, 'r', encoding='utf-8') as f:
      process_input(f)
  else:
    process_input(sys.stdin)
 except FileNotFoundError:
  print(f"Error: File '{args.file}' not found.", file=sys.stderr)
 except Exception as e:
  print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
  main()


import csv
import re
import sys
import os
import glob


def search_files(pattern, files, flags=0):
  for file in files:
    with open(file, 'r') as f:
      for line_number, line in enumerate(f, start=1):
        if re.search(pattern, line, flags=flags):
          print(f"{file}:{line_number}: {line}")


def case(case_pref, pattern, files):
  if case_pref == "yes":
    for file in files:
      with open(file, 'r') as f:
        for line_number, line in enumerate(f, start=1):
          if re.search(pattern, line, re.IGNORECASE):
            print(f"{file}:{line_number}: {line}")
  else:
    search_files(pattern, files)


def modify_output(pattern,
                  files,
                  case_sensitive=True,
                  display_count_only=False):
  flags = 0 if case_sensitive else re.IGNORECASE
  match_count = 0
  for file in files:
    with open(file, 'r') as f:
      for line_number, line in enumerate(f, start=1):
        if re.search(pattern, line, flags=flags):
          match_count += 1
          if not display_count_only:
            print(f"{file}:{line_number}: {line}", end='')
  if display_count_only:
    print(f"Total matching lines: {match_count}")


def main():
  pattern = input("Enter pattern to search: ")
  directory = input("Enter directory to search recursively: ")
  case_sensitive_input = input(
      "Perform case-sensitive search? (yes/no): ").lower()
  case_sensitive = case_sensitive_input == "yes"
  display_count_input = input(
      "Display count of matching lines only? (yes/no): ").lower()
  display_count_only = display_count_input == "yes"
  if display_count_only:
    files = glob.glob("*.txt")
    modify_output(pattern, files, case_sensitive, display_count_only)
  elif case_sensitive_input:
    files = glob.glob("*.txt")
    case(case_sensitive_input, pattern, files)


if __name__ == "__main__":
  main()

import csv
import re
import sys
import os
import glob
from colorama import init, Fore, Style

# Initialize colorama
init()

def search_files(pattern, files, flags=0):
    for file in files:
        with open(file, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                if re.search(pattern, line, flags=flags):
                    print(Fore.GREEN + f"{file}:{line_number}: {line}", end='')
                    print(Style.RESET_ALL, end='')


def case(case_pref, pattern, files):
    if case_pref == "yes":
        for file in files:
            with open(file, 'r') as f:
                for line_number, line in enumerate(f, start=1):
                    if re.search(pattern, line, re.IGNORECASE):
                        print(Fore.GREEN + f"{file}:{line_number}: {line}", end='')
                        print(Style.RESET_ALL, end='')
    else:
        search_files(pattern, files)


def modify_output(pattern, files, case_sensitive=True, display_count_only=False):
    flags = 0 if case_sensitive else re.IGNORECASE
    match_count = 0
    for file in files:
        with open(file, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                if re.search(pattern, line, flags=flags):
                    match_count += 1
                    if not display_count_only:
                        print(Fore.GREEN + f"{file}:{line_number}: {line}", end='')
                        print(Style.RESET_ALL, end='')
    if display_count_only:
        print(f"{Fore.CYAN}Total matching lines: {match_count}{Style.RESET_ALL}")


def context_invert_wholewords(pattern, directory,
                              case_sensitive=True,
                              display_count_only=False,
                              context_lines=0,
                              invert_match=False,
                              whole_words=False):
    flags = re.MULTILINE
    if not case_sensitive:
        flags |= re.IGNORECASE

    if whole_words:
        pattern = r'\b' + re.escape(pattern) + r'\b'

    match_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    match = re.search(pattern, line, flags=flags)
                    if (match and not invert_match) or (not match and invert_match):
                        match_count += 1
                        if not display_count_only:
                            start_index = max(0, i - context_lines)
                            end_index = min(len(lines), i + context_lines + 1)
                            context = ''.join(lines[start_index:end_index])
                            print(Fore.GREEN + f"{file_path}:{i+1}: {context}", end='')
                            print(Style.RESET_ALL, end='')
    if display_count_only:
        print(f"{Fore.CYAN}Total matching lines: {match_count}{Style.RESET_ALL}")


def main():
    pattern = input("Enter pattern to search: ")
    directory = input("Enter directory to search recursively: ")
    case_sensitive_input = input(
        "Perform case-sensitive search? (yes/no): ").lower()
    case_sensitive = case_sensitive_input == "yes"
    display_count_input = input(
        "Display count of matching lines only? (yes/no): ").lower()
    display_count_only = display_count_input == "yes"
    context_lines = int(
        input("Enter number of context lines to display (0 for no context): "))
    invert_match_input = input("Invert the match? (yes/no): ").lower()
    invert_match = invert_match_input == "yes"
    whole_words_input = input("Search only whole words? (yes/no): ").lower()
    whole_words = whole_words_input == "yes"
    if context_lines or invert_match or whole_words:
        context_invert_wholewords(pattern, directory, case_sensitive,
                                  display_count_only, context_lines,
                                  invert_match, whole_words)
    elif display_count_only:
        files = glob.glob("*.txt")
        modify_output(pattern, files, case_sensitive, display_count_only)
    elif case_sensitive_input:
        files = glob.glob("*.txt")
        case(case_sensitive_input, pattern, files)


if __name__ == "__main__":
    main()

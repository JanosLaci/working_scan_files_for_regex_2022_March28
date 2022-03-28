#!/usr/bin/env python

"""scans the .py, .txt. and .sql files of a folder named folder_to_scan for regular expression patterns (SELECT * and DECODE)"""

import pathlib
import re
import argparse
from datetime import datetime

def main():
    current_date_and_time = datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")

    current_working_directory = pathlib.Path.cwd()
    file_to_scan = None

    parser = argparse.ArgumentParser(description="Scan files or folders for regular expressions that may point to suboptimal coding practices.")

    parser.add_argument("-p", "--path", required=True, type=str, help="absolute or relative path of a single file or a folder containing the files to be scanned")
    # parser.add_argument("-o", "--output", action="store_true", help="Generate output file output_scan_results_<date and time.csv>")
    parser.add_argument("-s", "--start", required=False, type=int, help="Start the scan at this line.")
    parser.add_argument("-e", "--end", required=False, type=int, help="End the scan at this line.")

    args = parser.parse_args()

    potential_absolute_path = pathlib.Path(args.path)

    if potential_absolute_path.is_file():
        file_to_scan = potential_absolute_path
        
    elif potential_absolute_path.is_dir():
        directory_to_scan = potential_absolute_path

    potential_relative_path = pathlib.Path(current_working_directory, args.path)

    if potential_relative_path.is_file():
        file_to_scan = potential_relative_path

    elif potential_relative_path.is_dir():
        directory_to_scan = potential_relative_path



# the regex pattern will match any SELECT * command 
# pattern is case-insensitive and tolerates any amount of whitespace (even if SELECT and * are on different lines)

    pattern_select_star = re.compile(r'(?i)SELECT\s*\*')

# a folder_to_scan directory is used, '.py', '.txt', '.sql' files must be placed there


    # if args.output:
        # output_path = pathlib.Path(current_working_directory, r"output_scan_results_", current_date_and_time, r".csv")
    with open('output_scan_results.csv', "w") as writer:
        line_to_append = "file_containing_regex;line_beginning;line_ending;type_found;datetime_of_scan\n"
        writer.write(line_to_append)

    # a folder_to_scan directory is used, '.py', '.txt', '.sql' files must be placed there

    filetypes_to_check = ['.py', '.txt', '.sql']
    if file_to_scan and file_to_scan.suffix in filetypes_to_check:
        path = file_to_scan
        with open(path, 'r') as file_scanned:
                content = file_scanned.read()
                print(f'The following matches were found in the {path.name} file:')
                matches = pattern_select_star.finditer(content)
                for match in matches:
                    line_beginning = content[:match.span()[0]].count("\n" ) + 1
                    print(f'    Beginning on line {line_beginning}:')
                    print(f'    --->>>{match.group(0)}<<<---')
                    print("\n")

    else:
        files_or_folders_found = directory_to_scan.iterdir()
        filetypes_to_check = ['.py', '.txt', '.sql']
        # , current_date_and_time, r".csv"
        # output_path = pathlib.Path(current_working_directory, r"output_scan_results.csv")
        for path in files_or_folders_found:
            if path.is_file() and path.suffix in filetypes_to_check:
                with open(path, 'r') as file_scanned:
                    content = file_scanned.read()
                    print(f'The following matches were found in the {path.name} file:')
                    matches = pattern_select_star.finditer(content)
                    for match in matches:
                        line_beginning = content[:match.span()[0]].count("\n" ) + 1
                        line_ending = content[:match.span()[1]].count("\n" ) + 1
                        print(f'    Beginning on line {line_beginning} and ending on line {line_ending}:')
                        print(f'    --->>>{match.group(0)}<<<---')
                        print("\n")
                        #if args.output:
                        with open('output_scan_results.csv', "a") as writer:
                            # r"file_containing_regex,line_beginning,line_ending,type_found,datetime_of_scan"
                            line_to_append = f"{path.name};{line_beginning};{line_ending};{pattern_select_star};{current_date_and_time}\n"
                            print(line_to_append)
                            writer.write(line_to_append)




if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import os
import re

# Function to process each file
def process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    tb_match_line_index = None
    last_initial_begin_index = None

    # Find the "wire tb_match" line and its location
    for i, line in enumerate(lines):
        if re.match(r'^\s*wire\s+tb_match\s*\;.*$', line):
            tb_match_line_index = i
            break

    if tb_match_line_index is None:
        # No "wire tb_match" found, nothing to do
        print(f"SKIPPED: {file_path} (didn't find a matching 'wire tb_match;')")
        return

    # Search for the last "initial begin" within the previous 15 lines of "wire tb_match"
    for i in range(tb_match_line_index - 1, max(0, tb_match_line_index - 16), -1):
        if re.search(r'\binitial begin\b', lines[i]):
            last_initial_begin_index = i
            break

    if last_initial_begin_index is None:
        # No suitable "initial begin" found, skip this file
        print(f"SKIPPED: {file_path} (didn't find a matching 'initial begin')")
        return

    # Move "wire tb_match" and the next line above the found "initial begin"
    tb_match_line = lines.pop(tb_match_line_index)
    next_line = lines.pop(tb_match_line_index)  # Index remains same because we popped one line

    # Insert the two lines above the found "initial begin"
    lines.insert(last_initial_begin_index, next_line)
    lines.insert(last_initial_begin_index, tb_match_line)

    # Write the modified content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    print(f"FIXED  : {file_path}")

for directory in [ './dataset_code-complete-iccad2023', 'dataset_spec-to-rtl' ]:
    # Iterate over all files in the directory ending with "_test.sv"
    for filename in os.listdir(directory):
        if filename.endswith('_test.sv'):
            process_file(os.path.join(directory, filename))

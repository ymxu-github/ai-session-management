# Developer: ymxu
# Created: 2026/9/26 9:07
# File: write-file.py

# The with statement ensures resources are properly acquired and released,
# even if an exception occurs. It is the recommended approach in projects.
# Open the file
with open('../resources/new_file.txt', 'w', encoding='utf-8') as f:
    # Write to the file
    f.write("This is newly written content.\n")
    f.write("This is newly written content.\n")
    i = 1/0  # Deliberately raise an exception
    f.write("This is newly written content.\n")
    f.write("This is newly written content.\n")
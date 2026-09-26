# Developer: ymxu
# Created: 2026/9/26 9:00
# File: read-file.py

# Open the file. The Unicode escapes preserve the existing Chinese filename.
f = open('../resources/\u671b\u5e90\u5c71\u7011\u5e03.txt', 'r', encoding='utf-8')

# Read the contents
try:
    # Method 1
    # content = f.read()
    # print(content)
    # Method 2
    content_list = f.readlines()
    for line in content_list:
        print(line.strip())  # Remove the newline from each line
# Close the file
finally:
    print("Closing the file")
    f.close()
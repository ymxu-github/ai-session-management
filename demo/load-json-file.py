# Developer: ymxu
# Created: 2026/9/26 9:51
# File: load-json-file.py
# Description: Read JSON data from a file and deserialize it into a Python object

import json

with open('../resources/json_file.json', 'r', encoding='utf-8') as f:
    # Deserialize the JSON data into a Python object
    obj = json.load(f)
    print(obj)
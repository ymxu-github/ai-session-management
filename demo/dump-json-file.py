# Developer: ymxu
# Created: 2026/9/26 9:41
# File: dump-json-file.py
# Description: Serialize a Python object to JSON and write it to a file
import json

obj = {
    "name": "Alice",
    "age": 15,
    "city": "New York",
    "hobbies": ["reading", "traveling", "swimming"],
}

with open('../resources/json_file.json', 'w', encoding='utf-8') as f:
    # ensure_ascii=False allows non-ASCII characters in the output.
    # indent=4 indents the output by four spaces.
    json.dump(obj, f, ensure_ascii=False, indent=4)
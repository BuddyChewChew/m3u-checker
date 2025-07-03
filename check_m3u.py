import os
import requests
from time import sleep

INPUT_FILE = 'playlist.m3u'
OUTPUT_FILE = 'working_playlist.m3u'
TIMEOUT = 10

def is_stream_working(url):
    try:
        r = requests.get(url, timeout=TIMEOUT, stream=True)
        return r.status_code == 200
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

if not os.path.isfile(INPUT_FILE):
    print(f"ERROR: {INPUT_FILE} not found. Please make sure it exists in the working directory.")
    # Still create an empty output file to avoid confusion
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        pass
    exit(1)

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

working_lines = []
i = 0
while i < len(lines):
    if lines[i].startswith('#EXTINF'):
        if i + 1 < len(lines):
            url = lines[i+1].strip()
            print(f'Checking: {url}')
            if is_stream_working(url):
                working_lines.append(lines[i])
                working_lines.append(url + '\n')
            else:
                print(f'Broken: {url}')
            i += 2
        else:
            print(f"Warning: #EXTINF at line {i} not followed by a URL")
            i += 1
    else:
        i += 1

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(working_lines)

if working_lines:
    print(f'Done. Working streams saved to {OUTPUT_FILE}')
else:
    print(f'No working streams found. {OUTPUT_FILE} created but is empty.')

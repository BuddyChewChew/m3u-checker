import requests
from time import sleep

INPUT_FILE = 'playlist.m3u'
OUTPUT_FILE = 'working_playlist.m3u'
TIMEOUT = 10

def is_stream_working(url):
    try:
        r = requests.get(url, timeout=TIMEOUT, stream=True)
        return r.status_code == 200
    except Exception:
        return False

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

working_lines = []
i = 0
while i < len(lines):
    if lines[i].startswith('#EXTINF'):
        url = lines[i+1].strip()
        print(f'Checking: {url}')
        if is_stream_working(url):
            working_lines.append(lines[i])
            working_lines.append(url + '\n')
        else:
            print(f'Broken: {url}')
        i += 2
    else:
        i += 1

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(working_lines)

print(f'Done. Working streams saved to {OUTPUT_FILE}')

import urllib.request
import re
import os

start_word = 'arts'
cache_file = 'poopbank.txt'

# fetch current word bank from poople.io
def fetch_poopometer():
    # inspect bowl for today's bundle
    with urllib.request.urlopen('https://poople.io/') as r:
        html = r.read().decode('utf-8')

    match = re.search(r'/assets/index-[^"\']+\.js', html)
    if not match:
        raise RuntimeError('Pipes clogged - could not find the poop pipe in poople.io index')

    bundle_url = 'https://poople.io' + match.group(0)

    # snake the pipe and extract the poopometer
    with urllib.request.urlopen(bundle_url) as r:
        raw_sewage = r.read().decode('utf-8')

    first_plop = raw_sewage.index('const wordDist=`') + len('const wordDist=`')
    final_wipe = raw_sewage.index('`', first_plop)
    return raw_sewage[first_plop:final_wipe]

# parse raw wordDist string to dict
def sewage_treatment(raw):
    poopometer = {}
    for line in raw.splitlines():
        line = line.strip().replace('\\r', '').replace('\r', '')
        if not line:
            continue
        parts = line.split(',')
        word = parts[0].strip().lower()
        poop_dist = int(parts[1].strip())
        poopometer[word] = poop_dist
    return poopometer

# load from cache or fetch fresh
def load_poopometer():
    if os.path.exists(cache_file):
        print(f'Loading from cache: {cache_file}')
        with open(cache_file, 'r', encoding='utf-8') as f:
            raw = f.read()
    else:
        print('No cache found, fetching from poople.io...')
        raw = fetch_poopometer()
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(raw)
        print(f'Saved to {cache_file}')

    return sewage_treatment(raw)

# check for word adjacency by diff == 1 char
def is_adjacent(a, b):
    if len(a) != len(b):
        return False
    poopy_diffs = sum(1 for x, y in zip(a, b) if x != y)
    return poopy_diffs == 1

# finding all neighbors at target dist
def turd_radar(word, target_dist):
    return [w for w, d in poopometer.items() if d == target_dist and is_adjacent(word, w)]

# wayfinding to poop
def find_all_flush_routes(start):
    start = start.lower()

    if start not in poopometer:
        print(f'"{start}" not in word bank')
        return []

    dist = poopometer[start]
    if dist == 0:
        return [[start]]

    flush_routes = []

    def repoop(current, tp_trail):
        current_poop_dist = poopometer[current]
        if current_poop_dist == 0:
            flush_routes.append(tp_trail[:])
            return
        for turd_candidate in turd_radar(current, current_poop_dist - 1):
            tp_trail.append(turd_candidate)
            repoop(turd_candidate, tp_trail)
            tp_trail.pop()

    repoop(start, [start])
    return flush_routes

poopometer = load_poopometer()
print(f'Loaded {len(poopometer)} words\n')

print(f'Finding all optimal flush routes: {start_word.upper()} -> POOP\n')

all_flush_routes = find_all_flush_routes(start_word)

if not all_flush_routes:
    print('No paths to POOP found.')
else:
    print(f'Found {len(all_flush_routes)} clean flush route(s) in {len(all_flush_routes[0]) - 1} plop(s):\n')
    for i, flush_route in enumerate(all_flush_routes, 1):
        print(f'  {i}: {" -> ".join(w.upper() for w in flush_route)}')

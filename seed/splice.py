#!/usr/bin/env python3
"""Puts the output of seed/make.py into compose.yaml, between the lines that write
/docker-entrypoint-initdb.d/shop.sql and the SQL that ends it.

    python3 seed/splice.py           rewrite compose.yaml
    python3 seed/splice.py --check   fail if compose.yaml is not what make.py writes
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
COMPOSE = HERE.parent / 'compose.yaml'
START = "cat > /docker-entrypoint-initdb.d/shop.sql <<'SQL'"

sql = subprocess.run([sys.executable, str(HERE / 'make.py')], check=True,
                     capture_output=True, text=True).stdout.rstrip('\n')
lines = COMPOSE.read_text().split('\n')
start = next(i for i, line in enumerate(lines) if line.strip() == START)
indent = lines[start][:len(lines[start]) - len(lines[start].lstrip())]
end = next(i for i in range(start + 1, len(lines)) if lines[i] == indent + 'SQL')
body = [(indent + line) if line else '' for line in sql.split('\n')]
wanted = '\n'.join(lines[:start + 1] + body + lines[end:])

if '--check' in sys.argv:
    if COMPOSE.read_text() != wanted:
        sys.exit('compose.yaml is not what seed/make.py writes: run python3 seed/splice.py')
    print('compose.yaml carries seed/make.py exactly')
else:
    COMPOSE.write_text(wanted)

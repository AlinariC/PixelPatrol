import curses
import json
import random
import string
from pathlib import Path

LICENSE_FILE = Path(__file__).parent / 'licenses.json'


def prompt(stdscr, y, text):
    curses.echo()
    stdscr.addstr(y, 2, text)
    stdscr.clrtoeol()
    value = stdscr.getstr(y, 2 + len(text), 60).decode().strip()
    curses.noecho()
    return value


def load_licenses():
    try:
        with open(LICENSE_FILE, 'r') as f:
            data = json.load(f)
            # Support old format: list of strings
            if data and isinstance(data[0], str):
                return [
                    {
                        'key': k,
                        'name': '',
                        'email': '',
                        'expires': ''
                    }
                    for k in sorted(set(data))
                ]
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_licenses(licenses):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(sorted(licenses, key=lambda x: x['key']), f, indent=2)


def draw_menu(stdscr, licenses, idx):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    title = "License Manager - Up/Down navigate, 'a' add, 'd' delete, 'q' quit"
    stdscr.addstr(0, 0, title[:width - 1])
    for i, lic in enumerate(licenses):
        attr = curses.A_REVERSE if i == idx else curses.A_NORMAL
        display = f"{lic['key']} - {lic['name']} ({lic['expires']})"
        stdscr.addstr(i + 2, 2, display[:width - 4], attr)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    licenses = load_licenses()
    idx = 0

    while True:
        draw_menu(stdscr, licenses, idx)
        ch = stdscr.getch()

        if ch in (ord('q'), ord('Q')):
            break
        elif ch in (curses.KEY_UP, ord('k')):
            if licenses:
                idx = max(0, idx - 1)
        elif ch in (curses.KEY_DOWN, ord('j')):
            if licenses:
                idx = min(len(licenses) - 1, idx + 1)
        elif ch in (ord('a'), ord('A')):
            # Auto-generate a unique 24-character alphanumeric license
            alphabet = string.ascii_uppercase + string.digits
            existing = {l['key'] for l in licenses}
            while True:
                new_key = ''.join(random.choices(alphabet, k=24))
                if new_key not in existing:
                    break
            y = len(licenses) + 4
            name = prompt(stdscr, y, 'Customer name: ')
            email = prompt(stdscr, y + 1, 'Customer email: ')
            expires = prompt(stdscr, y + 2, 'Expiration (YYYY-MM-DD): ')
            new_entry = {
                'key': new_key,
                'name': name,
                'email': email,
                'expires': expires,
            }
            licenses.append(new_entry)
            licenses.sort(key=lambda x: x['key'])
            idx = licenses.index(new_entry)
            stdscr.addstr(y + 4, 2, f"Added license: {new_key}")
            stdscr.refresh()
            curses.napms(1000)
        elif ch in (ord('d'), ord('D')) and licenses:
            licenses.pop(idx)
            idx = min(idx, len(licenses) - 1)

    save_licenses(licenses)


if __name__ == '__main__':
    curses.wrapper(main)

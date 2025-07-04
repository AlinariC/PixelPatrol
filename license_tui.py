import curses
import json
import random
import string
from pathlib import Path

LICENSE_FILE = Path(__file__).parent / 'licenses.json'


def prompt(stdscr, y, text):
    """Prompt for user input using the full width of the window."""
    curses.echo()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(y, 2, text)
    stdscr.clrtoeol()
    max_len = max(10, width - len(text) - 4)
    value = stdscr.getstr(y, 2 + len(text), max_len).decode().strip()
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
    """Render the license list with a simple framed layout."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Border and title
    stdscr.border()
    title = "License Manager"
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(0, max(2, (width - len(title)) // 2), title)
    stdscr.attroff(curses.A_BOLD)

    # Column headers
    # Determine column widths. For wide terminals (>=110 columns) we
    # expand the default sizes to better utilise the available space.
    table_width = width - 4  # account for border
    if width >= 110:
        col_key = 30
        col_name = 28
        col_email = 40
        col_expires = table_width - col_key - col_name - col_email - 3
        if col_expires < 10:
            col_expires = 10
    else:
        col_key = 25
        col_name = 18
        col_email = 23
        col_expires = max(7, table_width - col_key - col_name - col_email - 3)

    header = (
        "KEY".ljust(col_key) +
        "NAME".ljust(col_name) +
        "EMAIL".ljust(col_email) +
        "EXPIRES".ljust(col_expires)
    )
    stdscr.addstr(2, 2, header[:table_width], curses.A_UNDERLINE)

    # License entries
    for i, lic in enumerate(licenses):
        attr = curses.A_REVERSE if i == idx else curses.A_NORMAL
        row = (
            f"{lic['key']:<{col_key - 1}} "
            f"{lic['name']:<{col_name - 1}} "
            f"{lic['email']:<{col_email - 1}} "
            f"{lic['expires']:<{col_expires}}"
        )
        stdscr.addstr(3 + i, 2, row[:table_width], attr)

    help_line = "[A] Add  [D] Delete  [Q] Quit  Up/Down Navigate"
    stdscr.addstr(height - 2, 2, help_line[:width - 4])

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

            height, _ = stdscr.getmaxyx()
            y = height - 6
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
            removed = licenses.pop(idx)
            idx = min(idx, len(licenses) - 1)
            height, _ = stdscr.getmaxyx()
            stdscr.addstr(height - 4, 2, f"Removed license: {removed['key']}")
            stdscr.refresh()
            curses.napms(1000)

    save_licenses(licenses)


if __name__ == '__main__':
    curses.wrapper(main)

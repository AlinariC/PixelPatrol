import curses
import json
from pathlib import Path

LICENSE_FILE = Path(__file__).parent / 'licenses.json'


def load_licenses():
    try:
        with open(LICENSE_FILE, 'r') as f:
            return sorted(set(json.load(f)))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_licenses(licenses):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(sorted(licenses), f)


def draw_menu(stdscr, licenses, idx):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    title = "License Manager - Up/Down navigate, 'a' add, 'd' delete, 'q' quit"
    stdscr.addstr(0, 0, title[:width - 1])
    for i, lic in enumerate(licenses):
        attr = curses.A_REVERSE if i == idx else curses.A_NORMAL
        stdscr.addstr(i + 2, 2, lic[:width - 4], attr)
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
            curses.echo()
            stdscr.addstr(len(licenses) + 4, 2, "Enter new license: ")
            stdscr.clrtoeol()
            new = stdscr.getstr().decode().strip()
            curses.noecho()
            if new and new not in licenses:
                licenses.append(new)
                licenses.sort()
                idx = licenses.index(new)
        elif ch in (ord('d'), ord('D')) and licenses:
            licenses.pop(idx)
            idx = min(idx, len(licenses) - 1)

    save_licenses(licenses)


if __name__ == '__main__':
    curses.wrapper(main)

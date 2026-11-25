import argparse
import curses
import random
import time

DEFAULT_CHARS="abcdefghijklmnopqrstuvwxyz"
SPEEDS=[0.4, 0.6, 1.0]
COLUMN_GAP=2
FRAME_DELAY=0.04
COLORS={
    "green": curses.COLOR_GREEN,
    "red": curses.COLOR_RED,
    "cyan": curses.COLOR_CYAN,
    "blue": curses.COLOR_BLUE,
    "yellow": curses.COLOR_YELLOW,
    "magenta": curses.COLOR_MAGENTA,
    "white": curses.COLOR_WHITE,
}

def positive_float(value):
    number=float(value)
    if number<=0:
        raise argparse.ArgumentTypeError("speed must be greater than 0")
    return number

def parse_args():
    parser=argparse.ArgumentParser(description="Falling characters in the terminal")
    parser.add_argument("--text", default="", help="characters or word used in the rain")
    parser.add_argument("--color", default="green", choices=COLORS.keys(), help="color of the rain")
    parser.add_argument("--speed", type=positive_float, default=1.0, help="speed multiplier, 1.0 is normal")
    return parser.parse_args()

def create_drop(height, speed_scale):
    return {
        "y": random.uniform(-height, 0),
        "length": random.randint(5, max(6, height//2)),
        "speed": random.choice(SPEEDS)*speed_scale,
    }

def create_drops(width, height, speed_scale):
    return [create_drop(height, speed_scale) for _ in range(width)]

def setup_colors(color):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, COLORS[color], -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)

def get_style(position):
    if position==0:
        return curses.color_pair(2)|curses.A_BOLD
    if position<4:
        return curses.color_pair(1)|curses.A_BOLD
    return curses.color_pair(1)|curses.A_DIM

def draw_drop(screen, drop, x, height, chars):
    head=int(drop["y"])
    for i in range(drop["length"]):
        y=head-i
        if 0<=y<height:
            try:
                screen.addstr(y, x, random.choice(chars), get_style(i))
            except curses.error:
                pass

def update_drop(drop, height, speed_scale):
    drop["y"]+=drop["speed"]
    if int(drop["y"])-drop["length"]>height:
        return create_drop(height, speed_scale)
    return drop

def main(screen, chars, color, speed_scale):
    curses.curs_set(0)
    screen.nodelay(True)
    setup_colors(color)
    height, width=screen.getmaxyx()
    drops=create_drops(width, height, speed_scale)
    while True:
        if screen.getch() in (ord("q"), 27):
            break
        new_height, new_width=screen.getmaxyx()
        if (new_height, new_width)!=(height, width):
            height, width=new_height, new_width
            drops=create_drops(width, height, speed_scale)
        screen.erase()
        for x in range(0, width, COLUMN_GAP):
            draw_drop(screen, drops[x], x, height, chars)
            drops[x]=update_drop(drops[x], height, speed_scale)
        screen.refresh()
        time.sleep(FRAME_DELAY)

if __name__=="__main__":
    args=parse_args()
    chars=args.text.replace(" ", "") or DEFAULT_CHARS
    try:
        curses.wrapper(main, chars, args.color, args.speed)
    except KeyboardInterrupt:
        pass
"""Render taskbar credit-balance concepts with illustrative values."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
FONT = r"C:\Windows\Fonts\msyh.ttc"
BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
BG = (16, 18, 22)
TASKBAR = (29, 29, 31)
WIDGET = (27, 27, 27)
TEXT = (247, 248, 249)
MUTED = (178, 181, 185)
TRACK = (55, 59, 64)
ACCENT = (255, 255, 255)
LINE = (81, 85, 90)
YELLOW = (232, 191, 95)


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def text(d, xy, value, size=20, color=TEXT, bold=False):
    d.text(xy, value, font=font(size, bold), fill=color)


def rounded_bar(d, xy, pct):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=(y2-y1)//2, fill=TRACK)
    d.rounded_rectangle((x1, y1, x1+(x2-x1)*pct//100, y2), radius=(y2-y1)//2, fill=ACCENT)


def widget(d, x, y, variant):
    # Drawn at 2.5x an ordinary 40px taskbar for legibility.
    width = {"a": 960, "b": 930, "c": 910}[variant]
    d.rectangle((x, y, x+width, y+96), fill=WIDGET)
    d.rectangle((x+2, y+16, x+6, y+80), fill=LINE)
    for i, (label, pct, remainder, reset) in enumerate([
        ("5h", 96, "剩余96%", "00:07重置"),
        ("7d", 30, "剩余30%", "10/04重置"),
    ]):
        yy = y+14+i*42
        text(d, (x+30, yy), label, 24, bold=True)
        rounded_bar(d, (x+105, yy+12, x+370, yy+29), pct)
        text(d, (x+388, yy), remainder, 23, bold=True)
        text(d, (x+510, yy), reset, 23, bold=True)
    sep = x+680
    d.line((sep, y+17, sep, y+80), fill=LINE, width=2)
    if variant == "a":
        text(d, (sep+25, y+33), "点数 939.7", 25, bold=True)
    elif variant == "b":
        text(d, (sep+25, y+11), "额外点数", 21, MUTED)
        text(d, (sep+25, y+42), "939.7", 33, bold=True)
    else:
        d.rounded_rectangle((sep+18, y+21, sep+207, y+75), radius=15, fill=(47, 49, 52))
        text(d, (sep+37, y+31), "+ 939.7", 25, bold=True)
    return width


def render(variant, title, subtitle):
    im = Image.new("RGB", (1200, 490), BG)
    d = ImageDraw.Draw(im)
    text(d, (68, 43), title, 34, bold=True)
    text(d, (70, 98), subtitle, 21, MUTED)
    text(d, (70, 157), "任务栏局部放大预览 · 示例数值", 18, MUTED)
    bar_y = 350 if variant == "c" else 206
    d.rectangle((0, bar_y, 1200, bar_y+120), fill=TASKBAR)
    widget(d, 68, bar_y+12, variant)
    d.line((0, bar_y, 1200, bar_y), fill=(64, 65, 68), width=2)
    if variant == "c":
        # Windows taskbar popovers open above the taskbar.
        d.rounded_rectangle((735, 204, 1110, 336), radius=15, fill=(43, 45, 49))
        text(d, (760, 220), "Codex 额外点数", 20, MUTED)
        text(d, (760, 254), "939.7", 34, bold=True)
        text(d, (760, 304), "余额仅在接口返回时显示", 17, MUTED)
    else:
        text(d, (70, 371), "现有 5 小时和每周额度保持原样", 20, MUTED)
        text(d, (70, 415), "追加字段：Codex credits.balance", 18, MUTED)
    dest = OUT / f"codex-credit-option-{variant}.png"
    im.save(dest)
    print(dest)


render("a", "方案 A · 行内数字", "新增一段“点数 939.7”，视觉最轻，适合优先节省任务栏空间。")
render("b", "方案 B · 双行余额", "右侧独立显示名称和余额，扫一眼更容易分清百分比与点数。")
render("c", "方案 C · 紧凑入口", "任务栏只放短数字；点击后可看完整名称和余额状态。")

#!/usr/bin/env python3
"""The Daily Meridian - one picture of Tuesday 17 November 2026.
Pure stdlib. Own rasteriser, own stroke font, own PNG writer.
Deterministic: no randomness except a fixed arithmetic grain."""
import os, sys, zlib, struct, math

W, H = 1024, 1024
PX = bytearray(W * H * 3)

PAPER = (243, 238, 224); INK = (22, 24, 30); RED = (176, 32, 40)
NAVY = (24, 46, 84); BLUE = (58, 110, 168); SEA = (168, 205, 226)
SKY = (196, 222, 238); SAND = (232, 205, 150); GREEN = (74, 138, 74)
LGREEN = (150, 196, 130); BROWN = (128, 92, 58); GREY = (120, 124, 130)
DGREY = (70, 74, 82); WHITE = (250, 250, 246); GOLD = (216, 164, 52)
ORANGE = (232, 120, 44); TEAL = (40, 140, 140); PURPLE = (110, 74, 150)
PINK = (226, 140, 160); CREAM = (250, 244, 226); LGREY = (205, 206, 200)

def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3; PX[i] = c[0]; PX[i+1] = c[1]; PX[i+2] = c[2]

def rect(x, y, w, h, c):
    x0 = max(0, int(x)); y0 = max(0, int(y))
    x1 = min(W, int(x + w)); y1 = min(H, int(y + h))
    row = bytes(c) * max(0, x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3; PX[i:i + len(row)] = row

def frame(x, y, w, h, c, t=1):
    rect(x, y, w, t, c); rect(x, y + h - t, w, t, c)
    rect(x, y, t, h, c); rect(x + w - t, y, t, h, c)

def line(x0, y0, x1, y1, c, t=1):
    dx = x1 - x0; dy = y1 - y0; n = int(max(abs(dx), abs(dy))) + 1
    r = t // 2
    for i in range(n + 1):
        x = x0 + dx * i / n; y = y0 + dy * i / n
        rect(x - r, y - r, t, t, c)

def dash(x0, y0, x1, y1, c, t=2, on=7, off=5):
    dx = x1 - x0; dy = y1 - y0; n = int(max(abs(dx), abs(dy))) + 1
    for i in range(n + 1):
        if (i % (on + off)) < on:
            x = x0 + dx * i / n; y = y0 + dy * i / n
            rect(x - t // 2, y - t // 2, t, t, c)

def circ(cx, cy, r, c, fill=True):
    for yy in range(int(cy - r), int(cy + r) + 1):
        for xx in range(int(cx - r), int(cx + r) + 1):
            d = (xx - cx) ** 2 + (yy - cy) ** 2
            if fill and d <= r * r: put(xx, yy, c)
            if not fill and r * r - 2 * r <= d <= r * r: put(xx, yy, c)

def poly(pts, c):
    ys = [p[1] for p in pts]; y0 = max(0, int(min(ys))); y1 = min(H - 1, int(max(ys)))
    n = len(pts)
    for yy in range(y0, y1 + 1):
        xs = []
        for i in range(n):
            xa, ya = pts[i]; xb, yb = pts[(i + 1) % n]
            if (ya <= yy < yb) or (yb <= yy < ya):
                xs.append(xa + (yy - ya) * (xb - xa) / (yb - ya))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            rect(xs[i], yy, xs[i + 1] - xs[i], 1, c)

def person(x, y, s, shirt, skin=(236, 196, 150)):
    circ(x, y - 6 * s, 3.2 * s, skin); rect(x - 3 * s, y - 3 * s, 6 * s, 9 * s, shirt)
    line(x - 2 * s, y + 6 * s, x - 2 * s, y + 11 * s, DGREY, max(1, int(s)))
    line(x + 2 * s, y + 6 * s, x + 2 * s, y + 11 * s, DGREY, max(1, int(s)))

# ---------------- stroke font (grid 4 wide x 6 tall, all caps) -------------
def P(*pts): return list(pts)
GL = {
 'A': [P((0,6),(2,0),(4,6)), P((1,4),(3,4))],
 'B': [P((0,0),(0,6)), P((0,0),(3,0),(4,1),(3,3),(0,3)), P((3,3),(4,4),(3,6),(0,6))],
 'C': [P((4,1),(2,0),(0,1),(0,5),(2,6),(4,5))],
 'D': [P((0,0),(0,6)), P((0,0),(3,0),(4,2),(4,4),(3,6),(0,6))],
 'E': [P((4,0),(0,0),(0,6),(4,6)), P((0,3),(3,3))],
 'F': [P((4,0),(0,0),(0,6)), P((0,3),(3,3))],
 'G': [P((4,1),(2,0),(0,1),(0,5),(2,6),(4,5),(4,3),(2.4,3))],
 'H': [P((0,0),(0,6)), P((4,0),(4,6)), P((0,3),(4,3))],
 'I': [P((2,0),(2,6)), P((0,0),(4,0)), P((0,6),(4,6))],
 'J': [P((4,0),(4,5),(3,6),(1,6),(0,5))],
 'K': [P((0,0),(0,6)), P((4,0),(0,3)), P((1.6,3.8),(4,6))],
 'L': [P((0,0),(0,6),(4,6))],
 'M': [P((0,6),(0,0),(2,3),(4,0),(4,6))],
 'N': [P((0,6),(0,0),(4,6),(4,0))],
 'O': [P((1,0),(3,0),(4,1),(4,5),(3,6),(1,6),(0,5),(0,1),(1,0))],
 'P': [P((0,6),(0,0),(3,0),(4,1),(3,3),(0,3))],
 'Q': [P((1,0),(3,0),(4,1),(4,5),(3,6),(1,6),(0,5),(0,1),(1,0)), P((2.4,4.2),(4,6))],
 'R': [P((0,6),(0,0),(3,0),(4,1),(3,3),(0,3)), P((2,3),(4,6))],
 'S': [P((4,1),(2,0),(0,1),(0,2.4),(4,3.6),(4,5),(2,6),(0,5))],
 'T': [P((0,0),(4,0)), P((2,0),(2,6))],
 'U': [P((0,0),(0,5),(1,6),(3,6),(4,5),(4,0))],
 'V': [P((0,0),(2,6),(4,0))],
 'W': [P((0,0),(1,6),(2,2),(3,6),(4,0))],
 'X': [P((0,0),(4,6)), P((4,0),(0,6))],
 'Y': [P((0,0),(2,3),(4,0)), P((2,3),(2,6))],
 'Z': [P((0,0),(4,0),(0,6),(4,6))],
 '0': [P((1,0),(3,0),(4,1),(4,5),(3,6),(1,6),(0,5),(0,1),(1,0)), P((0.6,5),(3.4,1))],
 '1': [P((1,1),(3,0),(3,6)), P((1,6),(4,6))],
 '2': [P((0,1),(1,0),(3,0),(4,1),(0,6),(4,6))],
 '3': [P((0,1),(3,0),(4,1),(3,3),(0,3)), P((3,3),(4,4),(3,6),(0,5))],
 '4': [P((3,6),(3,0),(0,4),(4,4))],
 '5': [P((4,0),(0,0),(0,3),(3,3),(4,4),(3,6),(0,5))],
 '6': [P((4,1),(2,0),(0,2),(0,5),(1,6),(3,6),(4,5),(4,3.8),(3,3),(0,3))],
 '7': [P((0,0),(4,0),(2,6))],
 '8': [P((1,0),(3,0),(4,1),(3,3),(1,3),(0,2),(1,0)), P((1,3),(3,3),(4,4.4),(3,6),(1,6),(0,4.4),(1,3))],
 '9': [P((0,5),(2,6),(4,4),(4,1),(3,0),(1,0),(0,1),(0,2.2),(1,3),(4,3))],
 '.': [], ',': [], ':': [], ';': [], '!': [P((2,0),(2,4))],
 '-': [P((0,3),(4,3))], '+': [P((0,3),(4,3)), P((2,1),(2,5))],
 '$': [P((4,1),(2,0),(0,1),(0,2.4),(4,3.6),(4,5),(2,6),(0,5)), P((2,-0.4),(2,6.4))],
 '%': [P((0,6),(4,0))],
 '/': [P((0,6),(4,0))],
 '?': [P((0,1),(1,0),(3,0),(4,1),(4,2),(2,3.4),(2,4.4))],
 '(': [P((3,0),(1.4,1),(1.4,5),(3,6))], ')': [P((1,0),(2.6,1),(2.6,5),(1,6))],
 "'": [P((2,0),(1.4,1.6))],
}
DOTS = {'.': [(2, 5.4)], ',': [(2, 5.4)], ':': [(2, 1.4), (2, 4.6)],
        ';': [(2, 1.4), (2, 5.0)], '!': [(2, 5.4)], '?': [(2, 5.4)],
        '%': [(0.7, 1.0), (3.3, 5.0)]}

def tw(s, size):
    return len(s) * size * 5.2 / 6.0

def text(x, y, s, size, c=INK, bold=0, align='l'):
    s = s.upper()
    if align == 'c': x -= tw(s, size) / 2
    if align == 'r': x -= tw(s, size)
    u = size / 6.0; t = max(1, int(size / 9)) + bold
    cx = x
    for ch in s:
        if ch == ' ':
            cx += size * 3.4 / 6.0; continue
        for pl in GL.get(ch, []):
            for i in range(len(pl) - 1):
                line(cx + pl[i][0] * u, y + pl[i][1] * u,
                     cx + pl[i + 1][0] * u, y + pl[i + 1][1] * u, c, t)
                if bold:
                    line(cx + pl[i][0] * u + 1, y + pl[i][1] * u,
                         cx + pl[i + 1][0] * u + 1, y + pl[i + 1][1] * u, c, t)
        for (dx, dy) in DOTS.get(ch, []):
            rect(cx + dx * u - t / 2, y + dy * u - t / 2, t + 1, t + 1, c)
        cx += size * 5.2 / 6.0
    return cx

def wrap(s, size, maxw):
    words = s.upper().split(); out = []; cur = ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if tw(t, size) <= maxw or not cur: cur = t
        else: out.append(cur); cur = wd
    if cur: out.append(cur)
    return out

def para(x, y, s, size, maxw, c=INK, lh=None, bold=0):
    lh = lh or size * 1.32
    for ln in wrap(s, size, maxw):
        text(x, y, ln, size, c, bold); y += lh
    return y

def chip(x, y, n, c):
    rect(x, y, 17, 15, c); text(x + 8.5, y + 2.5, str(n), 10, WHITE, 1, 'c')

# ------------------------------- scenes ------------------------------------
def sc_bridge(x, y, w, h):
    rect(x, y, w, h, SKY); rect(x, y + h * 0.62, w, h * 0.38, SEA)
    for i in range(6): line(x + i * 9, y + h * 0.66, x + i * 9 + 22, y + h * 0.66, WHITE, 1)
    rect(x, y + h * 0.55, w * 0.34, 7, DGREY); rect(x + w * 0.60, y + h * 0.55, w * 0.40, 7, DGREY)
    line(x + w * 0.34, y + h * 0.58, x + w * 0.47, y + h * 0.78, DGREY, 3)
    line(x + w * 0.60, y + h * 0.58, x + w * 0.50, y + h * 0.80, DGREY, 3)
    rect(x + 4, y + h * 0.30, 8, h * 0.25, GREY); rect(x + w - 14, y + h * 0.30, 8, h * 0.25, GREY)
    ex, ey = x + w * 0.47, y + h * 0.42
    for a in range(12):
        line(ex, ey, ex + 20 * math.cos(a * 0.9), ey + 15 * math.sin(a * 0.9), ORANGE, 3)
    circ(ex, ey, 9, RED); circ(ex, ey, 5, GOLD)
    for i in range(5): circ(ex + 12 + i * 9, ey - 12 - i * 6, 6 + i * 2, (90, 92, 98))
    text(x + 6, y + 5, 'CRIMEA', 9, INK, 1); text(x + w - 6, y + 5, 'RUSSIA', 9, INK, 1, 'r')

def sc_gulf(x, y, w, h):
    rect(x, y, w, h, SEA)
    poly([(x, y), (x + w * 0.52, y), (x + w * 0.44, y + h * 0.4), (x + w * 0.2, y + h * 0.52), (x, y + h * 0.6)], SAND)
    poly([(x, y + h), (x + w * 0.3, y + h), (x + w * 0.42, y + h * 0.62), (x + w * 0.66, y + h * 0.58), (x + w, y + h)], SAND)
    circ(x + w * 0.52, y + h * 0.48, 7, SAND)
    text(x + 8, y + 6, 'IRAN', 10, INK, 1); text(x + w * 0.33, y + h * 0.53, 'QESHM', 7.5, INK, 1)
    text(x + 6, y + h - 15, 'ARABIA', 9, INK, 1); text(x + w - 6, y + h - 15, 'HORMUZ', 8, INK, 1, 'r')
    bx, by = x + w * 0.74, y + h * 0.62
    text(bx - 28, by + 18, 'BAHRAIN', 8, INK, 1)
    for a in range(8): line(bx, by, bx + 13 * math.cos(a * 0.785), by + 13 * math.sin(a * 0.785), RED, 2)
    circ(bx, by, 3, RED)
    for (sx, sy) in [(x + w * 0.2, y + 14), (x + w * 0.62, y + 10)]:
        dash(sx, sy, bx, by, RED, 2)
        poly([(sx, sy), (sx + 13, sy + 3), (sx, sy + 7)], DGREY)
    rect(x + w * 0.30, y + h * 0.82, 94, 13, RED)
    text(x + w * 0.30 + 47, y + h * 0.82 + 2.5, 'DRONES DOWNED', 7.5, WHITE, 1, 'c')

def flag(x, y, w, h, kind):
    frame(x, y, w, h, DGREY, 1)
    if kind == 0:
        rect(x, y, w, h, WHITE)
        for i in range(4): rect(x, y + i * h / 4, w, h / 8, RED)
        rect(x, y, w * 0.45, h * 0.55, NAVY)
    elif kind == 1:
        rect(x, y, w, h / 3, ORANGE); rect(x, y + h / 3, w, h / 3, WHITE); rect(x, y + 2 * h / 3, w, h / 3, GREEN)
        circ(x + w / 2, y + h / 2, h / 7, NAVY, False)
    elif kind == 2:
        rect(x, y, w, h, WHITE); circ(x + w / 2, y + h / 2, h / 4, RED)
    else:
        rect(x, y, w, h, NAVY); circ(x + w * 0.7, y + h * 0.4, 3, WHITE); circ(x + w * 0.3, y + h * 0.65, 2, WHITE)
        line(x, y, x + w * 0.4, y + h * 0.5, RED, 2); line(x, y + h * 0.5, x + w * 0.4, y, WHITE, 1)

def sc_quad(x, y, w, h):
    rect(x, y, w, h, (214, 228, 240)); rect(x, y + h * 0.68, w, h * 0.32, BROWN)
    rect(x + 6, y + 5, w - 12, 15, NAVY); text(x + w / 2, y + 8, 'QUAD SUMMIT - MANILA', 9, WHITE, 1, 'c')
    fw = (w - 40) / 4
    for i in range(4): flag(x + 8 + i * (fw + 8), y + 26, fw, 22, i)
    rect(x + w * 0.18, y + h * 0.66, w * 0.64, 7, DGREY)
    for i, col in enumerate([NAVY, ORANGE, RED, BLUE]):
        person(x + w * (0.28 + i * 0.15), y + h * 0.44, 1.1, col)

def sc_ebola(x, y, w, h):
    rect(x, y, w, h, (238, 226, 210))
    vx, vy = x + w * 0.30, y + h * 0.42
    circ(vx, vy, 15, PURPLE)
    for a in range(10):
        ex = vx + 19 * math.cos(a * 0.63); ey = vy + 19 * math.sin(a * 0.63)
        line(vx, vy, ex, ey, PURPLE, 2); circ(ex, ey, 3, PURPLE)
    circ(vx - 5, vy - 4, 3, PINK); circ(vx + 6, vy + 5, 3, PINK)
    rect(x + w * 0.66, y + h * 0.10, w * 0.30, h * 0.42, WHITE); frame(x + w * 0.66, y + h * 0.10, w * 0.30, h * 0.42, DGREY, 1)
    rect(x + w * 0.79, y + h * 0.16, 5, 14, RED); rect(x + w * 0.755, y + h * 0.235, 12, 5, RED)
    text(x + w * 0.81, y + h * 0.42, 'CLINIC', 6.5, INK, 1, 'c')
    for i, bh in enumerate([8, 14, 24]):
        rect(x + w * (0.56 + i * 0.13), y + h * 0.94 - bh, 10, bh, RED)

def sc_cop(x, y, w, h):
    rect(x, y, w, h, SKY); circ(x + w * 0.34, y + h * 0.44, 20, BLUE)
    circ(x + w * 0.27, y + h * 0.36, 7, LGREEN); circ(x + w * 0.42, y + h * 0.52, 6, LGREEN)
    poly([(x + w * 0.60, y + h * 0.14), (x + w * 0.94, y + h * 0.14), (x + w * 0.88, y + h * 0.6), (x + w * 0.64, y + h * 0.52)], WHITE)
    line(x + w * 0.77, y + h * 0.16, x + w * 0.74, y + h * 0.55, RED, 2)
    for i in range(3): line(x + w * 0.65, y + h * (0.24 + i * 0.11), x + w * 0.86, y + h * (0.24 + i * 0.11), LGREY, 2)
    text(x + w * 0.77, y + h * 0.68, 'DRAFT TORN', 7.5, RED, 1, 'c')
    text(x + 6, y + h - 12, 'ANTALYA', 7.5, INK, 1)

def sc_measles(x, y, w, h):
    rect(x, y, w, h, (226, 236, 244))
    sx, sy = x + w / 2, y + h * 0.44
    poly([(sx - 20, sy - 20), (sx + 20, sy - 20), (sx + 20, sy + 4), (sx, sy + 26), (sx - 20, sy + 4)], TEAL)
    rect(sx - 4, sy - 13, 8, 22, WHITE); rect(sx - 11, sy - 6, 22, 8, WHITE)
    line(sx - 14, sy - 16, sx + 2, sy + 2, RED, 3); line(sx + 4, sy + 4, sx + 16, sy + 20, RED, 3)
    text(x + w / 2, y + h - 12, 'US - MEXICO - BOLIVIA', 7, RED, 1, 'c')

def sc_nvidia(x, y, w, h):
    rect(x, y, w, h, (30, 34, 44))
    for i, bh in enumerate([10, 18, 30, 44]):
        rect(x + 10 + i * 20, y + h - 14 - bh, 13, bh, GREEN if i == 3 else LGREEN)
    rect(x + w * 0.58, y + 10, 34, 26, DGREY); frame(x + w * 0.58, y + 10, 34, 26, GOLD, 2)
    text(x + w * 0.58 + 17, y + 19, 'AI', 11, GOLD, 1, 'c')
    line(x + w * 0.60, y + h - 20, x + w * 0.88, y + h - 34, RED, 3)
    poly([(x + w * 0.88, y + h - 34), (x + w * 0.80, y + h - 36), (x + w * 0.86, y + h - 26)], RED)
    text(x + w - 8, y + 8, 'DOW -849', 9, RED, 1, 'r')

def sc_gaza(x, y, w, h):
    rect(x, y, w, h, (198, 206, 214))
    for i in range(14): line(x + i * 13, y + 2, x + i * 13 - 5, y + 12, BLUE, 1)
    for i, tx in enumerate([0.14, 0.38, 0.60]):
        poly([(x + w * tx - 16, y + h * 0.72), (x + w * tx, y + h * 0.40), (x + w * tx + 16, y + h * 0.72)], (240, 234, 214))
        frame(x + w * tx - 16, y + h * 0.40, 32, h * 0.32, BROWN, 1)
    rect(x + w * 0.76, y + h * 0.52, 30, 16, WHITE); frame(x + w * 0.76, y + h * 0.52, 30, 16, DGREY, 1)
    rect(x + w * 0.82, y + h * 0.56, 7, 7, RED)
    circ(x + w * 0.80, y + h * 0.72, 4, INK); circ(x + w * 0.99, y + h * 0.72, 4, INK)
    text(x + w * 0.88, y + h * 0.30, 'AID HELD', 8, RED, 1, 'c')

def sc_mongolia(x, y, w, h):
    rect(x, y, w, h, SKY); rect(x, y + h * 0.7, w, h * 0.3, SAND)
    rect(x + 8, y + h * 0.24, w * 0.4, h * 0.42, WHITE); frame(x + 8, y + h * 0.24, w * 0.4, h * 0.42, DGREY, 1)
    for i in range(3): rect(x + 14 + i * 13, y + h * 0.32, 8, 10, BLUE)
    poly([(x + w * 0.60, y + h * 0.66), (x + w * 0.76, y + h * 0.34), (x + w * 0.92, y + h * 0.66)], CREAM)
    frame(x + w * 0.60, y + h * 0.34, w * 0.32, h * 0.32, BROWN, 1)
    person(x + w * 0.52, y + h * 0.52, 1.0, NAVY)
    line(x + w * 0.52, y + h * 0.46, x + w * 0.44, y + h * 0.40, INK, 2)
    text(x + w * 0.97, y + 4, 'RESIGNS', 8, RED, 1, 'r')

def sc_serbia(x, y, w, h):
    rect(x, y, w, h, (232, 228, 214))
    rect(x + w * 0.24, y + 6, w * 0.52, h * 0.4, LGREY); frame(x + w * 0.24, y + 6, w * 0.52, h * 0.4, DGREY, 1)
    poly([(x + w * 0.20, y + 8), (x + w * 0.5, y - 2), (x + w * 0.80, y + 8)], BROWN)
    for i in range(4): rect(x + w * (0.30 + i * 0.11), y + 14, 7, 9, NAVY)
    for i in range(7): circ(x + 12 + i * (w - 24) / 6, y + h * 0.64, 4, [RED, BLUE, GREEN, ORANGE, TEAL, PURPLE, NAVY][i])
    rect(x + w * 0.28, y + h * 0.76, w * 0.44, 12, INK)
    text(x + w / 2, y + h * 0.76 + 2, 'VOTE 140 - 103', 8, WHITE, 1, 'c')

def sc_dhaka(x, y, w, h):
    rect(x, y, w, h, (226, 220, 204))
    rect(x + 6, y + 8, w * 0.44, h * 0.5, GREY)
    for r in range(2):
        for i in range(3): rect(x + 11 + i * 12, y + 13 + r * 14, 8, 9, GOLD)
    circ(x + w * 0.72, y + h * 0.24, 12, (170, 176, 160)); circ(x + w * 0.82, y + h * 0.18, 9, (170, 176, 160))
    rect(x + w * 0.18, y + h * 0.60, w * 0.64, 14, RED)
    text(x + w / 2, y + h * 0.60 + 2.5, 'TK 30,000 NOW', 9, WHITE, 1, 'c')
    for i in range(6): person(x + 16 + i * (w - 32) / 5, y + h * 0.76, 0.62, [TEAL, ORANGE, PURPLE, GREEN, NAVY, PINK][i])

def sc_an12(x, y, w, h):
    rect(x, y, w, h, (206, 218, 230)); rect(x, y + h * 0.62, w, h * 0.38, WHITE)
    bx, by = x + w * 0.46, y + h * 0.52
    poly([(bx - 42, by), (bx + 30, by - 12), (bx + 44, by), (bx + 28, by + 8), (bx - 30, by + 8)], DGREY)
    rect(bx - 40, by - 3, 66, 4, RED)
    poly([(bx - 6, by - 4), (bx + 16, by - 22), (bx + 26, by - 20), (bx + 12, by - 2)], GREY)
    circ(bx + 34, by - 2, 5, INK); line(bx + 34, by - 12, bx + 34, by + 8, INK, 2)
    line(bx - 30, by + 8, bx - 44, by + 18, DGREY, 3)
    for i in range(8): circ(x + 10 + i * (w - 20) / 7, y + 8 + (i % 3) * 4, 2, WHITE)
    text(x + 6, y + 5, 'SIBERIA', 7.5, INK, 1)

def sc_mondlane(x, y, w, h):
    rect(x, y, w, h, (238, 232, 216))
    rect(x + 8, y + h * 0.20, w * 0.46, h * 0.5, LGREY); frame(x + 8, y + h * 0.20, w * 0.46, h * 0.5, DGREY, 1)
    poly([(x + 4, y + h * 0.20), (x + w * 0.27, y + h * 0.08), (x + w * 0.58, y + h * 0.20)], BROWN)
    rect(x + w * 0.22, y + h * 0.32, 10, 16, BROWN)
    sx = x + w * 0.74
    line(sx, y + h * 0.16, sx, y + h * 0.52, INK, 2); line(sx - 14, y + h * 0.22, sx + 14, y + h * 0.22, INK, 2)
    poly([(sx - 20, y + h * 0.38), (sx - 8, y + h * 0.38), (sx - 14, y + h * 0.30)], GOLD)
    poly([(sx + 8, y + h * 0.38), (sx + 20, y + h * 0.38), (sx + 14, y + h * 0.30)], GOLD)
    rect(sx - 8, y + h * 0.52, 16, 5, INK)
    poly([(x + w * 0.60, y + h * 0.78), (x + w * 0.95, y + h * 0.78), (x + w * 0.90, y + h * 0.92), (x + w * 0.65, y + h * 0.92)], GREEN)
    line(x + w * 0.62, y + h * 0.85, x + w * 0.93, y + h * 0.85, GOLD, 2)

SCENES = [None, sc_bridge, sc_gulf, sc_quad, sc_ebola, sc_cop, sc_measles,
          sc_nvidia, sc_gaza, sc_mongolia, sc_serbia, sc_dhaka, sc_an12, sc_mondlane]

FEATURES = [
 (4, 'AFRICA - HEALTH', 'EBOLA PASSES 11,000 IN DR CONGO', 'Clinics fill as WHO teams race to trace contacts in the east.'),
 (5, 'GLOBAL - CLIMATE', 'COP31 DRAFT TORN UP', 'Negotiators scrap the text and start again, two days left.'),
 (6, 'AMERICAS - HEALTH', 'AMERICAS LOSE MEASLES STATUS', 'US, Mexico and Bolivia lose status after long outbreaks.'),
 (7, 'WORLD - MARKETS', 'NVIDIA $115.8BN; DOW -849', 'Chip sales up 103% fail to lift a sliding Dow, off 1.6%.'),
 (8, 'MIDDLE EAST - AID', 'GAZA AID HELD AS RAIN BITES', 'Convoys wait while flooded tent camps face a cold night.'),
 (9, 'ASIA - POLITICS', 'MONGOLIA PRESIDENT RESIGNS', 'President quits after a parliament clash in Ulaanbaatar.'),
 (10, 'EUROPE - POLITICS', 'SERBIA GOVERNMENT SURVIVES', 'Ministers win the no-confidence vote; students protest.'),
 (11, 'ASIA - LABOUR', 'DHAKA GARMENT WORKERS MARCH', 'Thousands demand Tk 30,000; tear gas near factories.'),
 (12, 'EUROPE - DISASTER', 'RUSSIAN AN-12 PLANE CRASHES', 'Freighter down in Siberian snow; rescuers at the site.'),
 (13, 'AFRICA - JUSTICE', 'MONDLANE TRIAL OPENS', 'Opposition leader in Maputo court; backers wave ribbons.'),
]

ONELINERS = [
 'EU agrees 45bn euro loan for Ukraine',
 'Knesset elects Kahana 66-52',
 'China-Canada farm tariff cuts',
 'Britain sanctions settler firms',
 'Cyclone Akvan strengthens off Oman',
 'JPMorgan fixes morning outage',
 'EU migrant hub deal with Egypt',
 'India private orbital rocket flies',
 'Japan exports beat forecasts',
 'Sydney drifting bushfire smoke',
 'Brazil coffee hit by drought',
 'Seoul court upholds media law',
 'Turkey inflation eases to 31%',
 'Naira steadies after bank move',
 'Chile copper strike ends',
 'France rail strike called off',
 'Germany orders air defence kit',
 'Italy recovers stolen paintings',
 'Valencia clears flood drains',
 'Pakistan-IMF staff deal reached',
 'Indonesia volcano alert raised',
 'Vietnam typhoon weakens at land',
 'Thailand approves Laos rail link',
 'Argentina inflation falls again',
 'Mexico expands Pacific port',
 'Kenya moves marathon trials',
 'Egypt opens grand museum halls',
 'Norway fund exits coal firms',
 'Iceland fissure lengthens',
 'Wellington quake: no damage',
 'Canada fire crews head home',
 'Oil slips as OPEC weighs rise',
 'WHO warns on Sudan cholera',
]

STATS = [('2 DAYS', 'STRIKES ON THE CRIMEAN BRIDGE'),
         ('11,000+', 'EBOLA CASES IN DR CONGO'),
         ('$115.8BN', 'NVIDIA QUARTERLY SALES, UP 103%'),
         ('-849', 'DOW FALL (-1.6%)')]

# ------------------------------ page layout --------------------------------
rect(0, 0, W, H, PAPER)
rect(0, 0, W, 20, NAVY)
text(12, 5, "THE WORLD'S NEWS IN ONE PICTURE", 9, WHITE, 1)
text(W - 12, 5, '45+ STORIES - 6 CONTINENTS - ALL FROM TUESDAY', 9, WHITE, 1, 'r')
text(W / 2, 26, 'THE DAILY MERIDIAN', 25, INK, 1, 'c')
rect(10, 56, W - 20, 2, INK)
rect(10, 60, W - 20, 46, (28, 30, 38))
text(W / 2, 68, 'TUESDAY 17 NOVEMBER 2026', 31, (248, 240, 214), 1, 'c')
rect(10, 110, W - 20, 2, INK)

LEADS = [
 (1, 'EUROPE - WAR', 'KERCH BRIDGE STRUCK FOR A SECOND DAY', 'KERCH STRAIT - STRUCK FOR A SECOND DAY'),
 (2, 'MIDDLE EAST - WAR', 'IRAN DRONES DOWNED NEAR BAHRAIN RADAR', 'GULF - DRONES DOWNED OVER THE STRAIT'),
 (3, 'ASIA - DIPLOMACY', 'QUAD LEADERS MEET IN MANILA', 'MANILA - FIRST QUAD SUMMIT IN TWO YEARS'),
]
for i, (n, kick, head, cap) in enumerate(LEADS):
    x = 10 + i * 338; y = 118; w = 332
    frame(x, y, w, 186, INK, 2); chip(x + 5, y + 5, n, RED)
    text(x + 27, y + 7, kick, 9, RED, 1)
    SCENES[n](x + 4, y + 24, w - 8, 96)
    yy = para(x + 7, y + 124, head, 11.5, w - 14, INK, 14, 1)
    rect(x + 4, y + 158, w - 8, 22, INK)
    text(x + w / 2, y + 164, cap, 9.5, WHITE, 1, 'c')

for idx, (n, kick, head, summ) in enumerate(FEATURES):
    row = 0 if idx < 5 else 1; col = idx % 5
    x = 10 + col * 202; y = 312 + row * 172; w = 196
    frame(x, y, w, 164, INK, 1); chip(x + 4, y + 4, n, NAVY)
    text(x + 25, y + 6, kick, 7, RED, 1)
    SCENES[n](x + 4, y + 21, w - 8, 58)
    yy = para(x + 6, y + 84, head, 9.5, w - 12, INK, 12, 1)
    para(x + 6, yy + 4, summ, 7.2, w - 12, DGREY, 9.4)

# bottom: map left, also-list right
by = 656
text(10, by, 'WHERE IT HAPPENED - STORIES 1-13', 11, INK, 1)
text(512, by, 'ALSO ON TUESDAY 17 NOVEMBER', 11, INK, 1)
rect(10, by + 16, 490, 1, INK); rect(512, by + 16, 502, 1, INK)
MAP = (14, by + 22, 482, 196)
mx, my, mw, mh = MAP
rect(mx, my, mw, mh, SEA); frame(mx, my, mw, mh, NAVY, 1)
def M(lon, lat): return (mx + (lon + 170) / 360 * mw, my + (78 - lat) / 150 * mh)
def land(pts, c=LGREEN):
    poly([(M(a, b)[0], M(a, b)[1]) for a, b in pts], c)
land([(-168, 66), (-140, 70), (-125, 49), (-122, 37), (-105, 20), (-97, 16), (-87, 21), (-90, 29), (-81, 26), (-76, 35), (-65, 44), (-55, 47), (-70, 58), (-95, 69), (-168, 66)])
land([(-80, 9), (-77, -4), (-70, -10), (-60, -20), (-58, -30), (-65, -41), (-73, -50), (-75, -38), (-77, -15), (-80, -5)])
land([(-10, 36), (0, 44), (-2, 49), (5, 53), (10, 57), (18, 56), (24, 60), (30, 70), (45, 68), (60, 69), (30, 62), (28, 41), (22, 37), (12, 38), (3, 42), (-9, 43)])
land([(28, 41), (45, 68), (70, 72), (100, 77), (140, 72), (170, 66), (178, 62), (160, 55), (142, 50), (135, 35), (122, 30), (108, 20), (100, 8), (97, 16), (90, 22), (78, 8), (72, 20), (60, 25), (48, 29), (44, 38)])
land([(-17, 15), (-10, 5), (0, 6), (8, 4), (13, -12), (12, -18), (14, -26), (19, -34), (27, -34), (32, -26), (35, -18), (40, -10), (48, -5), (51, 2), (44, 11), (38, 18), (35, 28), (30, 31), (20, 32), (10, 34), (-5, 35), (-15, 27)])
land([(95, 5), (105, -2), (112, -3), (120, -8), (130, -12), (114, -22), (122, -34), (130, -32), (140, -38), (147, -39), (150, -22), (146, -12), (138, -5), (125, -2), (110, 2), (100, 6)])
land([(167, -45), (172, -41), (176, -37), (174, -41), (169, -46)])
PINS = [(34, 45), (51, 26), (121, 15), (23, -3), (30, 37), (-102, 38), (-74, 41),
        (34, 31), (105, 47), (21, 45), (90, 24), (87, 55), (32, -26)]
for i, (lo, la) in enumerate(PINS):
    px, py = M(lo, la); circ(px, py, 7, RED); text(px, py - 4.5, str(i + 1), 8, WHITE, 1, 'c')
LEG = [('AMERICAS', BLUE), ('EUROPE', PURPLE), ('MIDDLE EAST', RED), ('ASIA', TEAL),
       ('AFRICA', ORANGE), ('OCEANIA', GREEN), ('GLOBAL', GOLD)]
for i, (nm, c) in enumerate(LEG):
    lx = 14 + (i % 4) * 122; ly = my + mh + 8 + (i // 4) * 17
    rect(lx, ly, 10, 10, c); text(lx + 14, ly + 1, nm, 8, INK, 1)

colw = 248
for i, s in enumerate(ONELINERS):
    col = 0 if i < 17 else 1; r = i % 17
    x = 512 + col * (colw + 8); y = by + 24 + r * 15.4
    text(x, y, str(14 + i) + '.', 8, RED, 1)
    text(x + 22, y + 0.5, s, 7.0, INK)

sy = 942
rect(10, sy, W - 20, 38, INK)
for i, (big, small) in enumerate(STATS):
    x = 10 + i * 251
    if i: rect(x, sy, 1, 38, (90, 92, 100))
    text(x + 8, sy + 4, big, 13, GOLD, 1)
    text(x + 8, sy + 22, small, 7.5, WHITE, 1)
rect(10, 986, W - 20, 1, INK)
text(W / 2, 991, 'EVERY STORY HERE HAPPENED OR WAS FIRST REPORTED ON TUESDAY 17 NOVEMBER 2026. CONTESTED CLAIMS ARE MARKED AS CLAIMS.', 8, INK, 1, 'c')
text(W / 2, 1004, 'SOURCES: REUTERS, AP, AFP, BBC, AL JAZEERA, WHO, UN. ORIGINAL DRAWINGS.', 8, DGREY, 0, 'c')

# deterministic grain
for yy in range(H):
    base = yy * W * 3
    for xx in range(W):
        v = ((xx * 73856093) ^ (yy * 19349663)) & 0xffff
        d = (v % 7) - 3
        i = base + xx * 3
        for k in range(3):
            nv = PX[i + k] + d
            PX[i + k] = 0 if nv < 0 else (255 if nv > 255 else nv)

def chunk(tag, data):
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

raw = b''.join(b'\x00' + bytes(PX[y * W * 3:(y + 1) * W * 3]) for y in range(H))
png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
outdir = os.environ.get('MAKEFUN_OUTPUT_DIR', '.')
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, 'entry.png'), 'wb') as f:
    f.write(png)
print('wrote', os.path.join(outdir, 'entry.png'), len(png), 'bytes')

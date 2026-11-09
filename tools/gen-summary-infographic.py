#!/usr/bin/env python3
"""Regenerate the summary infographic for the Blue Archive gacha post.

Deterministic PIL render (not an image model) so Vietnamese text is exact.
Output: src/assets/blog/blue-archive-new-gacha-mechanics-personal-thoughts-06.png (1024x1536)
Usage: python3 tools/gen-summary-infographic.py
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib

W, H = 1024, 1536
BG = (11, 11, 15)
PANEL = (23, 23, 31)
BORDER = (42, 42, 54)
WHITE = (242, 242, 245)
MUTED = (161, 161, 170)
PINK = (255, 61, 145)
BLUE = (74, 144, 217)
BLUE_DK = (30, 58, 95)
PURPLE = (168, 85, 247)
PURPLE_DK = (59, 30, 95)
GREEN = (52, 211, 153)
GREEN_DK = (20, 70, 55)
AMBER = (251, 191, 36)
AMBER_DK = (70, 50, 10)

FDIR = "/usr/share/fonts/truetype/dejavu/"
def fb(sz): return ImageFont.truetype(FDIR + "DejaVuSans-Bold.ttf", sz)
def fr(sz): return ImageFont.truetype(FDIR + "DejaVuSans.ttf", sz)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")
MX = 40           # side margin
CW = W - 2 * MX   # content width
y = 34

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(text, font, x, y, max_w, fill=WHITE, lh=None):
    lh = lh or int(font.size * 1.35)
    for line in wrap(text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y

def bullets(items, font, x, y, max_w, bullet="•", bfill=PINK, lh=None):
    lh = lh or int(font.size * 1.45)
    for it in items:
        d.text((x, y), bullet, font=font, fill=bfill)
        y = text_block(it, font, x + 24, y, max_w - 24, lh=lh)
        y += 2
    return y

def panel_header(title, color, dark, x, y, w):
    d.rounded_rectangle([x, y, x + w, y + 46], radius=10, fill=dark)
    d.rounded_rectangle([x, y, x + w, y + 46], radius=10, outline=color, width=2)
    d.text((x + 16, y + 11), title, font=fb(22), fill=color)
    return y + 46

def panel_box(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=PANEL, outline=BORDER, width=2)

# ---------- header ----------
d.text((MX, y), "TỔNG KẾT", font=fb(26), fill=PINK)
y += 40
d.text((MX, y), "CƠ CHẾ GACHA BLUE ARCHIVE", font=fb(40), fill=WHITE)
y += 58
d.text((MX, y), "Cơ chế cũ ", font=fb(24), fill=BLUE)
w1 = d.textlength("Cơ chế cũ ", font=fb(24))
d.text((MX + w1, y), "(Spark 200)", font=fb(24), fill=MUTED)
w2 = d.textlength("(Spark 200)", font=fb(24))
d.text((MX + w1 + w2, y), "  vs  ", font=fb(24), fill=WHITE)
w3 = d.textlength("  vs  ", font=fb(24))
d.text((MX + w1 + w2 + w3, y), "Cơ chế mới ", font=fb(24), fill=PURPLE)
w4 = d.textlength("Cơ chế mới ", font=fb(24))
d.text((MX + w1 + w2 + w3 + w4, y), "(Stack 100/200 + Mileage)", font=fb(24), fill=MUTED)
y += 46

# ---------- row 1: old vs new ----------
ROW1_H = 404
py = y
pw = (CW - 24) // 2
# old panel
panel_box(MX, py, pw, ROW1_H)
hy = panel_header("1 · CƠ CHẾ CŨ — SPARK 200", BLUE, BLUE_DK, MX + 12, py + 12, pw - 24)
by = hy + 16
by = bullets([
    "Mỗi lần quay = 1 Recruitment Point.",
    "200 điểm → đổi 1 pickup, tự chọn.",
    "Trúng pickup: điểm KHÔNG reset.",
    "Hết banner: điểm mất giá trị.",
], fr(20), MX + 24, by, pw - 48, bfill=BLUE)
# bar
bar_y = py + ROW1_H - 78
bx0, bx1 = MX + 24, MX + pw - 24
d.line([bx0, bar_y, bx1, bar_y], fill=BLUE, width=4)
for bx, lab in [(bx0, "0"), (bx1, "200")]:
    d.ellipse([bx - 7, bar_y - 7, bx + 7, bar_y + 7], fill=BLUE)
    d.text((bx - 6, bar_y + 14), lab, font=fb(18), fill=MUTED)
d.text((bx0 + 60, bar_y - 34), "200 điểm → đổi 1 PU (tự chọn)", font=fb(19), fill=WHITE)
# new panel
nx = MX + pw + 24
panel_box(nx, py, pw, ROW1_H)
hy = panel_header("2 · CƠ CHẾ MỚI — STACK 100/200", PURPLE, PURPLE_DK, nx + 12, py + 12, pw - 24)
by = hy + 16
by = bullets([
    "100 Stack: chắc chắn 3★, 50% là pickup.",
    "200 Stack: đúng pickup của banner.",
    "Trúng pickup: Stack reset về 0.",
    "3★ lệch: Stack KHÔNG reset.",
    "2 Stack riêng: thường / đặc biệt–FES.",
    "Chưa ra pickup: Stack mang sang kỳ sau.",
], fr(19), nx + 24, by, pw - 48, bfill=PURPLE)
bar_y = py + ROW1_H - 78
bx0, bx1 = nx + 24, nx + pw - 24
bxm = (bx0 + bx1) // 2
d.line([bx0, bar_y, bx1, bar_y], fill=PURPLE, width=4)
for bx, lab in [(bx0, "0"), (bxm, "100"), (bx1, "200")]:
    d.ellipse([bx - 7, bar_y - 7, bx + 7, bar_y + 7], fill=PURPLE)
    d.text((bx - 14, bar_y + 14), lab, font=fb(18), fill=MUTED)
d.text((bxm - 52, bar_y - 34), "50% PU", font=fb(19), fill=PURPLE)
d.text((bx1 - 82, bar_y - 34), "100% PU", font=fb(19), fill=PURPLE)
y = py + ROW1_H + 20

# ---------- panel 3: mileage ----------
P3_H = 186
panel_box(MX, y, CW, P3_H)
hy = panel_header("3 · MILEAGE — THƯỞNG THEO KỲ", GREEN, GREEN_DK, MX + 12, y + 12, CW - 24)
by = hy + 16
by = bullets([
    "Vé 10 lượt ở các mốc 70 · 130 · 150 · 170 · 270 · 330 · 350 · 370 — tối đa 8 vé = 80 lượt/kỳ.",
    "Hết kỳ: Mileage về 0 — vé chưa nhận thì mất.",
    "Hard pity thực chi: 160 lần đá = 19.200 Pyroxene (thay vì 24.000).",
], fr(20), MX + 24, by, CW - 48, bfill=GREEN)
y += P3_H + 20

# ---------- panel 4: probability ----------
P4_H = 238
panel_box(MX, y, CW, P4_H)
hy = panel_header("4 · XÁC SUẤT NÓI GÌ — SO THEO CÙNG LƯỢNG ĐÁ", PINK, (60, 16, 36), MX + 12, y + 12, CW - 24)
by = hy + 18
col_w = (CW - 72) // 2
# left
d.text((MX + 24, by), "SĂN 1 PICKUP", font=fb(20), fill=BLUE)
by2 = by + 34
by2 = text_block("100 lần đá:  50,5% → 76,7%", fb(22), MX + 24, by2, col_w)
by2 = text_block("Đá trung bình tới pickup: 108 → 79", fr(19), MX + 24, by2 + 4, col_w, fill=MUTED)
# right
rx = MX + 24 + col_w + 24
d.text((rx, by), "SĂN 2 PICKUP", font=fb(20), fill=PURPLE)
by2 = by + 34
by2 = text_block("200 lần đá:  75,5% → 76,8%", fb(22), rx, by2, col_w)
by2 = text_block("Trần đủ cặp: 320 đá + 80 vé", fr(19), rx, by2 + 4, col_w, fill=MUTED)
# warning line
wy = y + P4_H - 46
d.rounded_rectangle([MX + 12, wy - 8, MX + CW - 12, wy + 34], radius=8, fill=AMBER_DK)
text_block("⚠  Con số 64,1% < 75,5% là bẫy đọc: so theo tổng lượt quay (200), không cùng lượng đá.",
           fr(19), MX + 28, wy, CW - 56, fill=AMBER)
y += P4_H + 20

# ---------- panel 5: thresholds & player types ----------
P5_H = 252
panel_box(MX, y, CW, P5_H)
hy = panel_header("5 · NGƯỠNG SUZUMI & KIỂU NGƯỜI CHƠI", AMBER, AMBER_DK, MX + 12, y + 12, CW - 24)
by = hy + 18
d.text((MX + 24, by), "Suzumi ra ở lượt x → người thứ 2:", font=fb(20), fill=WHITE)
by += 34
by = bullets([
    "x ≤ 40: còn đủ ngân sách bảo đảm.",
    "41 ≤ x ≤ 140: chỉ còn mốc 50/50.",
    "x > 140: hết pity trong kỳ — Stack mang sang kỳ sau.",
], fr(20), MX + 24, by, col_w, bfill=AMBER)
d.text((rx, hy + 18), "Đá cho 1 học sinh (cũ → mới):", font=fb(20), fill=WHITE)
by2 = hy + 18 + 34
by2 = bullets([
    "Chia nhỏ <70 lần: 143 → 90 (−36,9%).",
    "Gom 200 lần: 108 → 79 (−26,7%).",
    "Trùng 1.000 đá: 83 → 85 (+2,5%) — ngoại lệ duy nhất.",
], fr(20), rx, by2, col_w, bfill=GREEN)
y += P5_H + 20

# ---------- footer: verdict ----------
F_H = 168
d.rounded_rectangle([MX, y, MX + CW, y + F_H], radius=12, fill=(16, 28, 66), outline=BLUE, width=2)
d.text((MX + 24, y + 16), "KẾT LUẬN", font=fb(22), fill=BLUE)
fy = y + 52
fy = text_block(
    "Cơ chế mới là hệ thống pity tốt hơn, và là hệ thống xác suất tốt hơn ở cùng lượng đá — "
    "nhưng là công cụ lập kế hoạch chắc chắn tệ hơn.",
    fb(23), MX + 24, fy, CW - 48)
d.text((MX + 24, y + F_H - 30),
       "Số liệu theo 11 slide cải tổ hệ thống chiêu mộ · Global 10/11/2026 · blog.dh6k.vip",
       font=fr(16), fill=MUTED)
print("final y:", y + F_H, "canvas:", H)

out = pathlib.Path.home() / "workspace/hashnode-astro-export/src/assets/blog/blue-archive-new-gacha-mechanics-personal-thoughts-06.png"
img.save(out)
print("saved:", out, img.size)

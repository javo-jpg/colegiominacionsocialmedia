import sys, os, json
sys.path.insert(0, "/home/claude/scripts")
from design import *
DECO = deco

OUT = "/home/claude/colegiominacionsocialmedia/assets/2026-11/"
def PH(name): return Image.open(M + name).convert("RGB")
def save(im, slug, n):
    d = OUT + slug + "/"; os.makedirs(d, exist_ok=True); im.convert("RGB").save(d + f"{n:02d}.jpg", quality=92)

# ---------------- layouts ----------------
def L_photo_panel(photo, eyebrow_t, title, sub=None, bg=G, fg=C, acc=Y, focus=(.5, .5), ph=780, n=0, i=0, swipe_=False, tag=None):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    im.paste(cover(photo, W, ph, focus), (0, 0))
    if tag: pill(d, (60, 60), tag, font(SB, 28), acc, bg if acc != bg else fg)
    y = ph + 56
    eyebrow(d, (80, y), eyebrow_t, acc); y += 54
    f = fit_font(d, title, MIJA, W - 160, 3, 84, 52)
    y = text_block(d, (80, y), title, f, fg, W - 160, 1.08)
    if sub: text_block(d, (80, y + 14), sub, font(SL, 34), fg, W - 160, 1.3)
    if swipe_: swipe(d, acc)
    page_dots(d, n, i, H - 40, acc, tuple(int(c * .6 + b * .4) for c, b in zip(bg, fg)))
    return im

def L_photo_full(photo, eyebrow_t, title, sub=None, focus=(.5, .5), acc=Y, n=0, i=0, swipe_=False, logo_=True):
    im = cover(photo, W, H, focus).convert("RGBA")
    grad = Image.new("L", (1, H)); [grad.putpixel((0, y), int(max(0, (y - H * .38) / (H * .62)) ** 1.3 * 235)) for y in range(H)]
    shade = Image.new("RGBA", (W, H), (20, 52, 44, 255)); shade.putalpha(grad.resize((W, H))); im.alpha_composite(shade)
    d = ImageDraw.Draw(im)
    f = fit_font(d, title, MIJA, W - 160, 3, 92, 56)
    lines = wrap(d, title, f, W - 160); th = len(lines) * f.size * 1.08
    subh = 0
    if sub: subh = len(wrap(d, sub, font(SL, 36), W - 160)) * 36 * 1.3 + 16
    y = H - 150 - th - subh
    eyebrow(d, (80, y - 54), eyebrow_t, acc)
    y = text_block(d, (80, y), title, f, C, W - 160, 1.08)
    if sub: text_block(d, (80, y + 16), sub, font(SL, 36), LG, W - 160, 1.3)
    if logo_: lg = logo("verdeclaro", 200); im.alpha_composite(lg, (80, 64)) if False else im.paste(lg, (80, 64), lg)
    if swipe_: swipe(d, acc, H - 70)
    page_dots(d, n, i, H - 40, acc, (120, 140, 130))
    return im

def L_type(bg, fg, acc, eyebrow_t, title, body=None, ic=None, n=0, i=0, swipe_=False, big=110, deco=True, foot=True):
    _deco = deco
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    if _deco: DECO(im, bg, acc, i + len(title)); d = ImageDraw.Draw(im)
    f = fit_font(d, title, MIJA, W - 160, 4, big, 64); tl = wrap(d, title, f, W - 160)
    fb = font(SL, 40); bl = wrap(d, body, fb, W - 170) if body else []
    hb = (190 if ic else 0) + 56 + len(tl) * f.size * 1.08 + (26 + len(bl) * 40 * 1.36 if body else 0)
    top, bot = 200, H - 190; y = top + max(0, (bot - top - hb) / 2)
    if ic:
        icn = icon(ic, 150, acc, bg); im.paste(icn, (80, int(y)), icn); y += 190
    eyebrow(d, (80, y), eyebrow_t, acc); y += 56
    y = text_block(d, (80, y), title, f, fg, W - 160, 1.08)
    if body: text_block(d, (80, y + 26), body, fb, fg, W - 170, 1.36)
    if foot:
        lg = logo("verdeclaro" if bg in (G, B, P) else "verde", 210); im.paste(lg, (80, H - lg.height - 64), lg)
    if swipe_: swipe(d, acc)
    page_dots(d, n, i, H - 40, acc, tuple(int(c * .55 + b * .45) for c, b in zip(bg, fg)))
    return im

def L_list(bg, fg, acc, eyebrow_t, title, items, n=0, i=0, card=(255, 255, 255), cardfg=INK):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    f = fit_font(d, title, MIJA, W - 160, 2, 84, 56); tl = len(wrap(d, title, f, W - 160))
    ch = min(230, (H - 330 - tl * f.size * 1.1 - 24 * (len(items) - 1)) / len(items))
    hb = 56 + tl * f.size * 1.08 + 40 + len(items) * (ch + 24)
    y = max(100, (H - 60 - hb) / 2); eyebrow(d, (80, y), eyebrow_t, acc); y += 56
    y = text_block(d, (80, y), title, f, fg, W - 160, 1.08) + 40
    for (ic, head, txt) in items:
        d.rounded_rectangle([80, y, W - 80, y + ch], radius=34, fill=card)
        icn = icon(ic, int(ch * .5), acc if card != acc else G, card); im.paste(icn, (116, int(y + ch * .25)), icn)
        tx = 116 + int(ch * .5) + 36
        d.text((tx, y + ch * .22), head, font=font(SB, 42), fill=cardfg)
        text_block(d, (tx, y + ch * .22 + 56), txt, font(SL, 32), cardfg, W - 80 - tx - 30, 1.25)
        y += ch + 24
    page_dots(d, n, i, H - 40, acc, tuple(int(c * .55 + b * .45) for c, b in zip(bg, fg)))
    return im

def L_phone(bg, fg, acc, shot, eyebrow_t, title, body=None, n=0, i=0, crop=None, swipe_=False):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    s = PH(shot)
    if crop: s = s.crop(crop)
    ph = phone_frame(s, 860)
    im.paste(ph, (W - ph.width + 40, H - ph.height + 230), ph) if False else None
    # text left top, phone bottom right
    y = 100; eyebrow(d, (80, y), eyebrow_t, acc); y += 56
    f = fit_font(d, title, MIJA, W - 160, 2, 80, 52); y = text_block(d, (80, y), title, f, fg, W - 160, 1.08)
    if body: y = text_block(d, (80, y + 18), body, font(SL, 34), fg, W - 160, 1.3)
    px = (W - ph.width) // 2; py = max(int(y) + 30, 420)
    im.paste(ph, (px, py), ph)
    if swipe_: swipe(d, acc)
    page_dots(d, n, i, H - 40, acc, tuple(int(c * .55 + b * .45) for c, b in zip(bg, fg)))
    return im

def L_cta(bg=C, fg=G, acc=G, title="¿Quieres conocer el colegio?", body="Pide informes y agenda tu visita. Te atendemos de 9:00 a. m. a 3:30 p. m.", n=0, i=0, btn="Pide informes"):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    DECO(im, bg, acc, i + 1); d = ImageDraw.Draw(im)
    y = 300; f = fit_font(d, title, MIJA, W - 160, 3, 90, 56); y = text_block(d, (80, y), title, f, fg, W - 160, 1.08)
    y = text_block(d, (80, y + 24), body, font(SL, 38), INK if bg == C else fg, W - 160, 1.34) + 40
    d.rounded_rectangle([80, y, 680, y + 100], radius=50, fill=acc)
    d.text((380, y + 50), btn, font=font(SB, 46), fill=C if acc == G else G, anchor="mm"); y += 140
    for ic, t in [("chat", "WhatsApp 56 5292 2720"), ("phone", "55 5911 1865"), ("globe", "colegiominacion.com")]:
        icn = icon(ic, 54, fg, bg); im.paste(icn, (80, int(y)), icn); d.text((154, y + 27), t, font=font(SB, 38), fill=fg, anchor="lm"); y += 74
    lg = logo("verde" if bg in (C, LG, Y) else "verdeclaro", 230); im.paste(lg, (80, H - lg.height - 64), lg)
    page_dots(d, n, i, H - 40, fg, (200, 200, 190))
    return im

# Zona segura Reels/Historias 1080x1920: texto solo en x 80-960 y y 270-1500.
# La cuadrícula del perfil recorta la portada a 3:4 (y 240-1680).
RSAFE = (80, 270, 960, 1500)
def L_reel_cover(photo, title, eyebrow_t, focus=(.5, .5), acc=Y, sub=None, bg=G, muertos=False):
    Wr, Hr, VH = 1080, 1920, 1080
    im = Image.new("RGB", (Wr, Hr), bg); im.paste(cover(photo, Wr, VH, focus), (0, 0)); d = ImageDraw.Draw(im)
    if muertos: picado(d, Wr, VH, 12, [Y, P, B, LG], bg, h=70)
    else: d.rectangle([0, VH, Wr, VH + 10], fill=acc); sparkle(d, Wr - 170, VH + 120, 34, acc); sparkle(d, Wr - 110, VH + 70, 14, acc)
    y = VH + 100; pill(d, (80, y), eyebrow_t, font(SB, 30), acc, G); y += 84
    f = fit_font(d, title, MIJA, RSAFE[2] - 80, 2, 84, 56)
    y = text_block(d, (80, y), title, f, C, RSAFE[2] - 80, 1.08)
    if sub: d.text((80, y + 8), sub, font=font(SL, 36), fill=LG); y += 50
    assert y <= RSAFE[3], ("reel cover fuera de zona segura", title, y)
    return im

def L_reel_card(bg, title, eyebrow_t, ic=None, sub=None):
    Wr, Hr = 1080, 1920
    im = Image.new("RGB", (Wr, Hr), bg); d = ImageDraw.Draw(im)
    DECO(im, bg, Y, len(title), top_only=True); d = ImageDraw.Draw(im)
    wm = eye(mix(bg, C, .1), 700); im.paste(wm, (Wr - 480, 1500), wm)
    lg = logo("verdeclaro", 240); im.paste(lg, (80, 300), lg)
    y = 560
    if ic: icn = icon(ic, 150, Y, bg); im.paste(icn, (80, y), icn); y += 185
    pill(d, (80, y), eyebrow_t, font(SB, 30), Y, G); y += 90
    f = fit_font(d, title, MIJA, RSAFE[2] - 80, 4, 100, 60); y = text_block(d, (80, y), title, f, C, RSAFE[2] - 80, 1.08)
    if sub: y = text_block(d, (80, y + 20), sub, font(SL, 38), LG, RSAFE[2] - 80, 1.3)
    assert y <= RSAFE[3], ("reel card fuera de zona segura", title, y)
    return im

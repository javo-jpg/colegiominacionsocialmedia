from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math, os, random
F = "/home/claude/zip/Entrega/Fonts/"
MIJA = F + "Mija W03 Regular.ttf"; SB = F + "Sohne-Kraftig.otf"; SL = F + "Sohne-Leicht.otf"
G = (35, 93, 78); LG = (220, 229, 182); Y = (237, 204, 111); B = (84, 158, 187); C = (252, 248, 239); P = (232, 131, 107); INK = (31, 43, 39)
M = "/home/claude/media/"; BR = "/home/claude/colegiominacionsocialmedia/brand/"
W, H = 1080, 1350

def font(p, s): return ImageFont.truetype(p, s)

def logo(color="verdeclaro", w=300):
    im = Image.open(BR + f"logo-horizontal-{color}.png").convert("RGBA"); im = im.crop(im.getbbox())
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)

_eye = None
def eye(col, w):
    global _eye
    if _eye is None:
        e = Image.open("/home/claude/zip/Entrega/png/ColgeioNacion--16.png").convert("RGBA"); _eye = e.crop(e.getbbox())
    a = _eye.split()[3]; s = Image.new("RGBA", _eye.size, col + (255,)); s.putalpha(a)
    return s.resize((w, int(w * _eye.height / _eye.width)), Image.LANCZOS)

def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w_ in para.split():
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else:
                if cur: out.append(cur)
                cur = w_
        out.append(cur)
    return out

def text_block(d, xy, text, f, fill, maxw, lh=1.18, anchor_center=False):
    x, y = xy
    for ln in wrap(d, text, f, maxw):
        if anchor_center: d.text((x, y), ln, font=f, fill=fill, anchor="ma")
        else: d.text((x, y), ln, font=f, fill=fill)
        y += f.size * lh
    return y

def fit_font(d, text, path, maxw, maxlines, start, minsize=40, lh=1.1):
    s = start
    while s > minsize:
        f = font(path, s)
        if len(wrap(d, text, f, maxw)) <= maxlines: return f
        s -= 4
    return font(path, minsize)

def cover(img, w, h, focus=(0.5, 0.5)):
    img = img.convert("RGB"); r = max(w / img.width, h / img.height)
    nw, nh = int(img.width * r + 0.5), int(img.height * r + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = int((nw - w) * focus[0]); y = int((nh - h) * focus[1])
    out = img.crop((x, y, x + w, y + h))
    if r > 1.05: out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    return out

def rmask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255); return m

def paste_round(base, img, xy, r=36):
    base.paste(img, xy, rmask(img.width, img.height, r))

def picado(d, W_, y0, n, cols, bg, h=None):
    fw = W_ / n; h = h or int(fw * 1.05)
    d.line([(0, y0), (W_, y0)], fill=cols[0], width=4)
    for i in range(n):
        x = i * fw + 8; c = cols[i % len(cols)]; top = y0 + 6; bot = y0 + h
        d.polygon([(x, top), (x + fw - 16, top), (x + fw - 16, bot), (x + (fw - 16) / 2, bot - 20), (x, bot)], fill=c)
        cx = x + (fw - 16) / 2; cy = (top + bot) / 2 - 6
        d.regular_polygon((cx, cy, 13), 4, rotation=45, fill=bg)
        d.ellipse([cx - 5, top + 10, cx + 5, top + 20], fill=bg)

def pill(d, xy, text, f, bg, fg, padx=30, h=None):
    x, y = xy; h = h or int(f.size * 1.9); w = d.textlength(text, font=f) + padx * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    d.text((x + w / 2, y + h / 2), text, font=f, fill=fg, anchor="mm"); return x + w

def eyebrow(d, xy, text, fg, size=30):
    f = font(SB, size); d.text(xy, text.upper(), font=f, fill=fg)

def page_dots(d, n, i, y, fg, dim):
    if n <= 1: return
    x0 = W / 2 - (n - 1) * 14
    for k in range(n):
        d.ellipse([x0 + k * 28 - 6, y - 6, x0 + k * 28 + 6, y + 6], fill=fg if k == i else dim)

def swipe(d, fg, y=H - 92):
    f = font(SB, 30); d.text((W - 150, y), "Desliza", font=f, fill=fg, anchor="rm")
    d.line([(W - 138, y), (W - 98, y)], fill=fg, width=5); d.polygon([(W - 98, y - 11), (W - 82, y), (W - 98, y + 11)], fill=fg)

def footer_logo(im, color="verdeclaro", y=None, w=230):
    lg = logo(color, w); y = y or H - lg.height - 64; im.paste(lg, (80, y), lg)

# ---------- icons (drawn) ----------
def icon(kind, size, fg, bg):
    s = size; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); lw = max(6, s // 14)
    if kind == "chat":
        d.rounded_rectangle([s*.12, s*.16, s*.88, s*.70], radius=s*.16, fill=fg)
        d.polygon([(s*.28, s*.66), (s*.24, s*.88), (s*.46, s*.68)], fill=fg)
        for k in range(3): d.ellipse([s*(.32+k*.14)-s*.04, s*.43-s*.04, s*(.32+k*.14)+s*.04, s*.43+s*.04], fill=bg)
    elif kind == "phone":
        d.rounded_rectangle([s*.28, s*.08, s*.72, s*.92], radius=s*.1, outline=fg, width=lw)
        d.line([(s*.42, s*.18), (s*.58, s*.18)], fill=fg, width=lw); d.ellipse([s*.46, s*.76, s*.54, s*.84], fill=fg)
    elif kind == "form":
        d.rounded_rectangle([s*.18, s*.08, s*.82, s*.92], radius=s*.08, outline=fg, width=lw)
        for k, w_ in enumerate([.5, .38, .5, .3]): d.line([(s*.3, s*(.28+k*.16)), (s*(.3+w_), s*(.28+k*.16))], fill=fg, width=lw)
    elif kind == "heart":
        r = s*.22; d.ellipse([s*.12, s*.18, s*.12+2*r, s*.18+2*r], fill=fg); d.ellipse([s*.88-2*r, s*.18, s*.88, s*.18+2*r], fill=fg)
        d.polygon([(s*.13, s*.45), (s*.87, s*.45), (s*.5, s*.86)], fill=fg)
    elif kind == "book":
        d.polygon([(s*.08, s*.22), (s*.48, s*.3), (s*.48, s*.86), (s*.08, s*.78)], fill=fg)
        d.polygon([(s*.92, s*.22), (s*.52, s*.3), (s*.52, s*.86), (s*.92, s*.78)], fill=fg)
    elif kind == "star":
        pts = [(s/2 + (s*.42 if k % 2 == 0 else s*.18) * math.cos(math.pi/2 + k*math.pi/5), s/2 - (s*.42 if k % 2 == 0 else s*.18) * math.sin(math.pi/2 + k*math.pi/5)) for k in range(10)]
        d.polygon(pts, fill=fg)
    elif kind == "pin":
        d.ellipse([s*.22, s*.08, s*.78, s*.64], fill=fg); d.polygon([(s*.28, s*.48), (s*.72, s*.48), (s*.5, s*.92)], fill=fg); d.ellipse([s*.4, s*.26, s*.6, s*.46], fill=bg)
    elif kind == "numbers":
        f = font(SB, int(s*.42)); d.text((s/2, s/2), "1+2", font=f, fill=fg, anchor="mm")
    elif kind == "letters":
        f = font(SB, int(s*.5)); d.text((s/2, s/2), "Aa", font=f, fill=fg, anchor="mm")
    elif kind == "leaf":
        d.ellipse([s*.18, s*.12, s*.82, s*.76], fill=fg); d.line([(s*.5, s*.3), (s*.5, s*.92)], fill=bg if bg else fg, width=lw)
        d.line([(s*.5, s*.9), (s*.5, s*.96)], fill=fg, width=lw)
    elif kind == "music":
        d.line([(s*.38, s*.2), (s*.38, s*.72)], fill=fg, width=lw); d.line([(s*.74, s*.12), (s*.74, s*.64)], fill=fg, width=lw)
        d.polygon([(s*.38-lw/2, s*.2), (s*.74+lw/2, s*.12), (s*.74+lw/2, s*.26), (s*.38-lw/2, s*.34)], fill=fg)
        d.ellipse([s*.18, s*.64, s*.42, s*.84], fill=fg); d.ellipse([s*.54, s*.56, s*.78, s*.76], fill=fg)
    elif kind == "bulb":
        d.ellipse([s*.24, s*.08, s*.76, s*.6], fill=fg); d.rectangle([s*.38, s*.56, s*.62, s*.74], fill=fg); d.rectangle([s*.4, s*.78, s*.6, s*.86], fill=fg)
    elif kind == "calendar":
        d.rounded_rectangle([s*.12, s*.18, s*.88, s*.88], radius=s*.08, outline=fg, width=lw); d.rectangle([s*.12, s*.18, s*.88, s*.36], fill=fg)
        for k in range(3):
            for j in range(2): d.rectangle([s*(.24+k*.2), s*(.48+j*.18), s*(.34+k*.2), s*(.58+j*.18)], fill=fg)
    elif kind == "globe":
        d.ellipse([s*.1, s*.1, s*.9, s*.9], outline=fg, width=lw); d.ellipse([s*.32, s*.1, s*.68, s*.9], outline=fg, width=lw)
        d.line([(s*.1, s*.5), (s*.9, s*.5)], fill=fg, width=lw)
    return im

def phone_frame(shot, h_target):
    """screenshot inside a rounded phone frame"""
    sw = int(shot.width * h_target / shot.height); shot = shot.resize((sw, h_target), Image.LANCZOS)
    pad = 18; fw, fh = sw + pad * 2, h_target + pad * 2
    im = Image.new("RGBA", (fw + 40, fh + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([24, 30, fw + 16, fh + 26], radius=64, fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(sh)
    ImageDraw.Draw(im).rounded_rectangle([20, 20, fw + 20, fh + 20], radius=60, fill=(22, 30, 27, 255))
    im.paste(shot, (20 + pad, 20 + pad), rmask(sw, h_target, 44))
    return im

# ---------- elementos neutrales del sitio (para todo lo que no es Día de Muertos) ----------
_sellos = {}
def sello(dark_bg, w):
    k = (dark_bg, w)
    if k not in _sellos:
        f = "/home/claude/zip/Entrega/png/ColgeioNacion--25.png" if dark_bg else "/home/claude/zip/Entrega/png/ColgeioNacion--24.png"
        im = Image.open(f).convert("RGBA"); im = im.crop(im.getbbox()).resize((w, w), Image.LANCZOS)
        _sellos[k] = im
    return _sellos[k]

def sparkle(d, cx, cy, r, fill):
    pts = []
    for k in range(8):
        a = math.pi / 4 * k; rr = r if k % 2 == 0 else r * .28
        pts.append((cx + rr * math.cos(a - math.pi / 2), cy + rr * math.sin(a - math.pi / 2)))
    d.polygon(pts, fill=fill)

def mix(a, b, t): return tuple(int(x * (1 - t) + y * t) for x, y in zip(a, b))


def heart(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r * .7, cx, cy + r * .3], fill=fill); d.ellipse([cx, cy - r * .7, cx + r, cy + r * .3], fill=fill)
    d.polygon([(cx - r * .97, cy - r * .05), (cx + r * .97, cy - r * .05), (cx, cy + r * 1.05)], fill=fill)

def smiley(d, cx, cy, r, fill, ink):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    d.ellipse([cx - r * .42, cy - r * .35, cx - r * .22, cy - r * .1], fill=ink); d.ellipse([cx + r * .22, cy - r * .35, cx + r * .42, cy - r * .1], fill=ink)
    d.arc([cx - r * .5, cy - r * .35, cx + r * .5, cy + r * .5], start=20, end=160, fill=ink, width=max(4, int(r * .1)))

def pencil(im, x, y, L, ang, col):
    lay = Image.new("RGBA", (L + 40, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([20, 14, L - 30, 46], fill=col); d.polygon([(L - 30, 14), (L + 10, 30), (L - 30, 46)], fill=(245, 222, 179)); d.polygon([(L - 2, 25), (L + 10, 30), (L - 2, 35)], fill=G)
    d.rectangle([10, 14, 24, 46], fill=P)
    lay = lay.rotate(ang, resample=Image.BICUBIC, expand=True); im.paste(lay, (x, y), lay)

def deco(im, bg, acc, variant=0, top_only=False):
    """Decoración neutral inspirada en colegiominacion.com: sello, destellos, arcos y marca de agua."""
    Wi, Hi = im.size; d = ImageDraw.Draw(im)
    dark = bg in (G, B, P)
    line = mix(bg, C if dark else G, .18)
    v = variant % 8
    if v == 0:   # arco grande arriba a la derecha + sello
        d.ellipse([Wi - 520, -380, Wi + 300, 440], outline=line, width=5)
        s = sello(dark, 170).rotate(-10, resample=Image.BICUBIC, expand=True); im.paste(s, (Wi - 250, 50), s)
        sparkle(d, 120, 120, 34, acc); sparkle(d, 190, 70, 16, acc)
    elif v == 1: # sol con rayos + destellos
        cx, cy = Wi - 170, 150; d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=Y if bg != Y else C)
        for k in range(9):
            a = math.pi * (1.05 + k * .11); d.line([(cx + 95 * math.cos(a), cy + 95 * math.sin(a)), (cx + 130 * math.cos(a), cy + 130 * math.sin(a))], fill=line if bg != Y else G, width=6)
        sparkle(d, 110, 120, 30, acc)
    elif v == 2: # "Aa" y garabato, como en el hero del sitio
        d.text((80, 60), "Aa", font=font(MIJA, 120), fill=line)
        s = sello(dark, 150).rotate(8, resample=Image.BICUBIC, expand=True); im.paste(s, (Wi - 230, 60), s)
        sparkle(d, 330, 110, 26, acc)
    elif v == 4: # corazones del sello
        heart(d, Wi - 170, 130, 52, P if bg != P else C); heart(d, Wi - 270, 90, 22, acc); sparkle(d, 120, 120, 30, acc)
    elif v == 5: # carita feliz + destellos
        smiley(d, Wi - 170, 150, 78, Y if bg != Y else C, G); sparkle(d, Wi - 300, 80, 22, acc); sparkle(d, 110, 120, 30, acc)
    elif v == 6: # lápiz como en el sitio + sello
        pencil(im, Wi - 470, 70, 330, -18, B if bg != B else Y); d = ImageDraw.Draw(im)
        s = sello(dark, 130).rotate(-6, resample=Image.BICUBIC, expand=True); im.paste(s, (70, 50), s)
    elif v == 7: # corazón + carita pequeños y arco
        d.ellipse([Wi - 460, -300, Wi + 220, 380], outline=line, width=5)
        smiley(d, Wi - 140, 120, 48, Y if bg != Y else C, G); heart(d, Wi - 250, 190, 30, P if bg != P else C); sparkle(d, 120, 110, 32, acc)
    else:        # dos arcos punteados + destellos
        for r in (260, 340):
            for k in range(0, 180, 6):
                a1 = math.radians(k); a2 = math.radians(k + 3)
                d.arc([Wi - 200 - r, -r, Wi - 200 + r, r], start=k, end=k + 3, fill=line, width=5)
        sparkle(d, 120, 110, 36, acc); sparkle(d, 200, 175, 14, acc)
    if not top_only:
        wm = eye(mix(bg, C if dark else G, .12), 760); im.paste(wm, (Wi - 520, Hi - 560), wm)

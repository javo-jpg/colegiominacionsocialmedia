"""Historias animadas 1080x1920 (MP4 con música). Zona segura de texto: y 250–1580, x 80–1000."""
import sys, os, json, glob, math, subprocess
sys.path.insert(0, "/home/claude/scripts")
from design import *
from multiprocessing import Pool

Wr, Hr, FPS = 1080, 1920, 24
REPO = "/home/claude/colegiominacionsocialmedia/"
A = REPO + "assets/2026-11/"
OUT = A + "stories-v2/"; os.makedirs(OUT, exist_ok=True)
M = "/home/claude/media/"
MUSIC = ["/home/claude/reel/src/happy4u.mp3", "/home/claude/reel/src/pearl.mp3", "/home/claude/reel/src/summer.mp3", "/home/claude/reel/src/steps.mp3"]

def clamp(x): return min(max(x, 0.0), 1.0)
def e_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def e_back(x): x = clamp(x); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def e_io(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def sg(t, t0, d): return (t - t0) / d

def put(im, sp, x, y, a=1.0, s=1.0, rot=0):
    """Pega un sprite RGBA con opacidad, escala y rotación (centro como ancla si s/rot)."""
    if a <= 0.01: return
    if s != 1.0 or rot:
        w, h = sp.size
        if s != 1.0: sp = sp.resize((max(1, int(w * s)), max(1, int(h * s))), Image.BILINEAR)
        if rot: sp = sp.rotate(rot, resample=Image.BILINEAR, expand=True)
        x = x + (w - sp.width) / 2; y = y + (h - sp.height) / 2
    m = sp.getchannel("A")
    if a < 0.99: m = m.point(lambda v: int(v * a))
    im.paste(sp.convert("RGB"), (int(x), int(y)), m)

def text_sprite(text, f, fill, maxw, lh=1.12):
    d = ImageDraw.Draw(Image.new("RGB", (4, 4))); lines = wrap(d, text, f, maxw); out = []
    for l in lines:
        sp = Image.new("RGBA", (int(d.textlength(l, font=f)) + 8, int(f.size * lh) + 10), (0, 0, 0, 0))
        ImageDraw.Draw(sp).text((2, 2), l, font=f, fill=fill); out.append(sp)
    return out

def pill_sprite(txt, bg, fg, size=32, arrow=False):
    f = font(SB, size); d = ImageDraw.Draw(Image.new("RGB", (4, 4))); tw = int(d.textlength(txt, font=f)); w = tw + 60 + (size * 1.3 if arrow else 0); w = int(w); h = int(size * 1.9)
    sp = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dd = ImageDraw.Draw(sp)
    dd.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=bg); dd.text((30, h / 2), txt, font=f, fill=fg, anchor="lm") if arrow else dd.text((w / 2, h / 2), txt, font=f, fill=fg, anchor="mm")
    if arrow:
        x0 = 30 + tw + size * .35; x1 = w - 30; cy = h / 2; lw = max(4, size // 7)
        dd.line([(x0, cy), (x1, cy)], fill=fg, width=lw); dd.line([(x1 - size * .3, cy - size * .3), (x1, cy), (x1 - size * .3, cy + size * .3)], fill=fg, width=lw, joint="curve")
    return sp

class Base:
    def __init__(s, bg, acc, wm_seed, sp_seed=0):
        s.bg, s.acc = bg, acc; s.dark = bg in (G, B, P); s.fg = C if s.dark else G
        kind = WM_KINDS[wm_seed % len(WM_KINDS)]
        s.wm = wm_mark(kind, 900, mix(bg, C if s.dark else G, .16 if s.dark else .11)); s.seed = sp_seed; s.k = wm_seed
    def frame(s, t):
        im = Image.new("RGB", (Wr, Hr), s.bg)
        w = s.wm.rotate(-12 + 7 * math.sin(t * .6 + s.k) + t * 2.5, resample=Image.BILINEAR, expand=True)
        pos = [(Wr - w.width * .72, Hr - w.height * .78), (-w.width * .25, Hr - w.height * .8), (Wr - w.width * .65, Hr * .38)][s.k % 3]
        im.paste(w.convert("RGB"), (int(pos[0]), int(pos[1] + 12 * math.sin(t * .9))), w.getchannel("A"))
        d = ImageDraw.Draw(im)
        for i, (x, y, r) in enumerate([(130, 200, 34), (215, 150, 16), (Wr - 120, 215, 26)]):
            sparkle(d, x, y, r * (.85 + .3 * math.sin(t * 3 + i * 1.7 + s.seed)), s.acc if i != 2 else (Y if s.bg != Y else C))
        return im

def foot(im, bg, t, t0=.5):
    lg = logo("verdeclaro" if bg in (G, B, P) else "verde", 230)
    put(im, lg, 80, 1480 + int(20 * (1 - e_out(sg(t, t0, .5)))), e_out(sg(t, t0, .5)))

# ---------- plantillas ----------
def render_text(sp, t):
    base = sp["_base"]; im = base.frame(t); bg, fg, acc = sp["bg"], base.fg, sp["acc"]
    S = sp["_sprites"]; y = S["y0"]; icn = S.get("icon")
    if icn:
        a = e_back(sg(t, .05, .6)); put(im, icn, 80, y + 4 * math.sin(t * 2.4), a, max(.01, a)); y += 200
    put(im, S["pill"], 80, y, e_out(sg(t, .2, .35)), .6 + .4 * e_back(sg(t, .2, .5))); y += 64
    for i, ln in enumerate(S["title"]):
        p = e_out(sg(t, .45 + i * .13, .55)); put(im, ln, 80, y + 70 * (1 - p), p); y += S["tlh"]
    y += 30
    for i, ln in enumerate(S["body"]):
        p = e_out(sg(t, .5 + .13 * len(S["title"]) + i * .08, .5)); put(im, ln, 80, y + 30 * (1 - p), p); y += S["blh"]
    y += 40
    for i, (ics, tx) in enumerate(S["rows"]):
        p = e_out(sg(t, 1.1 + i * .18, .5)); put(im, ics, 80 - 90 * (1 - p), y, p); put(im, tx, 164 - 90 * (1 - p), y + 4, p); y += 86
    foot(im, bg, t); return im

def prep_text(sp):
    bg, acc = sp["bg"], sp["acc"]; base = Base(bg, acc, sp["wm"], sp["wm"]); sp["_base"] = base
    d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    f = fit_font(d, sp["title"], MIJA, 900, 4, 120, 70); fb = font(SL, 44)
    S = {"title": text_sprite(sp["title"], f, base.fg, 900, 1.08), "tlh": int(f.size * 1.08),
         "body": text_sprite(sp["body"], fb, base.fg, 880, 1.35) if sp.get("body") else [], "blh": int(44 * 1.35)}
    S["pill"] = pill_sprite(sp["eyebrow"].upper() if False else sp["eyebrow"], acc, G if acc != G else C)
    if sp.get("ic"): S["icon"] = icon(sp["ic"], 170, acc, bg)
    S["rows"] = [(icon(ic, 60, Y, bg), text_sprite(tx, font(SB, 44), base.fg, 800)[0]) for ic, tx in sp.get("rows", [])]
    h = (200 if sp.get("ic") else 0) + 64 + len(S["title"]) * S["tlh"] + (30 + len(S["body"]) * S["blh"] if S["body"] else 0) + (40 + 86 * len(S["rows"]) if S["rows"] else 0)
    S["y0"] = max(380, (250 + 1440 - h) / 2); assert S["y0"] + h <= 1580, (sp["name"], S["y0"] + h)
    sp["_sprites"] = S

LOGOF = logo
def render_photo(sp, t):
    # foto a pantalla completa, texto limpio abajo (sin división)
    S = sp["_sprites"]; big = S["big"]; bw, bh = big.size; u = clamp(t / sp["dur"])
    z = 1.0 + .08 * u; cw, ch = bw / 1.10 / z, bh / 1.10 / z
    x0 = (bw - cw) * (.5 + .10 * (u - .5)); y0 = (bh - ch) * .5
    im = big.resize((Wr, Hr), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")
    im.alpha_composite(S["grad"])
    im = im.convert("RGB")
    put(im, S["logo"], 80, 290, e_out(sg(t, .2, .5)))
    y = 1180
    put(im, S["pill"], 80, y, e_out(sg(t, .6, .35)), .6 + .4 * e_back(sg(t, .6, .5))); y += 84
    for i, ln in enumerate(S["title"]):
        p = e_out(sg(t, .8 + i * .13, .5)); put(im, ln, 80, y + 50 * (1 - p), p); y += S["tlh"]
    return im

def prep_photo(sp):
    bg, acc = sp["bg"], sp["acc"]
    d = ImageDraw.Draw(Image.new("RGB", (4, 4))); f = fit_font(d, sp["title"], MIJA, 860, 2, 92, 60)
    ph = Image.open(sp["photo"]).convert("RGB"); big = cover(ph, int(Wr * 1.10), int(Hr * 1.10), sp.get("focus", (.5, .5)))
    g = Image.new("RGBA", (Wr, Hr), (0, 0, 0, 0)); px = g.load()
    for yy in range(0, 520):
        a = int(120 * (1 - yy / 520) ** 1.6)
        for xx in range(Wr): px[xx, yy] = (14, 24, 20, a)
    for yy in range(1000, Hr):
        a = int(170 * ((yy - 1000) / (Hr - 1000)) ** 1.4)
        for xx in range(Wr): px[xx, yy] = (14, 24, 20, a)
    lg = LOGOF("verdeclaro", 230)
    sp["_sprites"] = {"big": big, "grad": g, "logo": lg, "title": text_sprite(sp["title"], f, C, 860, 1.08), "tlh": int(f.size * 1.08), "pill": pill_sprite(sp["eyebrow"], acc, G)}
    sp["dur"] = sp.get("dur", 7)

def prep_teaser(sp):
    bg, acc = sp["bg"], sp["acc"]; base = Base(bg, acc, sp["wm"], sp["wm"]); sp["_base"] = base
    d = ImageDraw.Draw(Image.new("RGB", (4, 4))); f = fit_font(d, sp["title"], MIJA, 900, 2, 84, 60)
    imgs = [Image.open(p).convert("RGB") for p in sp["slides"]]
    r0 = imgs[0].width / imgs[0].height; ch = 820; cw = int(ch * r0)
    if cw > 700: cw = 700; ch = int(cw / r0)
    n = len(imgs); gap = 24; strip = Image.new("RGB", (n * (cw + gap), ch), C)
    for i, im_ in enumerate(imgs):
        strip.paste(im_.resize((cw, int(im_.height * cw / im_.width)), Image.LANCZOS).crop((0, 0, cw, ch)) if im_.width / im_.height > .5 else cover(im_, cw, ch), (i * (cw + gap), 0))
    fr = 14; mask = rmask(cw, ch, 28); sh = Image.new("RGBA", (cw + 2 * fr + 120, ch + 2 * fr + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([60, 80, cw + 2 * fr + 60, ch + 2 * fr + 80], radius=36, fill=(0, 0, 0, 90)); sh = sh.filter(ImageFilter.GaussianBlur(18))
    frame = Image.new("RGBA", (cw + 2 * fr, ch + 2 * fr), C + (255,)); frame.putalpha(rmask(cw + 2 * fr, ch + 2 * fr, 38))
    sp["_sprites"] = {"strip": strip, "cw": cw, "ch": ch, "n": n, "gap": gap, "fr": fr, "mask": mask, "shadow": sh, "frame": frame,
                      "title": text_sprite(sp["title"], f, base.fg, 900, 1.08), "tlh": int(f.size * 1.08),
                      "pill": pill_sprite("NUEVO EN EL PERFIL", acc, G if acc != G else C), "hint": pill_sprite("Desliza para ver todo" if n > 1 else "Míralo en el perfil", Y if bg != Y else G, G if bg != Y else Y, 34, arrow=n > 1)}
    show = min(n, 4); sp["_show"] = show; sp["dur"] = 2.0 + max(show - 1, 0) * 1.25 + 1.4 if show > 1 else 5.5

def render_teaser(sp, t):
    base = sp["_base"]; bg = sp["bg"]; im = base.frame(t); S = sp["_sprites"]; fg = base.fg
    put(im, S["pill"], 80, 290, e_out(sg(t, .1, .35)), .6 + .4 * e_back(sg(t, .1, .5)))
    y = 370
    for i, ln in enumerate(S["title"]):
        p = e_out(sg(t, .3 + i * .13, .5)); put(im, ln, 80, y + 60 * (1 - p), p); y += S["tlh"]
    top = int(y + 40); cw, ch, fr, gap = S["cw"], S["ch"], S["fr"], S["gap"]
    # carrusel: pasa de lámina en lámina
    k = 0.0
    if sp["_show"] > 1:
        tt = t - 1.9
        for i in range(sp["_show"] - 1):
            k += e_io(sg(tt, i * 1.25, .5))
    off = int(k * (cw + gap))
    win = S["strip"].crop((off, 0, off + cw, ch)); card = S["frame"].copy(); card.paste(win, (fr, fr), S["mask"])
    full = Image.new("RGBA", S["shadow"].size, (0, 0, 0, 0)); full.alpha_composite(S["shadow"]); full.alpha_composite(card, (60 - 0, 50))
    enter = e_back(sg(t, .55, .8)); ang = -3 + 1.4 * math.sin(t * 1.8)
    bob = 10 * math.sin(t * 2.2)
    cx = (Wr - full.width) // 2; cy = top - 50 + int(900 * (1 - enter)) + bob
    put(im, full, cx, cy, e_out(sg(t, .55, .3)), 1.0, ang)
    # puntos
    d = ImageDraw.Draw(im); n = sp["_show"]
    if n > 1:
        cur = int(round(k)); yy = min(top + ch + 70, 1500)
        for i in range(n): d.ellipse([Wr / 2 - n * 22 + i * 44 - (9 if i == cur else 6), yy - (9 if i == cur else 6), Wr / 2 - n * 22 + i * 44 + (9 if i == cur else 6), yy + (9 if i == cur else 6)], fill=(Y if bg != Y else G) if i == cur else mix(bg, fg, .35))
    hy = min(top + ch + 110, 1520)
    pulse = 1 + .04 * math.sin(t * 4)
    put(im, S["hint"], (Wr - S["hint"].width) // 2 + 6 * math.sin(t * 4), hy, e_out(sg(t, 1.6, .4)), pulse)
    return im

RENDER = {"text": (prep_text, render_text), "photo": (prep_photo, render_photo), "teaser": (prep_teaser, render_teaser)}

def build(sp):
    prep, rend = RENDER[sp["kind"]]; prep(sp); dur = sp.get("dur", 7); n = int(dur * FPS)
    out = OUT + sp["name"] + ".mp4"; tr = MUSIC[sp["music"] % len(MUSIC)]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wr}x{Hr}", "-r", str(FPS), "-i", "-",
           "-ss", str(sp["music"] * 9 % 40 + 3), "-i", tr, "-filter_complex", f"[1:a]atrim=0:{dur},afade=t=in:d=0.4,afade=t=out:st={dur - 1.2}:d=1.2,volume=.55[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-t", str(dur), "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(rend(sp, i / FPS).tobytes())
    p.stdin.close(); p.wait()
    poster = rend(sp, min(dur - .3, 3.5 if sp["kind"] != "teaser" else dur - 1.0)); poster.save(OUT + sp["name"] + ".jpg", quality=88)
    return sp["name"], dur

def specs():
    CT = [("chat", "WhatsApp 56 5292 2720"), ("phone", "55 5911 1865"), ("globe", "colegiominacion.com")]
    L = []; mk = 0
    def add(**k):
        nonlocal mk; k["music"] = mk; k.setdefault("wm", mk); mk += 1; L.append(k)
    T = lambda n, f, h, u, **k: add(kind="text", name=n, fecha=f, hora=h, uso=u, **k)
    P_ = lambda n, f, h, u, **k: add(kind="photo", name=n, fecha=f, hora=h, uso=u, **k)
    T("hl-informes-1", "2026-11-03", "09:00", "Destacada: Informes", bg=G, acc=Y, eyebrow="Informes", title="¿Quieres conocer Mi Nación?", body="Escríbenos o llámanos y te damos toda la información.", ic="chat", rows=CT)
    T("hl-informes-2", "2026-11-03", "19:00", "Destacada: Informes", bg=Y, acc=G, eyebrow="Informes", title="Una semana de experiencia sin costo", body="Tu hijo conoce el colegio desde adentro. Fechas y disponibilidad se confirman con nosotros.", ic="calendar")
    T("hl-informes-3", "2026-11-04", "09:00", "Destacada: Informes", bg=LG, acc=G, eyebrow="Ubicación", title="Preescolar: Fresno 172, Santa Úrsula Coapa", body="Primaria: San Felipe MZ532 LT4 (271), Pedregal de Santa Úrsula. Coyoacán.", ic="pin")
    P_("hl-preescolar-1", "2026-11-04", "19:00", "Destacada: Preescolar", bg=G, acc=Y, eyebrow="Preescolar Fresno", title="Un espacio para jugar y explorar", photo=M + "juegos2.jpg")
    P_("hl-preescolar-2", "2026-11-05", "09:00", "Destacada: Preescolar", bg=B, acc=Y, eyebrow="Preescolar Fresno", title="Tradiciones que vivimos en comunidad", photo=M + "ofr/1_altar_kinder.jpg")
    P_("hl-primaria-1", "2026-11-06", "09:00", "Destacada: Primaria", bg=P, acc=Y, eyebrow="Primaria San Felipe", title="Aprender, crear y recordar juntos", photo=M + "ofr/2_altar_primaria.jpg")
    T("hl-idiomas-1", "2026-11-06", "19:00", "Destacada: Idiomas", bg=C, acc=B, eyebrow="Idiomas", title="¡Hola! Hello! Bonjour !", body="Español, inglés y francés desde preescolar.", ic="globe")
    T("hl-idiomas-2", "2026-11-07", "09:00", "Destacada: Idiomas", bg=B, acc=Y, eyebrow="Cambridge English", title="El colegio cubre el costo de la certificación", body="Pregunta a admisiones en qué grado se presenta.", ic="star")
    T("hl-aliados-1", "2026-11-08", "11:00", "Destacada: Aliados", bg=LG, acc=G, eyebrow="Aliados", title="Innovamat, LUCA, Hachette, Tekman, Nat Geo y Música", body="Programas y recursos que apoyan a los maestros en el salón.", ic="bulb")
    T("hl-papas-1", "2026-11-08", "19:00", "Destacada: Papás", bg=G, acc=Y, eyebrow="Papás Presentes", title="Un espacio gratuito para todas las familias", body="Lectura del mes, preguntas para Rocío e ideas para casa.", ic="book")
    P_("hl-vida-1", "2026-11-03", "13:00", "Destacada: Vida MN", bg=G, acc=Y, eyebrow="Día de Muertos", title="Así vivimos nuestras ofrendas", photo=M + "ofr/3_cempasuchil.jpg")
    posts = json.load(open(REPO + "plan/2026-11/posts.json"))
    TEASER = {"03-nueva-web": "¡Tenemos página nueva!", "04-papas-presentes": "Presentamos Papás Presentes", "05-tres-idiomas": "Hola · Hello · Bonjour", "06-pedir-informes": "Así puedes pedir informes", "07-buen-fin": "Este Buen Fin, invierte en su futuro", "08-preescolar-reel": "Conoce nuestro preescolar", "09-preguntas-casa": "3 preguntas para platicar en casa", "11-aliados": "¿Con qué aprenden nuestros alumnos?", "12-20-noviembre": "20 de noviembre en Mi Nación", "13-pregunta-rocio": "Pregúntale a Rocío", "14-valores": "Valores que se viven", "16-planteles": "Nuestros dos planteles", "17-agenda-visita": "Agenda tu visita", "18-cierre-lectura": "Cerramos Hijos felices", "19-informes-reel": "Pide informes en 30 segundos"}
    cols = [(G, Y), (B, Y), (P, Y), (LG, G), (Y, G), (C, B)]; k = 0
    for p in posts:
        if p["slug"] in ("01-ofrendas", "02-reel-recap", "10-maestras-reel", "15-papas-reel"): continue
        fs = sorted(glob.glob(A + p["slug"] + "/*.jpg")); cv = [f for f in fs if f.endswith("portada.jpg")]; sl = cv + [f for f in fs if f not in cv]
        h, m_ = map(int, p["hora"].split(":")); m_ += 45; h += m_ // 60; m_ %= 60; bg, acc = cols[k % 6]; k += 1
        add(kind="teaser", name="post-" + p["slug"], fecha=p["fecha"], hora=f"{h:02d}:{m_:02d}", uso="Aviso de post nuevo", bg=bg, acc=acc, title=TEASER[p["slug"]], slides=sl if len(sl) > 1 else sl)
    for i, f in enumerate(["2026-11-06", "2026-11-13", "2026-11-20", "2026-11-27"]):
        t = ["Escríbenos hoy y agenda tu visita", "¿Tienes dudas? Te respondemos por WhatsApp", "Conoce nuestros dos planteles en Coyoacán", "Agenda tu visita antes de vacaciones"][i]
        T(f"viernes-informes-{i+1}", f, "12:00" if i < 3 else "16:00", "Viernes: Pide informes", bg=[G, B, P, G][i], acc=Y, eyebrow="Pide informes", title=t, ic="chat", rows=CT)
    return L

if __name__ == "__main__":
    L = specs(); only = sys.argv[1:]
    if only: L = [s for s in L if s["name"] in only]
    with Pool(min(4, os.cpu_count() or 2)) as pool:
        res = pool.map(build, L)
    meta = [dict(file="stories-v2/" + s["name"] + ".mp4", poster="stories-v2/" + s["name"] + ".jpg", name=s["name"], fecha=s["fecha"], hora=s["hora"], uso=s["uso"], dur=s.get("dur", 7)) for s in specs() if (not only or s["name"] in only)]
    if not only: json.dump(meta, open(REPO + "plan/2026-11/stories_v2.json", "w"), ensure_ascii=False, indent=1)
    print(res)

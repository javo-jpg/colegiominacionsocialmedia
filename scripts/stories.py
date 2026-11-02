"""Historias de noviembre 1080x1920. Zona segura de historias: texto entre y=250 y y=1580, x 80–1000."""
import sys, os, json, glob
sys.path.insert(0, "/home/claude/scripts")
from design import *
Wr, Hr = 1080, 1920
A = "/home/claude/colegiominacionsocialmedia/assets/2026-11/"
OUT = A + "stories/"; os.makedirs(OUT, exist_ok=True)
TOP, BOT = 250, 1580
def chk(y, what): assert TOP <= y <= BOT, (what, y)

def base(bg, acc, v):
    im = Image.new("RGB", (Wr, Hr), bg); deco(im, bg, acc, v, top_only=True)
    wm = eye(mix(bg, C if bg in (G, B, P) else G, .1), 760); im.paste(wm, (Wr - 520, Hr - 640), wm)
    return im

def foot(im, bg, y=1470):
    lg = logo("verdeclaro" if bg in (G, B, P) else "verde", 230); im.paste(lg, (80, y), lg); chk(y + lg.height, "logo")

def s_text(bg, fg, acc, eyebrow_t, title, body=None, ic=None, v=0, extra=None):
    im = base(bg, acc, v); d = ImageDraw.Draw(im)
    f = fit_font(d, title, MIJA, 900, 4, 120, 70); tl = wrap(d, title, f, 900)
    fb = font(SL, 44); bl = wrap(d, body, fb, 880) if body else []
    h = (200 if ic else 0) + 64 + len(tl) * f.size * 1.08 + (30 + len(bl) * 44 * 1.35 if body else 0) + (extra[1] if extra else 0)
    y = max(380, (TOP + 1440 - h) / 2)
    if ic: icn = icon(ic, 170, acc, bg); im.paste(icn, (80, int(y)), icn); y += 200
    pill(d, (80, y), eyebrow_t, font(SB, 32), acc, G if acc != G else C); y += 64
    y = text_block(d, (80, y), title, f, fg, 900, 1.08)
    if body: y = text_block(d, (80, y + 30), body, fb, fg, 880, 1.35)
    if extra: y = extra[0](im, d, y + 40)
    chk(y, title); foot(im, bg); return im

def s_photo(photo, eyebrow_t, title, body=None, bg=G, acc=Y, focus=(.5, .5)):
    im = Image.new("RGB", (Wr, Hr), bg); im.paste(cover(photo, Wr, 1060, focus), (0, 0)); d = ImageDraw.Draw(im)
    sparkle(d, Wr - 140, 1120, 30, acc); heart(d, Wr - 230, 1180, 22, P if bg != P else C)
    y = 1110; pill(d, (80, y), eyebrow_t, font(SB, 30), acc, G); y += 70
    f = fit_font(d, title, MIJA, 880, 2, 90, 60); y = text_block(d, (80, y), title, f, C if bg in (G, B, P) else G, 880, 1.08)
    if body: y = text_block(d, (80, y + 14), body, font(SL, 38), LG if bg == G else INK, 880, 1.3)
    chk(y, title); return im

def s_teaser(cover_path, title, bg, acc, v):
    im = base(bg, acc, v); d = ImageDraw.Draw(im)
    pill(d, (80, 300), "NUEVO EN EL PERFIL", font(SB, 32), acc, G if acc != G else C)
    f = fit_font(d, title, MIJA, 900, 2, 84, 60); y = text_block(d, (80, 380), title, f, C if bg in (G, B, P) else G, 900, 1.08)
    cv = Image.open(cover_path).convert("RGB"); r = 1020 / cv.height if cv.height > cv.width * 1.5 else 760 / cv.width
    cv = cv.resize((int(cv.width * r), int(cv.height * r)), Image.LANCZOS)
    if cv.height > 1500 - y - 60:
        r2 = (1500 - y - 60) / cv.height; cv = cv.resize((int(cv.width * r2), int(cv.height * r2)), Image.LANCZOS)
    fr = Image.new("RGBA", (cv.width + 24, cv.height + 24), C + (255,)); fr.paste(cv, (12, 12))
    sh = Image.new("RGBA", (fr.width + 60, fr.height + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([30, 44, fr.width + 30, fr.height + 44], radius=30, fill=(0, 0, 0, 100))
    sh = sh.filter(ImageFilter.GaussianBlur(16)); m = rmask(fr.width, fr.height, 28); fr.putalpha(m); sh.alpha_composite(fr, (30, 30))
    sh = sh.rotate(-3, resample=Image.BICUBIC, expand=True)
    im.paste(sh, ((Wr - sh.width) // 2, int(y) + 30), sh); d = ImageDraw.Draw(im)
    chk(int(y) + 30 + sh.height - 60, "teaser img")
    return im

def cta_extra(im, d, y):
    for ic, t in [("chat", "WhatsApp 56 5292 2720"), ("phone", "55 5911 1865"), ("globe", "colegiominacion.com")]:
        icn = icon(ic, 60, Y, G); im.paste(icn, (80, int(y)), icn); d.text((164, y + 30), t, font=font(SB, 44), fill=C, anchor="lm"); y += 86
    return y
CTA_EXTRA = (cta_extra, 260)

stories = []
def add(name, img, fecha, hora, uso):
    img.save(OUT + name + ".jpg", quality=92); stories.append(dict(file="stories/" + name + ".jpg", fecha=fecha, hora=hora, uso=uso))
M = "/home/claude/media/"
# --- Destacadas (evergreen), 3 al 9 de noviembre ---
add("hl-informes-1", s_text(G, C, Y, "Informes", "¿Quieres conocer Mi Nación?", "Escríbenos o llámanos y te damos toda la información.", "chat", 0, CTA_EXTRA), "2026-11-03", "09:00", "Destacada: Informes")
add("hl-informes-2", s_text(Y, G, G, "Informes", "Una semana de experiencia sin costo", "Tu hijo conoce el colegio desde adentro. Fechas y disponibilidad se confirman con nosotros.", "calendar", 5), "2026-11-03", "19:00", "Destacada: Informes")
add("hl-informes-3", s_text(LG, G, G, "Ubicación", "Preescolar: Fresno 172, Santa Úrsula Coapa", "Primaria: San Felipe MZ532 LT4 (271), Pedregal de Santa Úrsula. Coyoacán.", "pin", 4), "2026-11-04", "09:00", "Destacada: Informes")
add("hl-preescolar-1", s_photo(Image.open(M + "juegos2.jpg"), "Preescolar Fresno", "Un espacio para jugar y explorar", None, G, Y), "2026-11-04", "19:00", "Destacada: Preescolar")
add("hl-preescolar-2", s_photo(Image.open(M + "ofr/1_altar_kinder.jpg"), "Preescolar Fresno", "Tradiciones que vivimos en comunidad", None, B, Y), "2026-11-05", "09:00", "Destacada: Preescolar")
add("hl-primaria-1", s_photo(Image.open(M + "ofr/2_altar_primaria.jpg"), "Primaria San Felipe", "Aprender, crear y recordar juntos", None, P, Y), "2026-11-06", "09:00", "Destacada: Primaria")
add("hl-idiomas-1", s_text(C, G, B, "Idiomas", "¡Hola! Hello! Bonjour !", "Español, inglés y francés desde preescolar.", "globe", 1), "2026-11-06", "19:00", "Destacada: Idiomas")
add("hl-idiomas-2", s_text(B, C, Y, "Cambridge English", "El colegio cubre el costo de la certificación", "Pregunta a admisiones en qué grado se presenta.", "star", 7), "2026-11-07", "09:00", "Destacada: Idiomas")
add("hl-aliados-1", s_text(LG, G, G, "Aliados", "Innovamat, LUCA, Hachette, Tekman, Nat Geo y Música", "Programas y recursos que apoyan a los maestros en el salón.", "bulb", 6), "2026-11-08", "11:00", "Destacada: Aliados")
add("hl-papas-1", s_text(G, C, Y, "Papás Presentes", "Un espacio gratuito para todas las familias", "Lectura del mes, preguntas para Rocío e ideas para casa.", "book", 2), "2026-11-08", "19:00", "Destacada: Papás")
add("hl-vida-1", s_photo(Image.open(M + "ofr/3_cempasuchil.jpg"), "Día de Muertos", "Así vivimos nuestras ofrendas", None, G, Y), "2026-11-03", "13:00", "Destacada: Vida MN")
# --- Aviso de cada post nuevo (45 min después) ---
posts = json.load(open("/home/claude/colegiominacionsocialmedia/plan/2026-11/posts.json"))
TEASER = {"03-nueva-web": "¡Tenemos página nueva!", "04-papas-presentes": "Presentamos Papás Presentes", "05-tres-idiomas": "Hola · Hello · Bonjour", "06-pedir-informes": "Así puedes pedir informes", "07-buen-fin": "Este Buen Fin, invierte en su futuro", "08-preescolar-reel": "Conoce nuestro preescolar", "09-preguntas-casa": "3 preguntas para platicar en casa", "11-aliados": "¿Con qué aprenden nuestros alumnos?", "12-20-noviembre": "20 de noviembre en Mi Nación", "13-pregunta-rocio": "Pregúntale a Rocío", "14-valores": "Valores que se viven", "16-planteles": "Nuestros dos planteles", "17-agenda-visita": "Agenda tu visita", "18-cierre-lectura": "Cerramos Hijos felices", "19-informes-reel": "Pide informes en 30 segundos"}
cols = [(G, Y), (B, Y), (P, Y), (LG, G), (Y, G), (C, B)]
k = 0
for p in posts:
    if p["slug"] in ("01-ofrendas", "02-reel-recap", "10-maestras-reel", "15-papas-reel"): continue
    fs = sorted(glob.glob(A + p["slug"] + "/*.jpg")); cv = [f for f in fs if f.endswith("portada.jpg")] or fs
    h, m_ = map(int, p["hora"].split(":")); m_ += 45; h += m_ // 60; m_ %= 60
    title = TEASER[p["slug"]]
    bg, acc = cols[k % len(cols)]
    add("post-" + p["slug"], s_teaser(cv[0], title[:70], bg, acc, k + 3), p["fecha"], f"{h:02d}:{m_:02d}", "Aviso de post nuevo"); k += 1
# --- Viernes: Pide informes ---
for i, f in enumerate(["2026-11-06", "2026-11-13", "2026-11-20", "2026-11-27"]):
    t = ["Escríbenos hoy y agenda tu visita", "¿Tienes dudas? Te respondemos por WhatsApp", "Conoce nuestros dos planteles en Coyoacán", "Agenda tu visita antes de vacaciones"][i]
    add(f"viernes-informes-{i+1}", s_text([G, B, P, G][i], C, Y, "Pide informes", t, None, "chat", i + 2, CTA_EXTRA), f, "12:00", "Viernes: Pide informes")
json.dump(stories, open("/home/claude/colegiominacionsocialmedia/plan/2026-11/stories.json", "w"), ensure_ascii=False, indent=1)
print(len(stories))

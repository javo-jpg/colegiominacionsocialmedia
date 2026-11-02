import sys, os, subprocess
sys.path.insert(0, "/home/claude/scripts")
from posts import *
A = "/home/claude/colegiominacionsocialmedia/assets/2026-11/"
T = "/home/claude/reel/tmp/"; os.makedirs(T, exist_ok=True)
Wr, Hr = 1080, 1920
def run(c): subprocess.run(c, shell=True, check=True)

def caption_png(lines, path, tagtxt=None, y=1330):
    im = Image.new("RGBA", (Wr, Hr), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = font(SB, 54)
    ws = [d.textlength(l, font=f) for l in lines]; w = max(ws) + 88; h = len(lines) * 62 + 52
    if tagtxt:
        ft = font(SB, 34); tw = d.textlength(tagtxt, font=ft) + 48
        d.rounded_rectangle([(Wr - tw) / 2, y - 84, (Wr + tw) / 2, y - 22], radius=31, fill=Y); d.text((Wr / 2, y - 53), tagtxt, font=ft, fill=G, anchor="mm")
    d.rounded_rectangle([(Wr - w) / 2, y, (Wr + w) / 2, y + h], radius=30, fill=C)
    for k, l in enumerate(lines): d.text((Wr / 2, y + 26 + k * 62), l, font=f, fill=G, anchor="ma")
    im.save(path)

def still_clip(img, dur, out, cap=None, zoom=(1.0, 1.08), focus=(.5, .5)):
    base = cover(img, Wr, Hr, focus); big = base.resize((Wr * 2, Hr * 2), Image.LANCZOS); big.save(T + "s.png")
    frames = int(dur * 30); z0, z1 = zoom
    vf = f"zoompan=z='{z0}+({z1}-{z0})*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={Wr}x{Hr}:fps=30"
    if cap:
        run(f"ffmpeg -v error -y -loop 1 -i {T}s.png -loop 1 -i {cap} -filter_complex \"[0]{vf}[v];[1]format=rgba,fade=in:st=0.2:d=0.3:alpha=1[c];[v][c]overlay,format=yuv420p\" -t {dur} -c:v libx264 -preset veryfast -crf 18 -r 30 {out}")
    else:
        run(f"ffmpeg -v error -y -loop 1 -i {T}s.png -vf \"{vf},format=yuv420p\" -t {dur} -c:v libx264 -preset veryfast -crf 18 -r 30 {out}")

def card_clip(img, dur, out):
    img.convert("RGB").save(T + "card.png")
    run(f"ffmpeg -v error -y -loop 1 -i {T}card.png -vf \"fade=in:st=0:d=0.3,format=yuv420p\" -t {dur} -c:v libx264 -preset veryfast -crf 18 -r 30 {out}")

def concat(parts, out):
    open(T + "l.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {T}l.txt -c copy -movflags +faststart {out}")

def end_card():
    im = Image.open("/home/claude/reel/ov/end.png"); return im

# ---- 02 recap cover ----
os.makedirs(A + "02-reel-recap", exist_ok=True)
L_reel_cover(Image.open("/home/claude/media/vid_37.5.jpg"), "Así se vivió el Día de Muertos en Mi Nación", "Recap", (.5, .5)).save(A + "02-reel-recap/portada.jpg", quality=92)

# ---- 08 preescolar reel ----
if "08" in sys.argv or len(sys.argv) == 1:
    parts = []
    caption_png(["Así es nuestro preescolar"], T + "c1.png", "FRESNO 172")
    caption_png(["Espacios para jugar", "y explorar"], T + "c2.png")
    caption_png(["Tradiciones que vivimos", "en comunidad"], T + "c3.png")
    caption_png(["Familias que nos acompañan"], T + "c4.png")
    caption_png(["Español · Inglés · Francés"], T + "c5.png", "TRES IDIOMAS")
    still_clip(PH("juegos2.jpg"), 3.0, T + "p1.mp4", T + "c1.png")
    still_clip(PH("juegos1.jpg"), 2.6, T + "p2.mp4", T + "c2.png", (1.08, 1.0))
    still_clip(PH("altar_kinder.jpg"), 2.6, T + "p3.mp4", T + "c3.png", focus=(.45, .5))
    still_clip(PH("patio_familias.jpg"), 2.6, T + "p4.mp4", T + "c4.png", focus=(.55, .5))
    still_clip(PH("ilustra_ninos.jpg"), 2.6, T + "p5.mp4", T + "c5.png", (1.0, 1.05))
    card_clip(end_card(), 3.5, T + "p6.mp4")
    concat([T + f"p{k}.mp4" for k in range(1, 7)], A + "08-preescolar-reel/reel.mp4")

# ---- 19 pide informes reel ----
if "19" in sys.argv or len(sys.argv) == 1:
    os.makedirs(A + "19-informes-reel", exist_ok=True)
    def phone_card(shot, crop, title, eyebrow_t, bg=G, fg=C, acc=Y, step=None):
        im = Image.new("RGB", (Wr, Hr), bg); d = ImageDraw.Draw(im)
        if step: pill(d, (80, 250), step, font(SB, 34), acc, C if acc == G else G)
        f = fit_font(d, title, MIJA, Wr - 160, 2, 92, 60); y = text_block(d, (80, 340), title, f, fg, Wr - 160, 1.08)
        d.text((80, y + 14), eyebrow_t, font=font(SL, 40), fill=LG if bg == G else INK)
        s = PH(shot).crop(crop); ph = phone_frame(s, 1180); im.paste(ph, ((Wr - ph.width) // 2, Hr - ph.height + 80), ph)
        return im
    cov = L_reel_card(G, "Pide informes en 30 segundos desde tu celular", "Tutorial", "phone", "colegiominacion.com")
    cov.save(A + "19-informes-reel/portada.jpg", quality=92)
    c1 = phone_card("web_hero.jpg", (0, 0, 800, 1640), "Entra a colegiominacion.com", "Desde tu celular, sin descargar nada.", step="PASO 1")
    c2 = phone_card("web_hero.jpg", (0, 0, 800, 1640), "Toca «Pedir informes»", "Está siempre abajo, junto a WhatsApp y Llamar.", Y, G, G, "PASO 2")
    d2 = ImageDraw.Draw(c2); # highlight bottom bar area
    c3 = L_reel_card(B, "Elige: WhatsApp, llamada o formulario", "Paso 3", "chat", "El mensaje ya va escrito; solo lo envías tú.")
    c4 = L_reel_card(P, "Te contactamos pronto", "Listo", "heart", "Horario de atención: 9:00 a. m. a 3:30 p. m.")
    parts = []
    for k, (im, dur) in enumerate([(cov, 2.2), (c1, 3.0), (c2, 3.0), (c3, 3.0), (c4, 2.6), (end_card(), 3.5)]):
        card_clip(im, dur, T + f"q{k}.mp4"); parts.append(T + f"q{k}.mp4")
    concat(parts, A + "19-informes-reel/reel.mp4")
print("ok")

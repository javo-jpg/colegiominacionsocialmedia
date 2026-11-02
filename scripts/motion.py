"""Recap v3 en motion graphics: video a pantalla completa, tipografía animada.
- El texto nunca va sobre los niños: va en tarjetas animadas entre tomas o sobre tomas sin niños.
- Zona segura Reels: texto en x 80–960, y 270–1500."""
import sys, os, subprocess, shutil, math
sys.path.insert(0, "/home/claude/scripts")
from design import *
from reels_end import SAFE
S = "/home/claude/reel/src/agencia.mp4"; T = "/home/claude/reel/mg/"; os.makedirs(T, exist_ok=True)
Wr, Hr, FPS = 1080, 1920, 30
def run(c): subprocess.run(c, shell=True, check=True)
def ease(x): x = max(0., min(1., x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0., min(1., x)); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

class Txt:
    def __init__(s, text, fnt, color, x, y, t0, kind="up", bg=None, pad=(26, 14), anchor="la"):
        s.text, s.f, s.color, s.x, s.y, s.t0, s.kind, s.bg, s.pad = text, fnt, color, x, y, t0, kind, bg, pad
        d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        l, t, r, b = d.textbbox((0, 0), text, font=fnt)
        w, h = r - l + (pad[0] * 2 if bg else 0), fnt.size * 1.15 + (pad[1] * 2 if bg else 0)
        s.img = Image.new("RGBA", (int(w) + 4, int(h) + 4), (0, 0, 0, 0)); dd = ImageDraw.Draw(s.img)
        if bg: dd.rounded_rectangle([0, 0, w, h], radius=int(h / 2), fill=bg)
        dd.text((pad[0] if bg else 0, (pad[1] if bg else 0) - t + fnt.size * .05), text, font=fnt, fill=color)
        assert x >= SAFE[0] - 1 and x + s.img.width <= SAFE[2] + 40 and y >= SAFE[1] and y + s.img.height <= SAFE[3], (text, x, y, s.img.size)
    def draw(s, frame, t):
        p = (t - s.t0) / 0.42
        if p <= 0: return
        e = ease(p); a = int(255 * min(1, p * 2.2))
        im = s.img
        if s.kind == "pop":
            k = .6 + .4 * back(p); im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
            x = s.x + (s.img.width - im.width) / 2; y = s.y + (s.img.height - im.height) / 2
        else:
            x, y = s.x, s.y + 70 * (1 - e)
        if a < 255:
            al = im.split()[3].point(lambda v: v * a // 255); im = im.copy(); im.putalpha(al)
        frame.alpha_composite(im, (int(x), int(y)))

def picado_anim(frame, t, t0=0.0, n=8, cols=(Y, P, B, LG), bg=G, h=150):
    fw = Wr / n
    for i in range(n):
        p = ease((t - t0 - i * 0.04) / 0.45)
        if p <= 0: continue
        layer = Image.new("RGBA", (Wr, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        x = i * fw + 8; c = cols[i % len(cols)]; top = 6; bot = h
        d.polygon([(x, top), (x + fw - 16, top), (x + fw - 16, bot), (x + (fw - 16) / 2, bot - 22), (x, bot)], fill=c)
        cx = x + (fw - 16) / 2; cy = (top + bot) / 2 - 6; d.regular_polygon((cx, cy, 14), 4, rotation=45, fill=bg)
        frame.alpha_composite(layer, (0, int(-(h + 20) * (1 - p))))

def render(name, dur, bg, elements, extra=None):
    """bg: color -> tarjeta opaca; None -> overlay transparente (PNG)"""
    d = T + name + "/"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for k in range(int(dur * FPS)):
        t = k / FPS
        fr = Image.new("RGBA", (Wr, Hr), (bg + (255,)) if bg else (0, 0, 0, 0))
        if extra: extra(fr, t)
        for e in elements: e.draw(fr, t)
        fr.save(d + f"{k:04d}.png")
    out = T + name + (".mp4" if bg else ".mov")
    if bg: run(f"ffmpeg -v error -y -framerate {FPS} -i {d}%04d.png -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p {out}")
    else: run(f"ffmpeg -v error -y -framerate {FPS} -i {d}%04d.png -c:v qtrle {out}")
    return out

SELLO = "/home/claude/reel/mg_sello.png"   # logo fijo, dentro de zona segura, no se mueve con el zoom
SX, SY = 830, 290
def clip(start, dur, out, crop=None, zoom=0.04, overlay=None):
    vf = "delogo=x=895:y=25:w=160:h=155," + (f"crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}," if crop else "") + \
         f"scale=w='trunc({Wr}*(1+{zoom}*t/{dur})/2)*2':h='trunc({Hr}*(1+{zoom}*t/{dur})/2)*2':eval=frame:flags=lanczos,crop={Wr}:{Hr},setsar=1"
    logo_in = "" if crop else f" -i {SELLO}"
    chain = f"[0]{vf}[v]"
    last = "[v]"
    if not crop:
        chain += f";{last}[{1}]overlay={SX}:{SY}[l]"; last = "[l]"
    if overlay:
        idx = 2 if not crop else 1
        chain += f";{last}[{idx}]overlay=eof_action=pass[o]"; last = "[o]"
    chain += f";{last}format=yuv420p[out]"
    ov_in = f" -i {overlay}" if overlay else ""
    run(f"ffmpeg -v error -y -ss {start} -t {dur} -i {S}{logo_in}{ov_in} -filter_complex \"{chain}\" -map \"[out]\" -t {dur} -r {FPS} -an -c:v libx264 -preset veryfast -crf 18 {out}")
    return out

MJ = lambda s: font(MIJA, s)
parts = []
# 1. intro card
parts.append(render("c1", 1.7, G, [
    Txt("DÍA DE MUERTOS 2026", font(SB, 38), Y, 80, 640, .25),
    Txt("Así se vivió", MJ(124), C, 80, 720, .38),
    Txt("en Mi Nación", MJ(124), Y, 80, 870, .52)], lambda fr, t: picado_anim(fr, t)))
# 2. baile (sin texto)
parts.append(clip(36.0, 2.2, T + "v1.mp4"))
# 3. ofrendas: fotos originales del Drive en vertical (alta resolución), con movimiento
OFR = [("1_altar_kinder", 1.0, (1.0, 1.10)), ("2_altar_primaria", 1.0, (1.10, 1.0)), ("3_cempasuchil", .8, (1.0, 1.12)), ("4_mesa", .8, (1.12, 1.0)), ("5_mesa2", .8, (1.0, 1.10))]
ov = render("o3", sum(d for _, d, _ in OFR), None, [
    Txt("Ofrendas hechas", MJ(84), G, 80, 1210, .15, bg=C, pad=(34, 16)),
    Txt("por nuestros alumnos", MJ(84), G, 80, 1340, .3, bg=C, pad=(34, 16))])
for k, (nm, du, (z0, z1)) in enumerate(OFR):
    im = Image.open(f"/home/claude/media/ofr/{nm}.jpg").convert("RGB").resize((Wr * 2, Hr * 2), Image.LANCZOS)
    im.save(T + "st.png"); fr = int(du * FPS)
    run(f"ffmpeg -v error -y -loop 1 -i {T}st.png -vf \"zoompan=z='{z0}+({z1}-{z0})*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s={Wr}x{Hr}:fps={FPS},format=yuv420p\" -t {du} -c:v libx264 -preset veryfast -crf 18 {T}d{k}.mp4")
open(T + "d.txt", "w").write("".join(f"file '{T}d{k}.mp4'\n" for k in range(len(OFR))))
run(f"ffmpeg -v error -y -f concat -safe 0 -i {T}d.txt -c copy {T}dcat.mp4")
run(f"ffmpeg -v error -y -i {T}dcat.mp4 -i {SELLO} -i {ov} -filter_complex \"[0][1]overlay={SX}:{SY}[a];[a][2]overlay=eof_action=pass,format=yuv420p\" -c:v libx264 -preset veryfast -crf 18 -an {T}v3.mp4")
parts.append(T + "v3.mp4")
# 4. tarjeta entrevistas
parts.append(render("c4", 1.5, LG, [
    Txt("ALUMNOS", font(SB, 38), B, 80, 700, .1),
    Txt("Nos explicaron", MJ(110), G, 80, 770, .22),
    Txt("qué significa", MJ(110), G, 80, 900, .34),
    Txt("su ofrenda", MJ(110), G, 80, 1030, .46)], lambda fr, t: picado_anim(fr, t, cols=(G, Y, B, P), bg=LG)))
# 5. entrevistas limpias
parts.append(clip(13.9, 3.0, T + "v5a.mp4")); parts.append(clip(23.3, 3.9, T + "v5b.mp4")); parts.append(clip(42.0, 5.0, T + "v5c.mp4"))
# 6. tarjeta baile
parts.append(render("c6", 1.5, B, [
    Txt("Y una presentación", MJ(96), C, 80, 760, .15),
    Txt("inspirada en", MJ(96), C, 80, 880, .3),
    Txt("Michael Jackson", MJ(104), Y, 80, 1000, .45, kind="pop")], lambda fr, t: picado_anim(fr, t, cols=(Y, P, LG, G), bg=B)))
# 7. baile limpio
parts.append(clip(34.0, 2.0, T + "v7a.mp4")); parts.append(clip(38.8, 3.0, T + "v7b.mp4"))
# 8. cierre animado
lg = logo("verdeclaro", 300)
def end_extra(fr, t):
    picado_anim(fr, t)
    p = ease((t - .15) / .45)
    if p > 0:
        im = lg.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * min(1, p))))
        fr.alpha_composite(im, (80, int(320 + 40 * (1 - p))))
parts.append(render("c8", 3.8, G, [
    Txt("Tradición,", MJ(100), C, 80, 560, .3), Txt("valores y", MJ(100), C, 80, 672, .42), Txt("comunidad.", MJ(100), C, 80, 784, .54),
    Txt("Preescolar y primaria en Coyoacán", font(SL, 40), LG, 80, 940, .8),
    Txt("Pide informes", font(SB, 48), G, 80, 1040, 1.0, kind="pop", bg=Y, pad=(48, 22)),
    Txt("WhatsApp 56 5292 2720", font(SB, 44), C, 80, 1190, 1.2),
    Txt("colegiominacion.com", font(SL, 44), C, 80, 1256, 1.3)], end_extra))
open(T + "all.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
run(f"ffmpeg -v error -y -f concat -safe 0 -i {T}all.txt -c copy {T}nomusic.mp4")
out = "/home/claude/colegiominacionsocialmedia/assets/2026-11/02-reel-recap/recap-ofrendas-v3.mp4"
D = float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {T}nomusic.mp4", shell=True))
run(f"ffmpeg -v error -y -i {T}nomusic.mp4 -i /home/claude/reel/src/guerita_34.mp3 -filter_complex \"[1]atrim=0:{D},afade=t=out:st={D-1.8}:d=1.8[a]\" -map 0:v -map \"[a]\" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart {out}")
print("ok", D)

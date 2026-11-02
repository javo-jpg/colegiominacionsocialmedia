"""Recap reel v2: video arriba, texto en panel inferior. Ningún texto sobre los niños.
Zonas seguras Reels 1080x1920: texto solo en x 80–960, y 270–1500 (abajo 420 px y derecha 120 px libres para la interfaz)."""
import sys, os, subprocess
sys.path.insert(0, "/home/claude/scripts")
from design import *
S = "/home/claude/reel/src/agencia.mp4"; T = "/home/claude/reel/tmp2/"; os.makedirs(T, exist_ok=True)
Wr, Hr, VH = 1080, 1920, 1180
def run(c): subprocess.run(c, shell=True, check=True)

def panel_png(path, eyebrow_t, lines, bg=C, fg=G, acc=B, big=False):
    im = Image.new("RGBA", (Wr, Hr), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, VH, Wr, Hr], fill=bg)
    picado(d, Wr, VH, 12, [Y, P, B, LG] if bg == G else [G, Y, B, P], bg, h=70)
    y = VH + 95
    if eyebrow_t: d.text((80, y), eyebrow_t.upper(), font=font(SB, 32), fill=acc); y += 52
    f = font(MIJA, 68 if big else 58)
    for l in lines: d.text((80, y), l, font=f, fill=fg); y += f.size * 1.1
    assert y < 1500, (lines, y)   # zona segura inferior
    im.save(path)

def seg(start, dur, crop, png, out):
    cw, ch, cx, cy = crop
    run(f"ffmpeg -v error -y -ss {start} -t {dur} -i {S} -loop 1 -i {png} -filter_complex "
        f"\"[0]crop={cw}:{ch}:{cx}:{cy},scale={Wr}:{VH}:flags=lanczos,setsar=1,pad={Wr}:{Hr}:0:0:color=black[v];"
        f"[1]format=rgba[p];[v][p]overlay=shortest=1,format=yuv420p\" -t {dur} -r 30 -an -c:v libx264 -preset veryfast -crf 18 {out}")

FULL_TOP = (1080, 1180, 0, 160)      # entrevistas: cara + micrófono
DANCE = (1080, 1180, 0, 440)
DET = (585, 639, 247, 880)           # detalles bajo el texto quemado de la agencia
panel_png(T + "hook.png", "Día de Muertos 2026", ["Así se vivió", "en Mi Nación"], G, C, Y, True)
panel_png(T + "ofr.png", "Ofrendas", ["Hechas por nuestros", "alumnos"])
panel_png(T + "ent.png", "Alumnos", ["Nos explicaron qué", "significa su ofrenda"], LG, G, G)
panel_png(T + "ent2.png", "Alumnos", ["Tradición que se aprende", "y se comparte"], LG, G, G)
panel_png(T + "com.png", "Comunidad", ["Toda la escuela", "reunida"], Y, G, G)
panel_png(T + "bai.png", "Presentación", ["Inspirada en", "Michael Jackson"], G, C, Y)
parts = []
plan = [(36.0, 2.8, DANCE, "hook"), (2.0, .8, DET, "ofr"), (3.6, .8, DET, "ofr"), (6.0, .8, DET, "ofr"), (9.5, .8, DET, "ofr"), (18.6, .8, DET, "ofr"),
        (13.9, 3.0, FULL_TOP, "ent"), (23.3, 3.9, FULL_TOP, "ent"), (42.0, 5.0, FULL_TOP, "ent2"), (13.0, .6, DANCE, "com"),
        (34.0, 2.0, DANCE, "bai"), (38.8, 3.0, DANCE, "bai")]
for k, (s, d_, cr, p) in enumerate(plan):
    seg(s, d_, cr, T + p + ".png", T + f"s{k}.mp4"); parts.append(T + f"s{k}.mp4")
from reels_end import end_card_safe
end_card_safe().save(T + "end.png")
run(f"ffmpeg -v error -y -loop 1 -i {T}end.png -vf \"fade=in:st=0:d=0.3,format=yuv420p\" -t 5 -r 30 -c:v libx264 -preset veryfast -crf 18 {T}end.mp4"); parts.append(T + "end.mp4")
open(T + "l.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
out = "/home/claude/colegiominacionsocialmedia/assets/2026-11/02-reel-recap/recap-ofrendas-v2.mp4"
run(f"ffmpeg -v error -y -f concat -safe 0 -i {T}l.txt -c copy -movflags +faststart {out}")
print("ok", out)

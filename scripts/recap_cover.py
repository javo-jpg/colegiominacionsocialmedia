import sys; sys.path.insert(0, "/home/claude/scripts")
from design import *
Wr, Hr = 1080, 1920
im = Image.new("RGB", (Wr, Hr), G); d = ImageDraw.Draw(im)
# textura: marca de agua del ojo
wm = eye(mix(G, C, .07), 900); im.paste(wm, (-260, 1180), wm)
picado(d, Wr, 0, 8, [Y, P, B, LG], G, h=200)
def polaroid(path, w, h, rot, focus=(.5, .5)):
    ph = cover(Image.open(path), w, h, focus)
    fr = Image.new("RGBA", (w + 36, h + 110), C + (255,)); fr.paste(ph, (18, 18))
    sh = Image.new("RGBA", (fr.width + 60, fr.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([30, 40, fr.width + 30, fr.height + 40], fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(14)); sh.alpha_composite(fr, (30, 30))
    return sh.rotate(rot, resample=Image.BICUBIC, expand=True)
M = "/home/claude/media/ofr/"
for path, w, h, rot, xy in [(M + "2_altar_primaria.jpg", 420, 520, 8, (560, 300)), (M + "3_cempasuchil.jpg", 380, 470, -10, (40, 330)), (M + "1_altar_kinder.jpg", 520, 600, -2, (260, 420))]:
    p = polaroid(path, w, h, rot); im.paste(p, xy, p)
d = ImageDraw.Draw(im)
# cempasúchil dibujado
def flor(cx, cy, r):
    for k in range(10):
        a = math.tau * k / 10; d.ellipse([cx + r * .55 * math.cos(a) - r * .45, cy + r * .55 * math.sin(a) - r * .45, cx + r * .55 * math.cos(a) + r * .45, cy + r * .55 * math.sin(a) + r * .45], fill=(235, 150, 40))
    d.ellipse([cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5], fill=Y)
flor(150, 1090, 60); flor(930, 1130, 44); sparkle(d, 860, 1200, 30, Y); sparkle(d, 250, 1230, 18, LG)
y = 1250
d.text((80, y), "Así se vivió", font=font(MIJA, 112), fill=C); y += 122
d.text((80, y), "el Día de Muertos", font=font(MIJA, 84), fill=Y)
w_ = d.textlength("el Día de Muertos", font=font(MIJA, 84))
pts = [(80 + t * w_ / 30, y + 104 + 8 * math.sin(t / 2.2)) for t in range(31)]; d.line(pts, fill=P, width=8, joint="curve")
assert y + 120 <= 1500
s = sello(True, 150).rotate(-12, resample=Image.BICUBIC, expand=True); im.paste(s, (Wr - 230, 260), s)
im.save("/home/claude/colegiominacionsocialmedia/assets/2026-11/02-reel-recap/portada.jpg", quality=93)
print("ok")

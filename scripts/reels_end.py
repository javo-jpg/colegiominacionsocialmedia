import sys
sys.path.insert(0, "/home/claude/scripts")
from design import *
# Zona segura Reels/Historias: texto y logos entre y=270 y y=1500, x=80 a x=960.
SAFE = (80, 270, 960, 1500)

def end_card_safe():
    Wr, Hr = 1080, 1920
    im = Image.new("RGB", (Wr, Hr), G); d = ImageDraw.Draw(im)
    picado(d, Wr, 0, 7, [Y, P, B, LG], G, h=150)
    lg = logo("verdeclaro", 300); im.paste(lg, (80, 300), lg)
    y = 300 + lg.height + 80
    f1 = font(MIJA, 96)
    for l in ["Tradición,", "valores y", "comunidad."]:
        d.text((80, y), l, font=f1, fill=C); y += 106
    f2 = font(SL, 40); y += 20
    d.text((80, y), "Preescolar y primaria en Coyoacán", font=f2, fill=LG); y += 54
    d.text((80, y), "Español · Inglés · Francés", font=f2, fill=LG); y += 90
    d.rounded_rectangle([80, y, 640, y + 96], radius=48, fill=Y); d.text((360, y + 48), "Pide informes", font=font(SB, 46), fill=G, anchor="mm"); y += 130
    d.text((80, y), "WhatsApp 56 5292 2720", font=font(SB, 44), fill=C); y += 60
    d.text((80, y), "colegiominacion.com", font=font(SL, 44), fill=C); y += 60
    assert y <= SAFE[3], y
    return im

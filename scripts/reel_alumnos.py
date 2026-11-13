from reel_real import build
I = "/home/claude/raw/int/"; R = "/home/claude/raw/prim/"
K = dict(zoom=1.7, cy=.6, audio=True)
segs = [
 dict(src=R+"VID_141741.src", ss=3.0, dur=2.6, txt=dict(pill="Primaria San Felipe", lines=["¿Qué dicen", "nuestros alumnos?"])),
 dict(src=I+"IMG_2842.mp4", ss=18.8, dur=4.2, subs=[(0, 4.2, "Me gusta por mis amigos y por los maestros")], **K),
 dict(src=I+"IMG_2842.mp4", ss=30.3, dur=3.7, subs=[(0, 3.7, "Me gusta mucho música y teatro")], **K),
 dict(src=I+"IMG_2836.mp4", ss=43.0, dur=12.0, subs=[(0, 3, "Me gusta venir a la escuela porque es divertido"), (3, 6, "Son muy pacientes"), (6, 9, "y tienen el tiempo para enseñarnos"), (9, 12, "y nos explican si no entendemos")], **K),
 dict(src=I+"IMG_2840.mp4", ss=11.0, dur=5.5, subs=[(0, 5.5, "Mis clases favoritas: inglés y francés")], **K),
 dict(src=I+"IMG_2836.mp4", ss=87.8, dur=3.4, subs=[(0, 3.4, "¡Bienvenidos a Colegio Mi Nación!")], **K),
]
print(build("alumnos-real", segs, "/home/claude/reel/src/shorelines45.mp3", "/home/claude/colegiominacionsocialmedia/assets/2026-11/reels-real"))

from reel_real import build
R = "/home/claude/raw/prim/"
segs = [
 dict(src=R+"VID_141741.src", ss=1.0, dur=3.0, txt=dict(pill="Primaria San Felipe", lines=["Así se vive", "la primaria"])),
 dict(src=R+"VID_141821.src", ss=4.0, dur=2.4, txt=dict(lines=["Aprender, crear", "y convivir"], y=1180)),
 dict(src=R+"VID_133916.src", ss=8.0, dur=3.0),
 dict(src=R+"IMG_2825.src", ss=1.0, dur=2.4),
 dict(src=R+"VID_133838.src", ss=4.0, dur=2.6),
 dict(src=R+"VID_140142.src", ss=18.0, dur=3.0),
 dict(src=R+"VID_134517.src", ss=11.6, dur=3.8, audio=True),
]
print(build("primaria-real", segs, "/home/claude/reel/src/littlegrin24.mp3", "/home/claude/colegiominacionsocialmedia/assets/2026-11/reels-real"))

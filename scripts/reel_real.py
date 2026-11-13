"""Reels con material real: clips verticales a pantalla completa, texto limpio solo en tomas sin niños.
Uso: from reel_real import build; build(name, segs, music, end_lines)"""
import subprocess, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/claude/scripts")
from design import *
from reels_end import end_card_safe

Wr, Hr, FPS = 1080, 1920, 30
TMP = "/home/claude/raw/tmp"; os.makedirs(TMP, exist_ok=True)
def run(c): subprocess.run(c, shell=True, check=True)

def text_png(lines, pill_t=None, path=None, y0=300, size=88):
    """Texto arriba (zona segura y 270-1500) con degradado suave detrás."""
    im = Image.new("RGBA", (Wr, Hr), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); y = y0
    if pill_t: pill(d, (80, y), pill_t, font(SB, 32), Y, G); y += 88
    f = font(MIJA, size)
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.rounded_rectangle([60, y - 6, 80 + w + 24, y + int(size * 1.08)], radius=18, fill=G + (255,))
        d.text((80, y), ln, font=f, fill=C); y += int(size * 1.2)
    assert y <= 1500
    im.save(path); return path

GRADE = "hqdn3d=1.5:1.5:6:6,eq=contrast=1.06:saturation=1.14:brightness=0.012:gamma=1.02,curves=preset=medium_contrast:master='0/0.02 0.5/0.52 1/0.98',unsharp=5:5:0.55"
def stab(src, ss, dur, i):
    trf = f"{TMP}/st{i:02d}.trf"
    run(f"ffmpeg -loglevel error -y -ss {ss} -t {dur} -i '{src}' -vf vidstabdetect=shakiness=6:accuracy=12:result={trf} -f null -")
    return f"vidstabtransform=input={trf}:smoothing=24:zoom=4:optzoom=0,"

def end_card_full():
    """Cortinilla de cierre: CTA + info general, dentro de zona segura."""
    im = canvas((Wr, Hr), G); d = ImageDraw.Draw(im)
    watermark(im, G, 5, "br", 620, .07)
    d = ImageDraw.Draw(im)
    lg = logo("verdeclaro", 300); im.paste(lg, (80, 300), lg); y = 300 + lg.height + 70
    for l in ["¿Quieres", "conocernos?"]:
        d.text((80, y), l, font=font(MIJA, 104), fill=C); y += 114
    y += 24
    d.rounded_rectangle([80, y, 700, y + 100], radius=50, fill=Y); d.text((390, y + 50), "Agenda tu visita", font=font(SB, 46), fill=G, anchor="mm"); y += 150
    for ic, t in [("WhatsApp", "56 5292 2720"), ("Teléfono", "55 5911 1865"), ("Web", "colegiominacion.com")]:
        d.text((80, y), ic, font=font(SL, 34), fill=LG); d.text((330, y - 4), t, font=font(SB, 42), fill=C); y += 64
    y += 20
    d.text((80, y), "Preescolar · Primaria · Coyoacán", font=font(SL, 36), fill=LG); y += 50
    d.text((80, y), "Español · Inglés · Francés", font=font(SL, 36), fill=LG); y += 50
    assert y <= 1500, y
    return im

def sub_png(text, path, y0=470, size=58):
    im = Image.new("RGBA", (Wr, Hr), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = font(SB, size)
    lines = wrap(d, text, f, Wr - 200); y = y0
    for ln in lines:
        w = d.textlength(ln, font=f); x = (Wr - w) / 2
        d.rounded_rectangle([x - 22, y - 8, x + w + 22, y + size + 10], radius=16, fill=G + (235,))
        d.text((x, y), ln, font=f, fill=C); y += size + 26
    assert y <= 1500; im.save(path); return path

def seg(i, src, ss, dur, txt=None, audio=False, still=False, zoom=None, cy=.62, cx=.5, subs=None, nostab=False):
    out = f"{TMP}/s{i:02d}.mp4"
    st = "" if (still or nostab or zoom) else stab(src, ss, dur, i)
    zc = ""
    if zoom:
        zc = f"crop=iw/{zoom}:ih/{zoom}:(iw-iw/{zoom})*{cx}:min(max(ih*{cy}-ih/{zoom}/2\\,0)\\,ih-ih/{zoom}),"
    vf = f"{st}{zc}scale={Wr}:{Hr}:force_original_aspect_ratio=increase,crop={Wr}:{Hr},setsar=1,fps={FPS},{GRADE}"
    if subs:
        ins = "".join(f" -loop 1 -t {dur} -i {sub_png(t, f'{TMP}/sub{i:02d}_{k}.png')}" for k, (a, b, t) in enumerate(subs))
        chain = "[0:v]" + vf + "[v0]"; last = "v0"
        for k, (a, b, t) in enumerate(subs):
            chain += f";[v{k}][{k+1}:v]overlay=0:0:enable='between(t,{a},{b})'[v{k+1}]"; last = f"v{k+1}"
        run(f"ffmpeg -loglevel error -y -ss {ss} -t {dur} -i '{src}'{ins} -filter_complex \"{chain}\" -map [{last}] -an -t {dur} -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {out}")
        return out
    if still:  # foto horizontal: zoom lento
        vf = f"scale=-2:{int(Hr*1.15)},crop={int(Wr*1.15)}:{int(Hr*1.15)},zoompan=z='1+0.0015*on':d={int(dur*FPS)}:s={Wr}x{Hr}:fps={FPS},setsar=1"
    inp = f"-loop 1 -t {dur} -i '{src}'" if still and src.endswith('.jpg') else f"-ss {ss} -t {dur} -i '{src}'"
    if txt:
        p = text_png(txt["lines"], txt.get("pill"), f"{TMP}/t{i:02d}.png", txt.get("y", 300))
        flt = f"[0:v]{vf}[v];[1:v]format=rgba,fade=t=in:st=0.2:d=0.4:alpha=1[t];[v][t]overlay=0:0[o]"
        run(f"ffmpeg -loglevel error -y {inp} -loop 1 -t {dur} -i {p} -filter_complex \"{flt}\" -map [o] -an -t {dur} -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {out}")
    else:
        run(f"ffmpeg -loglevel error -y {inp} -vf \"{vf}\" -an -t {dur} -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {out}")
    return out

def build(name, segs, music, out_dir, end=True, end_dur=3.5):
    parts, t, voice = [], 0.0, []
    for i, s in enumerate(segs):
        parts.append(seg(i, **{k: v for k, v in s.items() if k in ("src", "ss", "dur", "txt", "still", "zoom", "cy", "cx", "subs", "nostab")}))
        if s.get("audio"): voice.append((s["src"], s["ss"], s["dur"], t))
        t += s["dur"]
    if end:
        p = f"{TMP}/end.png"; end_card_full().save(p)
        out = f"{TMP}/send.mp4"
        run(f"ffmpeg -loglevel error -y -loop 1 -t {end_dur} -i {p} -vf \"fps={FPS},zoompan=z='1.04-0.04*on/{int(end_dur*FPS)}':d=1:s={Wr}x{Hr}:fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.35\" -c:v libx264 -preset veryfast -crf 20 {out}")
        parts.append(out); t += end_dur
    with open(f"{TMP}/list.txt", "w") as fh: fh.writelines(f"file '{p}'\n" for p in parts)
    run(f"ffmpeg -loglevel error -y -f concat -safe 0 -i {TMP}/list.txt -c copy {TMP}/v0.mp4")
    lg = logo("verdeclaro", 210); pad = Image.new("RGBA", (lg.width + 40, lg.height + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", pad.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([0, 0, pad.width - 1, pad.height - 1], radius=24, fill=(14, 24, 20, 90))
    pad.alpha_composite(sh); pad.alpha_composite(lg, (20, 15)); pad.save(f"{TMP}/logo.png")
    lx, ly = Wr - 60 - pad.width, 290  # arriba a la derecha, dentro de zona segura
    run(f"ffmpeg -loglevel error -y -i {TMP}/v0.mp4 -loop 1 -t 4 -i {TMP}/logo.png -filter_complex \"[1:v]format=rgba,fade=t=in:st=0:d=0.5:alpha=1,fade=t=out:st=3.4:d=0.6:alpha=1,setpts=PTS+5/TB[l];[0:v][l]overlay={lx}:{ly}:eof_action=pass\" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p {TMP}/v.mp4")
    # música baja; se agacha donde hablan los niños
    ins = f"-i {TMP}/v.mp4 -i '{music}'"; flt = []; mix = []
    duck = "+".join(f"between(t,{a-0.2:.2f},{a+d+0.2:.2f})" for _, _, d, a in voice) or "0"
    flt.append(f"[1:a]atrim=0:{t},asetpts=PTS-STARTPTS,volume='if({duck},0.12,0.5)':eval=frame,afade=t=in:d=0.4,afade=t=out:st={t-1.2:.2f}:d=1.2[m]"); mix.append("[m]")
    for k, (src, ss, d, a) in enumerate(voice):
        ins += f" -ss {ss} -t {d} -i '{src}'"
        flt.append(f"[{k+2}:a]volume=1.6,afade=t=in:d=0.15,afade=t=out:st={d-0.25:.2f}:d=0.25,adelay={int(a*1000)}|{int(a*1000)}[a{k}]"); mix.append(f"[a{k}]")
    flt.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,apad[a]")
    os.makedirs(out_dir, exist_ok=True)
    run(f"ffmpeg -loglevel error -y {ins} -filter_complex \"{';'.join(flt)}\" -map 0:v -map [a] -c:v copy -c:a aac -b:a 160k -t {t} {out_dir}/{name}.mp4")
    return f"{out_dir}/{name}.mp4", t

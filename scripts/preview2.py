import json, base64, io, glob, os, html
from PIL import Image
A = "/home/claude/colegiominacionsocialmedia/assets/2026-11/"
posts = [p for p in json.load(open("/home/claude/colegiominacionsocialmedia/plan/2026-11/posts.json")) if p["slug"] not in ("01-ofrendas", "02-reel-recap", "19-informes-reel")]
TAGS = "#ColegioMiNación #Coyoacán #Preescolar #Primaria"
extra = [
 dict(slug="01-ofrendas", fecha="2026-11-02", hora="18:00", tipo="Carrusel", pilar="Vida MN", estado="programado", caption="Este Día de Muertos, preescolar y primaria llenaron el colegio de color, memoria y tradición. 🌼\n\nLas familias nos acompañaron a recorrer las ofrendas y los trabajos que prepararon los alumnos para recordar a quienes queremos.\n\nGracias, comunidad Mi Nación, por mantener viva esta tradición con nosotros. 🧡\n\n¿Quieres conocer el colegio? Pide informes por WhatsApp: 56 5292 2720\n\n#ColegioMiNación #DíaDeMuertos #Coyoacán", nota="Programado en Metricool con 8 imágenes. Rocío confirma permisos antes de las 6:00 p. m.",
      files=[A+"01-ofrendas/01-portada.jpg", "/home/claude/media/altar_kinder.jpg", "/home/claude/media/altar_primaria.jpg", "/home/claude/media/patio_familias.jpg", "/home/claude/media/cempasuchil.jpg", A+"01-ofrendas/99-cta.jpg"]),
 dict(slug="02-reel-recap", fecha="2026-11-02", hora="16:12", tipo="Reel", pilar="Vida MN", estado="programado", video="v/recap.mp4", caption=f"Así se vivió el Día de Muertos en Mi Nación 💀🌼\n\nOfrendas hechas por nuestros alumnos, una presentación inspirada en Michael Jackson y toda la comunidad reunida.\n\nGracias a las familias, alumnos y maestros que lo hicieron posible. 💚\n\n{TAGS}", nota="Publicado hoy 2 nov a las 4:12 p. m. Motion graphics a pantalla completa, ofrendas con fotos originales en alta resolución. Música: Güerita, Epidemic Sound.",
      files=[A+"02-reel-recap/portada.jpg"]),
 dict(slug="19-informes-reel", fecha="2026-11-30", hora="13:00", tipo="Reel", pilar="Admisiones", estado="programado", video="v/informes.mp4", caption=f"¿Quieres información del colegio? Así de fácil la pides desde tu celular 📲\n\n1️⃣ Entra a colegiominacion.com\n2️⃣ Toca «Pedir informes»\n3️⃣ Elige WhatsApp, llamada o formulario\n\nTe contactamos pronto. 💚\n\n{TAGS}", nota="Cyber Monday. Música: Pearl City Beach, Epidemic Sound.", files=[A+"19-informes-reel/portada.jpg"]),
]
for p in posts:
    p["files"] = sorted(glob.glob(A + p["slug"] + "/*.jpg"))
    if p["slug"] == "08-preescolar-reel": p["video"] = "v/preescolar.mp4"; p["nota"] = p.get("nota", "") + " Música: Happy 4 U, Epidemic Sound."
    if p["slug"] == "04-papas-presentes": p["fecha"] = "2026-11-07"
allp = sorted(extra + posts, key=lambda p: (p["fecha"], p["hora"]))
# move reel recap date: Nov 3 (calendar slot 4 nov originally). keep.
def thumb(f, w=360, ratio=None):
    im = Image.open(f).convert("RGB")
    if ratio:
        tw, th = im.width, int(im.width / ratio)
        if th > im.height: th = im.height; tw = int(th * ratio)
        x = (im.width - tw) // 2; y = (im.height - th) // 2; im = im.crop((x, y, x + tw, y + th))
    im.thumbnail((w, w * 2)); b = io.BytesIO(); im.save(b, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
est = {"programado": ("Programado", "programado"), "listo": ("Listo para programar", "material"), "confirmar": ("Pendiente", "confirmar"), "levantamiento": ("Falta grabar", "levantamiento")}
pil = {"Vida MN": "#235D4E", "Admisiones": "#549EBB", "Propuesta": "#EDCC6F", "Papás Presentes": "#E8836B", "Familias": "#3E7A68"}
meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]; dias = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
import datetime
def fmt(s): d = datetime.date.fromisoformat(s); return f"{dias[d.weekday()]} {d.day} {meses[d.month-1]}"
pins = {"06-pedir-informes": 1, "15-papas-reel": 2, "04-papas-presentes": 3}
grid = []
for p in reversed(allp):
    t = thumb(p["files"][0], 360, 3 / 4)
    badge = "▶" if p["tipo"] == "Reel" else ("❐" if len(p["files"]) > 1 else "")
    pin = f'<span class="pin">FIJADO {pins[p["slug"]]}</span>' if p["slug"] in pins else ""
    grid.append(f'<a class="tile" href="#{p["slug"]}"><img src="{t}" alt="{html.escape(p["slug"])}"><span class="b">{badge}</span>{pin}</a>')
cards = []
RVB = lambda pid: f'<div class="rvb"><div><span class="rst">Pendiente</span></div><textarea aria-label="Comentario" placeholder="Comentario o cambios (opcional para aprobar)"></textarea><div class="acts"><button data-e="aprobado">Aprobar</button><button class="alt" data-e="cambios">Pedir cambios</button></div><div class="msg" role="status"></div><div class="log"></div></div>'
TODAY = "2026-11-12"
for p in allp:
    up = p["fecha"] >= TODAY
    lab, cls = est[p["estado"]]
    slides = "".join(f'<img src="{thumb(f, 300)}" alt="Lámina {k+1}" loading="lazy">' for k, f in enumerate(p["files"]))
    vid = f'<video src="{p["video"]}" controls playsinline preload="metadata" poster="{thumb(p["files"][0], 300)}"></video>' if p.get("video") else ""
    title = p["caption"].split("\n")[0]
    cards.append(f'''<article class="post{' rv' if up else ''}" data-id="{p["slug"]}" id="{p["slug"]}">
<header><div class="when"><b>{fmt(p["fecha"])}</b><span>{p["hora"]} · {p["tipo"]}{" · "+str(len(p["files"]))+" láminas" if len(p["files"])>1 else ""}</span></div>
<span class="pil" style="--c:{pil[p["pilar"]]}">{p["pilar"]}</span><span class="st {cls}">{lab}</span></header>
<div class="slides">{vid}{slides}</div>
<details><summary>Copy del post</summary><pre id="cap-{p["slug"]}">{html.escape(p["caption"])}</pre><button type="button" data-copy="cap-{p["slug"]}">Copiar copy</button></details>
{f'<p class="nota">{html.escape(p["nota"])}</p>' if p.get("nota") else ""}
{RVB(p["slug"]) if up else ""}
</article>''')
hl = []
for f in sorted(glob.glob("/home/claude/colegiominacionsocialmedia/assets/highlights/*.png")):
    n = os.path.basename(f)[3:-4]; im = Image.open(f).convert("RGB").crop((0, 420, 1080, 1500)).resize((120, 120)); b = io.BytesIO(); im.save(b, "JPEG", quality=80)
    hl.append(f'<figure><img src="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}" alt=""><figcaption>{ {"papas":"Papás","vida-mn":"Vida MN"}.get(n, n.capitalize()) }</figcaption></figure>')
tpl = open("/home/claude/scripts/preview2.tpl.html").read()
from solicitudes import render as sol_render
def stories_html():
    ss = sorted(json.load(open("/home/claude/colegiominacionsocialmedia/plan/2026-11/stories_v2.json")), key=lambda s: (s["fecha"], s["hora"]))
    weeks = {}
    for s in ss:
        d = datetime.date.fromisoformat(s["fecha"]); wk = d - datetime.timedelta(days=d.weekday()); weeks.setdefault(wk, []).append(s)
    out = []
    for wk, items in weeks.items():
        figs = "".join(f'<figure><img src="{thumb(A + s["poster"], 260)}" alt="" loading="lazy"><figcaption><b>{fmt(s["fecha"])} · {s["hora"]}</b>{s["uso"]}</figcaption></figure>' for s in items)
        rv = f'<div class="rv rvs" data-id="stories-{wk.isoformat()}"><b>Stories de esta semana</b>{RVB("")}</div>' if max(s["fecha"] for s in items) >= TODAY else ""
        out.append(f'<div class="wk2">Semana del {wk.day} de noviembre</div><div class="stw">{figs}</div>{rv}')
    return "".join(out)
REV = [
 ("primaria-real", "Reel · Así se vive la primaria", "Propuesta: mar 18 nov · nuevo", ["Fachada, biblioteca, computación y grupo gritando “¡Bienvenidos!” con su voz", "23 s · música Epidemic Sound"]),
 ("alumnos-real", "Reel · ¿Qué dicen nuestros alumnos?", "Propuesta: sáb 22 nov · nuevo", ["Amaya (3.º), Valentina y alumna en francés", "Subtítulos de transcripción automática: confirmar texto", "35 s · música Epidemic Sound"]),
]
def review_html():
    o = []
    for i, ti, when, notes in REV:
        li = "".join(f"<li>{n}</li>" for n in notes + ["Aparecen alumnos: confirmar autorización de imagen"])
        o.append(f'<article class="rv" data-id="{i}"><video src="v/{i}.mp4" poster="v/{i}.jpg" controls playsinline preload="none"></video><div><span class="rst">Pendiente</span></div><h3>{ti}</h3><div class="meta">{when}</div><ul>{li}</ul><textarea aria-label="Comentario" placeholder="Comentario o cambios (opcional para aprobar)"></textarea><div class="acts"><button data-e="aprobado">Aprobar</button><button class="alt" data-e="cambios">Pedir cambios</button></div><div class="msg" role="status"></div><div class="log"></div></article>')
    return "".join(o)
out = tpl.replace("__REVIEW__", review_html()).replace("__STORIES__", stories_html()).replace("__SOL__", sol_render()).replace("__GRID__", "".join(grid)).replace("__CARDS__", "".join(cards)).replace("__HL__", "".join(hl)).replace("__N__", str(len(allp)))
os.makedirs("/home/claude/prev", exist_ok=True)
open("/home/claude/prev/preview-noviembre.html", "w").write(out)
json.dump([{k: v for k, v in p.items() if k != "files"} for p in allp], open("/home/claude/colegiominacionsocialmedia/plan/2026-11/posts.json", "w"), ensure_ascii=False, indent=1)
print(len(allp), len(out) // 1024, "KB")

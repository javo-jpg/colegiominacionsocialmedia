import html
# Solicitudes de contenido para My Name Is Yellow (Armando Hernández y equipo).
# Cada solicitud: id, visita, formato, título, para qué publicación, idea, tomas, audio, personas/permisos, entrega.
VISITAS = [
 ("YA", "Sin grabar nada nuevo", "Material que ya existe"),
 ("V1", "Visita 1 · Preescolar Fresno", "Lunes 10 o martes 11 de noviembre, 8:30 a 11:30 a. m."),
 ("V2", "Visita 2 · Primaria San Felipe", "Miércoles 12 de noviembre, 8:30 a 12:00"),
 ("V3", "Visita 3 · 20 de noviembre", "Jueves 19 o viernes 20, solo si hay actividad escolar"),
 ("V4", "Visita 4 · Festival navideño", "Diciembre, fecha por confirmar con Rocío"),
 ("SEM", "Cada semana · maestras desde el celular", "Lunes a viernes, sin equipo de grabación"),
]
S = [
 dict(id="S-01", v="YA", fmt="Clips crudos", t="Entrevistas de ofrendas con audio original", para="Recap de ofrendas (voces de los niños)", prioridad=True,
      idea="Los videos originales, sin música, de los alumnos explicando su ofrenda con micrófono. Con ellos agregamos sus voces con subtítulos al recap.",
      tomas=["Todos los clips de entrevistas tal como salieron de la cámara o el celular", "También las entrevistas a alumnos y maestras de la primera visita"],
      audio="Audio original, sin música ni voz en off", gente="Solo alumnos con autorización", entrega="Hoy o mañana, en la carpeta de Drive /Ofrendas/crudos"),
 dict(id="S-02", v="V1", fmt="Reel 20–25 s", t="Un día en preescolar, desde la mochila", para="Reel 14 nov (reemplaza la versión con fotos)", prioridad=True,
      idea="Seguimos una mochila de la entrada a la salida. Sin rostros: manos, pies y espaldas, así funciona aunque haya niños sin autorización.",
      tomas=["Pies cruzando la puerta de Fresno 172", "Mochila colgándose en el perchero", "Manos saludando a la maestra", "Círculo de bienvenida desde atrás", "Manos con plastilina o material de LUCA", "Resbaladilla en cámara lenta (espaldas)", "Lunch abierto sobre la mesa", "Abrazo de despedida con papá o mamá (espaldas)"],
      audio="Sonido ambiente; la música la ponemos en edición", gente="Sin rostros", entrega="Vertical 4K, 8 tomas de 3–4 s, más 2 de respaldo cada una"),
 dict(id="S-03", v="V1", fmt="Reel 15–20 s", t="¿Cómo se dice…? en tres idiomas", para="Diciembre, serie de idiomas", prioridad=False,
      idea="Cada niño dice una palabra en español, inglés y francés frente a un fondo de color de la marca. Formato corto y fácil de compartir.",
      tomas=["6 niños, uno por toma, plano medio frente a pared lisa", "Palabras: manzana, apple, pomme / gato, cat, chat / gracias, thank you, merci", "Una toma de la maestra de francés diciendo «Bonjour !»"],
      audio="Micrófono de solapa o boom cerca; audio limpio es clave", gente="Solo niños con autorización y avisados el día anterior", entrega="Vertical, plano fijo con tripié"),
 dict(id="S-04", v="V1", fmt="Testimonio", t="Maestras de preescolar", para="Reel 17 nov", prioridad=True,
      idea="Dos maestras responden a cámara. Avisarles con días de anticipación para que vengan con la prenda del colegio.",
      tomas=["¿Qué es lo que más te gusta de enseñar aquí?", "¿Qué aprendió un niño contigo este año que te hizo sentir orgullosa?", "En una frase: ¿cómo es Mi Nación?", "B-roll: la maestra trabajando con el grupo (manos, espaldas)"],
      audio="Micrófono de solapa", gente="2 maestras de preescolar", entrega="Respuestas de 20–30 s cada una, más 4 tomas de apoyo"),
 dict(id="S-05", v="V1", fmt="Fotos", t="Así aprendemos jugando", para="Carrusel de diciembre", prioridad=False,
      idea="Detalles del salón y del trabajo de los niños. Sirven para muchos carruseles.",
      tomas=["10 fotos de detalle: manos con material, cuadernos, trabajos en la pared, juegos del patio", "2 fotos generales del salón sin niños", "Fachada y calle de Fresno 172 de día"],
      audio="—", gente="Sin rostros", entrega="Fotos verticales 4:5 y horizontales"),
 dict(id="S-06", v="V2", fmt="Fotos + clips", t="Nuestros aliados en el salón", para="Carrusel 19 nov (ya programado; se actualiza con fotos reales)", prioridad=True,
      idea="Una imagen real de cada aliado en uso para reemplazar las ilustraciones del carrusel.",
      tomas=["Innovamat: manos con material de matemáticas", "LUCA: pantalla con la actividad y manos", "Hachette: alumno leyendo (sobre el hombro)", "Tekman: trabajo en equipo en la mesa", "Nat Geo: actividad de ciencia o naturaleza", "Música: instrumentos en clase", "Un clip de 3 s de cada uno"],
      audio="Ambiente", gente="Preferir manos y espaldas", entrega="6 fotos 4:5 y 6 clips verticales; antes del 17 nov"),
 dict(id="S-07", v="V2", fmt="Testimonio", t="Familias: por qué elegimos Mi Nación", para="Reel 25 nov (fijado)", prioridad=True,
      idea="Tres papás o mamás a la salida. Rocío ayuda a elegir familias que quieran participar.",
      tomas=["¿Por qué eligieron Mi Nación?", "¿Desde cuándo están en el colegio?", "¿Qué ha cambiado en su hijo?", "Toma de la familia caminando hacia la entrada (puede ser de espaldas)"],
      audio="Micrófono de solapa", gente="3 familias con carta de autorización firmada", entrega="45–60 s por familia"),
 dict(id="S-08", v="V2", fmt="Reel 20 s", t="¿Qué quieres ser de grande?", para="Diciembre", prioridad=False,
      idea="Pregunta rápida a varios alumnos de primaria, estilo entrevista en la calle. Cierra con «En Mi Nación empiezan hoy».",
      tomas=["8–10 alumnos, una respuesta corta cada uno", "Pregunta extra: ¿qué es lo que más te gusta del colegio?"],
      audio="Micrófono de mano visible o solapa", gente="Solo alumnos con autorización", entrega="Vertical, respuestas de 3–5 s"),
 dict(id="S-09", v="V2", fmt="Clips", t="Clase de inglés y de francés", para="Carrusel de idiomas y reels de diciembre", prioridad=False,
      idea="Momentos reales de clase en otro idioma: una canción, una pregunta y respuesta, un juego.",
      tomas=["15 s de canción o saludo en francés", "15 s de conversación en inglés", "Pizarrón con palabras en los tres idiomas"],
      audio="Ambiente, sin música de fondo", gente="Grupo de espaldas o alumnos autorizados", entrega="Vertical"),
 dict(id="S-10", v="V2", fmt="Video 45 s + 3 cápsulas", t="Rocío presenta Papás Presentes", para="Posts de Papás Presentes en noviembre y diciembre", prioridad=True,
      idea="Rocío a cámara: qué es Papás Presentes, la lectura del mes y cómo enviar preguntas. Tres cápsulas de 20 s respondiendo preguntas de crianza.",
      tomas=["Presentación de 45 s", "3 respuestas de 20 s", "B-roll: Rocío con el libro en la mano"],
      audio="Micrófono de solapa, lugar silencioso", gente="Rocío", entrega="Vertical, luz de frente"),
 dict(id="S-11", v="V2", fmt="Fotos", t="Fachada y entrada de San Felipe", para="Carrusel 26 nov (ya programado; se actualiza)", prioridad=True,
      idea="La foto de primaria del carrusel de planteles es del altar; se cambia por la fachada.",
      tomas=["Fachada de frente, de día", "Entrada con el logo", "Calle para ubicar el plantel"],
      audio="—", gente="Sin personas", entrega="Antes del 24 nov"),
 dict(id="S-12", v="V2", fmt="Time-lapse", t="Ajedrez", para="Diciembre", prioridad=False,
      idea="Una partida en time-lapse desde arriba: solo tablero y manos.",
      tomas=["Cenital del tablero durante 5 minutos", "Detalle de una pieza moviéndose"],
      audio="—", gente="Solo manos", entrega="Celular en tripié cenital"),
 dict(id="S-13", v="V3", fmt="Cobertura", t="Actividad del 20 de noviembre", para="Post 20 nov (ya programado; se cambia por fotos reales)", prioridad=False,
      idea="Solo si el colegio hace desfile, festival o actividad deportiva.",
      tomas=["10–15 fotos", "5 clips de 3–5 s para un reel de 15 s"],
      audio="Ambiente", gente="Cuidar alumnos sin autorización", entrega="Mismo día, antes de las 3 p. m."),
 dict(id="S-14", v="V4", fmt="Cobertura completa", t="Festival o posada navideña", para="Recap de diciembre y campaña de inscripciones", prioridad=True,
      idea="La pieza más fuerte de diciembre. Dos personas: una en escenario y otra en familias.",
      tomas=["Presentaciones completas desde el frente", "Reacciones de familias (con autorización)", "3 entrevistas cortas a familias: ¿por qué recomendarías Mi Nación?", "Detalles de decoración"],
      audio="Audio del escenario y micrófono de solapa para entrevistas", gente="Lista de autorizaciones antes del evento", entrega="Selección en 48 h"),
 dict(id="S-15", v="SEM", fmt="Fotos y clips del celular", t="Momento de la semana", para="Historias diarias", prioridad=False,
      idea="Cada maestra manda de 5 a 8 fotos o clips cortos por semana de lo que pasa en su salón. Así hay historias sin esperar una visita.",
      tomas=["Una actividad", "Un trabajo terminado", "Un momento divertido"],
      audio="—", gente="Solo alumnos con autorización", entrega="Viernes, a la carpeta de Drive /Semana"),
]
def render():
    out = []
    for vid, name, when in VISITAS:
        items = [s for s in S if s["v"] == vid]
        cards = []
        for s in items:
            tomas = "".join(f"<li>{html.escape(x)}</li>" for x in s["tomas"])
            pr = '<span class="st confirmar">Prioridad</span>' if s["prioridad"] else ""
            cards.append(f'''<article class="sol">
<header><span class="sid">{s["id"]}</span><span class="fmt">{html.escape(s["fmt"])}</span>{pr}</header>
<h3>{html.escape(s["t"])}</h3>
<p class="para">Para: {html.escape(s["para"])}</p>
<p>{html.escape(s["idea"])}</p>
<details open><summary>Tomas</summary><ol>{tomas}</ol></details>
<dl><dt>Audio</dt><dd>{html.escape(s["audio"])}</dd><dt>Personas</dt><dd>{html.escape(s["gente"])}</dd><dt>Entrega</dt><dd>{html.escape(s["entrega"])}</dd></dl>
</article>''')
        out.append(f'<div class="visit"><div class="vh"><h3>{html.escape(name)}</h3><span>{html.escape(when)}</span></div><div class="sols">{"".join(cards)}</div></div>')
    return "".join(out)

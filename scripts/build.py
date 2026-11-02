import sys, json
sys.path.insert(0, "/home/claude/scripts")
from posts import *

WA = "WhatsApp: 56 5292 2720"
TAGS = "#ColegioMiNación #Coyoacán #Preescolar #Primaria"
posts = []
def add(slug, fecha, hora, tipo, pilar, estado, slides, caption, nota=""):
    for k, s in enumerate(slides, 1): save(s, slug, k)
    posts.append(dict(slug=slug, fecha=fecha, hora=hora, tipo=tipo, pilar=pilar, estado=estado, n=len(slides), caption=caption, nota=nota))

only = set(sys.argv[1:])
def want(s): return not only or s in only

# 03 Nueva web
if want("03-nueva-web"):
    n = 6
    add("03-nueva-web", "2026-11-05", "17:00", "Carrusel", "Admisiones", "listo", [
        L_phone(G, C, Y, "web_hero.jpg", "Nuevo en Mi Nación", "Nuestra nueva página ya está aquí", None, n, 0, crop=(0, 0, 800, 1500)),
        L_phone(C, G, B, "web_hero.jpg", "01 · Para los más pequeños", "Elige a tu compañero de aventura", "Tu hijo puede explorar la página con un personaje que lo acompaña.", n, 1, crop=(0, 560, 800, 1460)),
        L_phone(LG, G, G, "web_aliados.jpg", "02 · Cómo aprenden", "Conoce a nuestros aliados", "Qué es cada programa y cómo ayuda a tu hijo, con actividades para probar.", n, 2, crop=(0, 120, 800, 1500)),
        L_phone(G, C, Y, "web_papas.jpg", "03 · Para las familias", "Papás Presentes", "Un espacio gratuito con la lectura del mes y un buzón para preguntarle a Rocío.", n, 3, crop=(0, 120, 800, 1500)),
        L_phone(Y, G, G, "web_hero.jpg", "04 · Contacto directo", "Pide informes desde tu celular", "WhatsApp, llamada o formulario, siempre a la mano en la parte de abajo.", n, 4, crop=(0, 900, 800, 1640)),
        L_cta(C, G, G, "Explórala y cuéntanos qué te parece", "Entra a colegiominacion.com desde tu celular. Si tienes dudas, escríbenos.", n, 5, btn="Visitar la página"),
    ], f"¡Tenemos página nueva! 🎉\n\nAhora puedes conocer Colegio Mi Nación desde tu celular: cómo aprenden nuestros alumnos, los tres idiomas, nuestros aliados y Papás Presentes.\n\n👉 Los niños pueden elegir un personaje que los acompaña a explorar.\n👉 Pedir informes está a un toque: WhatsApp, llamada o formulario.\n\nEntra a colegiominacion.com y cuéntanos en los comentarios qué te gustó más. 💚\n\n{TAGS}")

# 04 Papás Presentes
if want("04-papas-presentes"):
    lib = Image.open("/home/claude/zip/Entrega/Mockups/Libro.jpg")
    n = 4
    add("04-papas-presentes", "2026-11-07", "11:00", "Carrusel", "Papás Presentes", "confirmar", [
        L_photo_panel(lib, "Papás Presentes", "Las grandes preguntas también se hacen en casa", "Un espacio gratuito para todas las familias, sean o no del colegio.", G, C, Y, (.5, .45), 720, n, 0),
        L_list(C, G, G, "Qué encuentras", "Así funciona Papás Presentes", [("book", "Un libro cada mes", "Leemos juntos y platicamos sobre lo que nos deja."), ("chat", "Preguntas para Rocío", "Envía tu pregunta desde la página; puedes pedir que no se publique tu nombre."), ("bulb", "Ideas para casa", "Actividades sencillas para hacer en familia."), ("heart", "Encuentros", "Espacios para conversar, en el colegio y en línea.")], n, 1),
        L_type(Y, G, G, "Lectura de noviembre", "Hijos felices", "De Sixto Porras. Durante el mes compartiremos ideas del libro para llevar a casa.", "book", n, 2),
        L_cta(G, C, Y, "Súmate, es gratis", "Entra a colegiominacion.com/papas-presentes y descubre la lectura del mes.", n, 3, btn="Ir a Papás Presentes"),
    ], f"Ser papá o mamá también se aprende, y nadie tiene que hacerlo solo. 💛\n\nPresentamos Papás Presentes, un espacio gratuito de Colegio Mi Nación para todas las familias, sean o no parte del colegio:\n📚 Un libro cada mes\n💬 Preguntas para Rocío\n🏡 Ideas y actividades para casa\n🤝 Encuentros para conversar\n\nEste mes leemos Hijos felices, de Sixto Porras.\n\nEntra a colegiominacion.com/papas-presentes 👈\n\n#PapásPresentes {TAGS}", "Confirmar con Rocío que Hijos felices es la lectura de noviembre.")

# 05 Tres idiomas
if want("05-tres-idiomas"):
    n = 6
    ilu = PH("ilustra_ninos.jpg")
    im = Image.new("RGB", (W, H), G); d = ImageDraw.Draw(im)
    for k, (t, c) in enumerate([("¡Hola!", Y), ("Hello!", LG), ("Bonjour !", B)]):
        f = font(MIJA, 150); d.text((80, 150 + k * 165), t, font=f, fill=c)
    eyebrow(d, (80, 690), "Tres idiomas desde preescolar", Y)
    text_block(d, (80, 744), "Español, inglés y francés en Mi Nación", font(MIJA, 66), C, W - 160, 1.1)
    ic = cover(ilu, 560, 380, (.5, .3)); paste_round(im, ic, (W - 600, H - 470), 36)
    lg = logo("verdeclaro", 210); im.paste(lg, (80, H - lg.height - 64), lg); page_dots(d, n, 0, H - 40, Y, (90, 130, 115))
    add("05-tres-idiomas", "2026-11-10", "13:00", "Carrusel", "Propuesta", "listo", [im,
        L_type(C, G, B, "¿Por qué tres idiomas?", "Más idiomas, más formas de ver el mundo", "Aprender otros idiomas desde pequeños ayuda a comunicarse con confianza y a conocer otras culturas.", "globe", n, 1),
        L_type(Y, G, G, "Español", "Leer, escribir y expresar lo que pienso", "La base para comprender, preguntar y contar sus propias ideas.", "letters", n, 2),
        L_type(B, C, Y, "English", "Hello, friends!", "Canciones, juegos y conversación para usar el inglés todos los días.", "chat", n, 3),
        L_type(P, C, Y, "Français", "Bonjour, les amis !", "Un tercer idioma que abre la curiosidad por otros países.", "star", n, 4),
        L_cta(C, G, G, "Certificación Cambridge English", "El colegio cubre su costo. Pregunta a admisiones en qué grado se presenta.", n, 5, btn="Pide informes"),
    ], f"Hola · Hello · Bonjour 👋\n\nEn Colegio Mi Nación tus hijos aprenden en tres idiomas: español, inglés y francés.\n\nAdemás, el colegio cubre el costo de la certificación Cambridge English. Pregunta a admisiones en qué grado se presenta.\n\n¿Quieres saber más? Pide informes por WhatsApp: 56 5292 2720\n\n#TresIdiomas #Bilingüe {TAGS}")

# 06 Cómo pedir informes (FIJAR)
if want("06-pedir-informes"):
    n = 5
    add("06-pedir-informes", "2026-11-12", "17:00", "Carrusel", "Admisiones", "listo", [
        L_photo_panel(PH("juegos2.jpg"), "Admisiones 2026–2027", "¿Cómo pedir informes? 3 caminos fáciles", None, G, C, Y, (.5, .55), 800, n, 0, tag="FIJADO"),
        L_list(C, G, G, "Elige el que te quede mejor", "Escríbenos, llámanos o déjanos tus datos", [("chat", "WhatsApp", "56 5292 2720. Te enviamos la información por mensaje."), ("phone", "Llamada", "55 5911 1865, de 9:00 a. m. a 3:30 p. m."), ("form", "Formulario", "En colegiominacion.com, botón Pedir informes.")], n, 1),
        L_type(Y, G, G, "Ven a vivirlo", "Una semana de experiencia sin costo", "Tu hijo puede conocer el colegio desde adentro. Fechas y disponibilidad se confirman con nosotros.", "calendar", n, 2),
        L_list(LG, G, G, "Dos planteles en Coyoacán", "¿Dónde estamos?", [("pin", "Preescolar · Fresno", "Fresno 172, Santa Úrsula Coapa, C.P. 04650."), ("pin", "Primaria · San Felipe", "San Felipe MZ532 LT4 (271), Pedregal de Santa Úrsula, C.P. 04600.")], n, 3, card=(255, 255, 255)),
        L_cta(G, C, Y, "¿Listo para conocernos?", "Escríbenos hoy y agenda tu visita.", n, 4),
    ], f"¿Buscas preescolar o primaria en Coyoacán? Así puedes pedir informes 👇\n\n💬 WhatsApp: 56 5292 2720\n📞 Llamada: 55 5911 1865 (9:00 a. m. a 3:30 p. m.)\n📝 Formulario: colegiominacion.com\n\n✨ Pregunta por la semana de experiencia sin costo.\n\n📍 Preescolar: Fresno 172, Santa Úrsula Coapa\n📍 Primaria: San Felipe MZ532 LT4 (271), Pedregal de Santa Úrsula\n\nGuarda este post para tenerlo a la mano 📌\n\n#Inscripciones {TAGS}", "Fijar en posición 1.")

# 07 Buen Fin
if want("07-buen-fin"):
    im = Image.new("RGB", (W, H), Y); d = ImageDraw.Draw(im)
    # price tag
    tag = Image.new("RGBA", (520, 300), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
    td.polygon([(0, 150), (110, 0), (520, 0), (520, 300), (110, 300)], fill=G + (255,)); td.ellipse([70, 130, 110, 170], fill=Y + (255,))
    td.text((320, 150), "$0", font=font(MIJA, 150), fill=C, anchor="mm")
    tag = tag.rotate(-8, expand=True, resample=Image.BICUBIC); im.paste(tag, (W - tag.width - 50, 110), tag)
    eyebrow(d, (80, 520), "Este Buen Fin", G)
    y = text_block(d, (80, 576), "La mejor inversión no tiene descuento: es su futuro.", font(MIJA, 92), G, W - 160, 1.06)
    text_block(d, (80, y + 26), "Vive una semana de experiencia sin costo en Mi Nación. Sujeto a disponibilidad.", font(SL, 40), INK, W - 160, 1.32)
    lg = logo("verde", 220); im.paste(lg, (80, H - lg.height - 64), lg)
    add("07-buen-fin", "2026-11-13", "13:00", "Post", "Admisiones", "confirmar", [im],
        f"Este Buen Fin, mientras todos buscan ofertas, te invitamos a algo que vale más: conocer dónde puede crecer tu hijo. 💚\n\nVive una semana de experiencia sin costo en Colegio Mi Nación (sujeto a disponibilidad).\n\nPide informes por WhatsApp: 56 5292 2720\n\n#BuenFin {TAGS}", "Confirmar con Rocío si habrá alguna promoción real; si no, se publica así.")

# 08 Conoce preescolar (reel slideshow) -> covers made here, video by reels.py
if want("08-preescolar-reel"):
    add("08-preescolar-reel", "2026-11-14", "11:00", "Reel", "Propuesta", "listo",
        [L_reel_cover(PH("juegos2.jpg"), "Conoce nuestro preescolar en Fresno", "Preescolar", (.5, .5))],
        f"Así es nuestro preescolar en Fresno 172, Santa Úrsula Coapa 🌳\n\nUn espacio para jugar, explorar y aprender en tres idiomas.\n\n¿Quieres conocerlo en persona? Agenda tu visita por WhatsApp: 56 5292 2720\n\n#Preescolar #Kinder {TAGS}", "Versión con fotos del plantel. Se reemplaza con 'Un día en preescolar' cuando haya levantamiento.")

# 09 Papás Presentes: preguntas para platicar
if want("09-preguntas-casa"):
    n = 5
    qs = ["¿Qué fue lo mejor de tu día?", "¿Qué te hizo sentir orgulloso esta semana?", "Si pudieras enseñarme algo, ¿qué sería?"]
    sl = [L_type(G, C, Y, "Papás Presentes", "3 preguntas para platicar en casa esta semana", "Para la cena, el camino a la escuela o antes de dormir.", "chat", n, 0)]
    for k, q in enumerate(qs):
        bg, fg, acc = [(C, G, B), (LG, G, G), (Y, G, G)][k]
        sl.append(L_type(bg, fg, acc, f"Pregunta {k+1}", q, "Escucha sin corregir. Lo importante es que se sienta escuchado.", None, n, k + 1, big=110))
    sl.append(L_cta(G, C, Y, "¿Te gustaron?", "Cuéntanos cómo te fue y envía tus preguntas a Rocío en colegiominacion.com/papas-presentes", n, 4, btn="Preguntarle a Rocío"))
    add("09-preguntas-casa", "2026-11-15", "18:00", "Carrusel", "Papás Presentes", "listo", sl,
        f"Las conversaciones más importantes a veces empiezan con una pregunta sencilla. 💬\n\nTe dejamos 3 preguntas para platicar con tus hijos esta semana. Guárdalas y cuéntanos cuál funcionó mejor.\n\nPapás Presentes es gratuito y abierto a todas las familias 💛\ncolegiominacion.com/papas-presentes\n\n#PapásPresentes {TAGS}")

# 10 Maestras reel (levantamiento) - cover
if want("10-maestras-reel"):
    add("10-maestras-reel", "2026-11-17", "13:00", "Reel", "Familias", "levantamiento",
        [L_reel_card(G, "Lo que más nos gusta de enseñar aquí", "Maestras Mi Nación", "heart", "Testimonios · se graba el 10–12 nov")],
        f"Les preguntamos a nuestras maestras qué es lo que más les gusta de enseñar en Mi Nación. 💚\n\n[Ajustar con sus respuestas]\n\n{TAGS}", "Portada lista. Falta grabar: 2 maestras de preescolar y 2 de primaria, 20–30 s cada una.")

# 11 Aliados
if want("11-aliados"):
    al = [("numbers", "Innovamat", "Pensamiento matemático", "Ayuda a comprender los números, buscar distintas soluciones y explicar cómo llegó a una respuesta.", Y, G, G),
          ("letters", "LUCA", "Lectoescritura en español e inglés", "Aprendizaje con juegos para reconocer palabras, leer y escribir.", B, C, Y),
          ("book", "Hachette", "Lectura y cultura general", "Materiales que fortalecen la comprensión lectora y la conversación sobre lo aprendido.", C, G, B),
          ("bulb", "Tekman", "Metodologías activas", "Participar, probar ideas y construir aprendizajes con acompañamiento.", LG, G, G),
          ("leaf", "Nat Geo Education", "Ciencia y naturaleza", "Curiosidad, observación, cuidado del ambiente y conocimiento del mundo.", G, C, Y),
          ("music", "Música", "Expresión y creatividad", "Sensibilidad, escucha, expresión de emociones y convivencia.", P, C, Y)]
    n = len(al) + 2
    sl = [L_phone(G, C, Y, "web_aliados.jpg", "Nuestros aliados", "Más herramientas, más posibilidades", "Programas y recursos que apoyan a los maestros y ayudan a tu hijo a pensar, leer, descubrir y expresarse.", n, 0, crop=(0, 120, 800, 1500), swipe_=True)]
    for k, (ic, name, area, txt, bg, fg, acc) in enumerate(al):
        sl.append(L_type(bg, fg, acc, f"{k+1:02d} · {area}", name, txt, ic, n, k + 1, big=104))
    sl.append(L_cta(C, G, G, "Pruébalos en nuestra página", "En colegiominacion.com hay una actividad para conocer cada aliado.", n, n - 1, btn="Pide informes"))
    add("11-aliados", "2026-11-19", "17:00", "Carrusel", "Propuesta", "listo", sl,
        f"¿Con qué aprenden nuestros alumnos? 🧩\n\nTrabajamos con aliados que apoyan a los maestros en el salón:\n🔢 Innovamat · pensamiento matemático\n🔤 LUCA · lectoescritura en español e inglés\n📚 Hachette · lectura y cultura general\n💡 Tekman · metodologías activas\n🌿 Nat Geo Education · ciencia y naturaleza\n🎵 Música · expresión y creatividad\n\nConoce cada uno y prueba sus actividades en colegiominacion.com\n\n{TAGS}", "Cuando haya levantamiento, sumar una foto real por aliado.")

# 12 20 de noviembre
if want("12-20-noviembre"):
    im = Image.new("RGB", (W, H), C); d = ImageDraw.Draw(im)
    picado(d, W, 0, 8, [G, Y, P, B], C)
    d.text((80, 230), "20", font=font(MIJA, 360), fill=G)
    d.text((80, 600), "de noviembre", font=font(MIJA, 80), fill=G)
    y = text_block(d, (80, 730), "Celebramos la Revolución Mexicana y el Día de la Niñez.", font(SB, 46), INK, W - 160, 1.25)
    text_block(d, (80, y + 20), "Cada niña y cada niño tiene derecho a jugar, aprender y ser escuchado. Eso cuidamos en Mi Nación todos los días.", font(SL, 38), INK, W - 160, 1.34)
    lg = logo("verde", 220); im.paste(lg, (80, H - lg.height - 64), lg)
    ilu = PH("ilustra_ninos.jpg"); ic = cover(ilu, 400, 300, (.5, .4)); paste_round(im, ic, (W - 470, 250), 30)
    add("12-20-noviembre", "2026-11-20", "13:00", "Post", "Vida MN", "listo", [im],
        f"Hoy recordamos la Revolución Mexicana 🇲🇽 y celebramos el Día de la Niñez.\n\nCada niña y cada niño tiene derecho a jugar, aprender y ser escuchado. Eso es lo que cuidamos en Mi Nación todos los días. 💚\n\n{TAGS}", "Si hay actividad escolar el 19 o 20, se cambia por cobertura.")

# 13 Pregúntale a Rocío
if want("13-pregunta-rocio"):
    im = Image.new("RGB", (W, H), G); d = ImageDraw.Draw(im)
    # speech bubbles
    for (x, y_, w_, h_, c, t) in [(80, 160, 700, 190, C, "¿Cómo le pongo límites sin gritar?"), (300, 390, 700, 190, Y, "¿Cuánto tiempo de pantallas es mucho?"), (80, 620, 700, 190, LG, "¿Cómo le ayudo con la tarea?")]:
        d.rounded_rectangle([x, y_, x + w_, y_ + h_], radius=50, fill=c)
        text_block(d, (x + 44, y_ + 44), t, font(SB, 44), G, w_ - 88, 1.18)
    eyebrow(d, (80, 900), "Papás Presentes", Y)
    text_block(d, (80, 956), "Pregúntale a Rocío", font(MIJA, 100), C, W - 160, 1.06)
    text_block(d, (80, 1080), "Envía tu pregunta en colegiominacion.com/papas-presentes. Puedes pedir que no se publique tu nombre.", font(SL, 36), LG, W - 160, 1.3)
    lg = logo("verdeclaro", 200); im.paste(lg, (80, H - lg.height - 50), lg)
    add("13-pregunta-rocio", "2026-11-21", "11:00", "Post", "Papás Presentes", "listo", [im],
        f"¿Tienes una pregunta sobre la crianza de tus hijos? 💬\n\nEnvíala a Rocío desde nuestra página. Puedes pedir que no se publique tu nombre. Las respuestas no son inmediatas: las compartimos en los espacios de Papás Presentes.\n\n👉 colegiominacion.com/papas-presentes\n\n#PapásPresentes {TAGS}", "Las preguntas de ejemplo son ilustrativas.")

# 14 Valores DARR
if want("14-valores"):
    vals = [("D", "Dignidad", "Todos valemos lo mismo. Nadie es más que nadie.", "Cuando un compañero se equivoca, no nos burlamos: lo ayudamos.", G, C, Y),
            ("A", "Agradecimiento", "Reconocer lo que otros hacen por nosotros.", "Dar las gracias a quien nos prepara el lunch o nos explica algo.", Y, G, G),
            ("R", "Respeto", "Escuchar y cuidar a los demás y sus cosas.", "Esperar nuestro turno para hablar y cuidar el material del salón.", B, C, Y),
            ("R", "Responsabilidad", "Hacernos cargo de lo que hacemos.", "Recoger lo que usamos y entregar nuestras tareas a tiempo.", P, C, Y)]
    n = 6
    im = Image.new("RGB", (W, H), C); d = ImageDraw.Draw(im)
    for k, (l, _, _, _, bg, fg, _) in enumerate(vals):
        x = 80 + k * 235; d.rounded_rectangle([x, 220, x + 215, 520], radius=40, fill=bg); d.text((x + 107, 370), l, font=font(MIJA, 190), fill=fg, anchor="mm")
    eyebrow(d, (80, 600), "Nuestros valores", B)
    text_block(d, (80, 656), "DARR: así se viven en el día a día", font(MIJA, 92), G, W - 160, 1.06)
    text_block(d, (80, 900), "Dignidad, Agradecimiento, Respeto y Responsabilidad, con ejemplos que los niños entienden.", font(SL, 38), INK, W - 160, 1.32)
    lg = logo("verde", 210); im.paste(lg, (80, H - lg.height - 64), lg); swipe(d, G); page_dots(d, n, 0, H - 40, G, (200, 200, 190))
    sl = [im]
    for k, (l, name, defi, ex, bg, fg, acc) in enumerate(vals):
        s = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(s)
        d.text((60, 40), l, font=font(MIJA, 420), fill=tuple(int(a * .82 + b * .18) for a, b in zip(bg, fg)))
        eyebrow(d, (80, 560), name, acc); y = text_block(d, (80, 616), defi, font(MIJA, 76), fg, W - 160, 1.08)
        d.rounded_rectangle([80, y + 40, W - 80, y + 300], radius=36, fill=C if bg != C else LG)
        eyebrow(d, (120, y + 76), "En el día a día", G, 26)
        text_block(d, (120, y + 120), ex, font(SB, 40), G, W - 240, 1.25)
        lg = logo("verdeclaro" if bg in (G, B, P) else "verde", 200); s.paste(lg, (80, H - lg.height - 64), lg)
        page_dots(d, n, k + 1, H - 40, acc, tuple(int(c * .55 + b * .45) for c, b in zip(bg, fg)))
        sl.append(s)
    sl.append(L_cta(C, G, G, "Valores que se aprenden juntos", "En casa y en la escuela. Conoce más en colegiominacion.com", n, 5))
    add("14-valores", "2026-11-23", "13:00", "Carrusel", "Propuesta", "listo", sl,
        f"En Mi Nación los valores no se memorizan: se viven. 💚\n\nD · Dignidad\nA · Agradecimiento\nR · Respeto\nR · Responsabilidad\n\nDesliza para ver cómo se ven en el día a día y cuéntanos: ¿cuál practican más en casa?\n\n#ValoresDARR {TAGS}")

# 15 Papás reel (levantamiento)
if want("15-papas-reel"):
    add("15-papas-reel", "2026-11-25", "17:00", "Reel", "Familias", "levantamiento",
        [L_reel_card(B, "¿Por qué elegimos Mi Nación?", "Familias Mi Nación", "chat", "Testimonios · se graba el 10–12 nov")],
        f"Nadie lo cuenta mejor que nuestras familias. 💚\n\n[Ajustar con sus respuestas]\n\n¿Quieres conocer el colegio? Pide informes por WhatsApp: 56 5292 2720\n\n{TAGS}", "Portada lista. Falta grabar 3 familias, 45–60 s cada una. Fijar en posición 2.")

# 16 Dos planteles
if want("16-planteles"):
    n = 4
    add("16-planteles", "2026-11-26", "13:00", "Carrusel", "Admisiones", "listo", [
        L_type(G, C, Y, "Dos planteles en Coyoacán", "Preescolar en Fresno. Primaria en San Felipe.", "Un mismo proyecto educativo, cerca de casa.", "pin", n, 0, swipe_=True),
        L_photo_panel(PH("juegos1.jpg"), "Preescolar · Fresno", "Fresno 172, Santa Úrsula Coapa", "C.P. 04650, Coyoacán", Y, G, G, (.5, .55), 820, n, 1),
        L_photo_panel(PH("altar_primaria.jpg"), "Primaria · San Felipe", "San Felipe MZ532 LT4 (271), Pedregal de Santa Úrsula", "C.P. 04600, Coyoacán", B, C, Y, (.5, .5), 760, n, 2),
        L_cta(C, G, G, "Ven a conocernos", "Agenda tu visita al plantel que te interesa.", n, 3),
    ], f"Estamos en dos planteles en Coyoacán 📍\n\n🌳 Preescolar · Fresno 172, Santa Úrsula Coapa, C.P. 04650\n🏫 Primaria · San Felipe MZ532 LT4 (271), Pedregal de Santa Úrsula, C.P. 04600\n\nAgenda tu visita por WhatsApp: 56 5292 2720\n\n{TAGS}", "Reemplazar foto de primaria por la fachada cuando se grabe.")

# 17 Agenda tu visita
if want("17-agenda-visita"):
    add("17-agenda-visita", "2026-11-27", "11:00", "Post", "Admisiones", "listo", [
        L_photo_full(PH("patio_familias.jpg"), "Antes de vacaciones", "Agenda tu visita y conoce Mi Nación", "Escríbenos por WhatsApp: 56 5292 2720", (.5, .5))],
        f"¿Estás buscando escuela para el próximo ciclo? Este es buen momento para conocernos. 🗓️\n\nAgenda tu visita antes de las vacaciones de diciembre y resuelve tus dudas en persona.\n\n💬 WhatsApp: 56 5292 2720\n📞 55 5911 1865 (9:00 a. m. a 3:30 p. m.)\n\n{TAGS}")

# 18 Cierre lectura
if want("18-cierre-lectura"):
    lib2 = Image.open("/home/claude/zip/Entrega/Mockups/Libr2.jpg")
    add("18-cierre-lectura", "2026-11-29", "18:00", "Post", "Papás Presentes", "confirmar", [
        L_photo_panel(lib2, "Papás Presentes · Diciembre", "Cerramos Hijos felices. Muy pronto, nueva lectura.", "Gracias a todas las familias que leyeron con nosotros.", G, C, Y, (.5, .5), 760)],
        f"Terminamos noviembre con Hijos felices 📚 Gracias a todas las familias que leyeron con nosotros.\n\nMuy pronto te contamos cuál será la lectura de diciembre. 👀\n\n#PapásPresentes {TAGS}", "Si Rocío confirma Educar con pasión, se anuncia el título.")

json.dump(posts, open(f"/home/claude/colegiominacionsocialmedia/plan/2026-11/posts{'_'+'_'.join(sorted(only)) if only else ''}.json", "w"), ensure_ascii=False, indent=1)
print("ok", [p["slug"] for p in posts])

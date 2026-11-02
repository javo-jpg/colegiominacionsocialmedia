# Zonas seguras (obligatorio en todas las piezas)

| Formato | Tamaño | Texto y logos solo en | Libre |
|---|---|---|---|
| Reel | 1080×1920 | x 80–960, y 270–1500 | 270 px arriba, 420 px abajo, 120 px a la derecha (botones) |
| Portada de reel | 1080×1920 | dentro de y 270–1500 (además el perfil la recorta a 3:4, y 240–1680) | igual que reel |
| Historia | 1080×1920 | x 80–1000, y 250–1580 | 250 px arriba, 340 px abajo |
| Post / carrusel | 1080×1350 | márgenes de 80 px (el perfil recorta 34 px por lado a 3:4) | — |

Reglas:
- Nunca poner texto sobre los niños. En video, el texto va en un panel de marca debajo del video.
- `scripts/posts.py` y `scripts/recap2.py` tienen `assert` que fallan si un texto sale de la zona segura.

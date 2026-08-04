# La Sana Doctrina No Morirá

Sitio web independiente del proyecto **La Sana Doctrina No Morirá**, construido a partir
del contenido de la página original en `ipdfv.com/la-sana-doctrina-no-morira`, pero con
identidad propia y en su propio dominio/repositorio.

Es un sitio **estático**: solo HTML, CSS y JavaScript. No necesita servidor, base de
datos ni instalación de dependencias.

## Estructura

Cada apartado del menú es **una página independiente**, con su propia dirección web
(por ejemplo `mision.html`), lo que permite compartir el enlace de una sección
concreta y ayuda a que Google la encuentre.

```
generar.py                EL GENERADOR: escribe todas las páginas. Ver abajo.
data/congresos.json       Única fuente de verdad de los congresos
data/COMO-AGREGAR-UN-CONGRESO.md   Instrucciones paso a paso
index.html                Portada: presentación, próximo congreso y cuenta regresiva
que-es.html               ¿Qué es? + Un Movimiento de Dios
apostasia.html            Enfrentando la Apostasía
mision.html               Nuestra Misión: los cuatro compromisos
iglesias.html             Iglesias que Viven la Sana Doctrina
remanente.html            ¿Eres Parte del Remanente? + «Quiero unirme»
pastores.html             Pastores Defensores (videos del congreso)
congresos/                Listado de congresos y una página por edición
congreso.html             Redirección a congresos/ (la dirección vieja, ya compartida)
contacto.html             Formulario y contacto directo
CNAME.ejemplo             Plantilla para cuando se compre el dominio propio
assets/css/estilo.css     Estilos (paleta azul marino y oro; el tema lo pone el sistema)
assets/js/main.js         Menú, cuenta regresiva, calendario, compartir, formularios
assets/img/logo.webp      Logotipo oficial (el que se muestra en la portada)
assets/img/logo.png       Respaldo del logotipo para navegadores antiguos
assets/img/logo-original.png  Copia maestra del logotipo, 1024 × 1024
assets/img/sello.webp     Emblema pequeño del encabezado (respaldo: sello.png)
assets/img/favicon.png    Icono de la pestaña del navegador
assets/img/emblema.svg    Versión vectorial del emblema, útil para imprimir
assets/img/sello.svg      Versión vectorial del escudo, sin la cinta
assets/img/fotos/         Fotografías del congreso (WebP + respaldo JPG)
assets/video/             Carpeta para los videos de los pastores
```

## El generador: `generar.py`

Los archivos `.html` **no se editan a mano**: los escribe `generar.py`. Por eso el
menú y el pie salen idénticos en todas las páginas sin tener que repetir el cambio
catorce veces.

Después de tocar `generar.py`, `data/congresos.json` o cualquier texto:

```bash
python3 generar.py
```

No hay que instalar nada: solo Python 3, que ya viene en Mac y Linux.

El generador escribe el HTML **ya terminado**. Eso importa: WhatsApp, Facebook y
Google no ejecutan JavaScript, así que el contenido y la imagen de vista previa
tienen que estar escritos en el archivo. El JavaScript solo se ocupa de lo que
depende de la hora en que alguien abre la página.

### Los tres valores que se cambian a mano

Están juntos al principio de `generar.py`, bajo `CONFIGURACIÓN`:

| Constante | Qué es |
|---|---|
| `SITIO` | El dominio. Es el **único** sitio donde aparece la dirección completa. |
| `CONTACTO` | Nombre, teléfono, WhatsApp y correo. Se cambian aquí y salen en todas las páginas. |
| `FORMULARIO_DESTINO` | Vacío a propósito: los formularios aún no envían. |

## Cómo verlo en tu computadora

Abre `index.html` con doble clic, o levanta un servidor local:

```bash
python3 -m http.server 8000
# luego abre http://localhost:8000
```

## Cómo publicarlo con GitHub Pages

1. En GitHub, entra a **Settings → Pages**.
2. En *Source* elige **Deploy from a branch**.
3. Selecciona la rama y la carpeta `/ (root)`.
4. Guarda. En unos minutos el sitio queda publicado.

El archivo `.nojekyll` ya está incluido para que GitHub publique los archivos tal cual.

## Cómo anunciar el congreso de cada año

Todos los congresos —los que vienen y los ya celebrados— salen de un solo archivo:
**`data/congresos.json`**. Ahí se edita, se ejecuta `python3 generar.py` y las
páginas se reescriben solas.

Las instrucciones campo por campo están en
[`data/COMO-AGREGAR-UN-CONGRESO.md`](data/COMO-AGREGAR-UN-CONGRESO.md).

De ese archivo salen cuatro cosas a la vez:

1. El bloque de próximos congresos de la portada.
2. La cuenta regresiva.
3. El listado de `congresos/`.
4. Una página propia por cada edición, en `congresos/<slug>/`.

### El estado no se escribe nunca

No hay ningún campo que diga «próximo» o «finalizado». Se deduce de las fechas, y
se vuelve a deducir cada vez que alguien abre la página. Por eso una edición que
termina deja de anunciarse como próxima **aunque nadie regenere el sitio en meses**.

| Situación | Qué muestra |
|---|---|
| Sin fecha confirmada | «Sede por anunciar» + «Estamos preparando la próxima edición» |
| Falta para el congreso | Cuenta regresiva en días, horas, minutos y segundos |
| Congreso en curso | «¡El congreso está en curso! Bienvenidos todos» |
| Ya terminó | Pasa a «Ediciones anteriores» y la portada asciende al siguiente |

### La dirección de cada congreso no cambia

Cada edición vive en `congresos/<slug>/`, por ejemplo
`congresos/2026-cartagena/`. Ese `slug` **no se cambia nunca** después de
publicarlo: si se cambia, se rompen los enlaces que la gente ya compartió.

La dirección vieja `congreso.html` sigue funcionando: redirige al listado.
## Las fotografías del congreso

Están en `assets/img/fotos/`, cada una en WebP (la que carga casi todo el mundo) y
JPG de respaldo, a 1600 px de ancho. Los originales de cámara, de 1,5 a 3,5 MB cada
uno, no se guardan en el repositorio: quedan en el historial de git, en el commit que
los subió.

Las catorce que hay ahora se reparten por sede:

- Las que tienen el emblema y los televisores al fondo son de **Newark, Nueva
  Jersey**, la primera edición, la de 2025.
- Las de predicación en el auditorio grande son de **Connecticut**.

| Archivos | Dónde aparecen |
|---|---|
| `pastor-retrato-*`, `pastor-predicando-*` | Galería de pastores de `pastores.html` |
| `predicacion-1` … `predicacion-8` | Connecticut: en `pastores.html` y en `congresos/2026-connecticut/` |
| `pastores-grupo`, `congreso-cartel`, `congreso-oracion`, `congreso-asamblea`, `congreso-grupo-1`, `congreso-grupo-2` | Newark: `congresos/2025-newark/` |
| `cartagena-*` (14 fotos) | Cartagena: `congresos/2026-cartagena/` |

Las galerías de cada congreso salen del campo `galeria` de
`data/congresos.json`, no del HTML. Para añadir fotos a una edición se
optimizan como las demás y se agregan a su lista `galeria`, con el ancho y el
alto reales.

Si una edición mezcla fotos verticales y horizontales, la galería pasa sola a
maquetación en columnas: recortar una vertical al formato común le cortaría la
cabeza a quien salga en ella.

Para añadir más fotos, súbelas al repositorio y regenera las versiones web:

```bash
python3 -c "
from PIL import Image, ImageOps
im = ImageOps.exif_transpose(Image.open('FOTO.jpeg')).convert('RGB')
im.thumbnail((1600, 1600), Image.LANCZOS)
im.save('assets/img/fotos/NOMBRE.webp', quality=80, method=6)
im.save('assets/img/fotos/NOMBRE.jpg', quality=78, optimize=True, progressive=True)
"
```

`exif_transpose` es importante: endereza las fotos que la cámara guardó giradas.

## Cómo poner los videos reales

En `pastores.html` hay cinco bloques con un marco de video
provisional (con las duraciones de la página original: 01:35, 01:06, 01:33, 01:45 y
01:17). Para publicar los videos verdaderos, sustituye el `<div class="video__marco">`
de cada bloque por una de estas dos opciones:

**a) Archivo propio** — copia el `.mp4` en `assets/video/`:

```html
<video controls preload="metadata" poster="assets/img/portada-1.jpg">
  <source src="assets/video/pastor-1.mp4" type="video/mp4">
</video>
```

**b) YouTube:**

```html
<div class="video__marco">
  <iframe style="width:100%;height:100%;border:0"
          src="https://www.youtube.com/embed/ID_DEL_VIDEO"
          title="Testimonio" allowfullscreen loading="lazy"></iframe>
</div>
```

Las instrucciones también están como comentario dentro del propio `pastores.html`.

## Qué falta por confirmar

Todo esto son datos que aún no tenemos. El sitio funciona sin ellos: los bloques
vacíos sencillamente no se dibujan, y la página irá creciendo a medida que se
rellene `data/congresos.json`.

- **Sede y fechas del próximo congreso.** Los tres celebrados ya pasaron, así que
  la portada está en modo «por anunciar». Cuando se confirme, se añade un congreso
  nuevo al JSON y se borra la entrada `por-anunciar`.
- **Afiches oficiales** de cada edición. Las tres tienen ya una fotografía de
  portada, que es lo que sale al compartir el enlace; el afiche, cuando exista,
  manda sobre ella.
- **Nombres de los pastores.** Los pies de foto describen la escena sin nombrar a
  nadie. Con los nombres mejoran también los textos alternativos.
- **Datos de cada congreso**: dirección, mapa, iglesia anfitriona, predicadores,
  horas del programa, logística y preguntas frecuentes. Todos los campos existen
  ya en el JSON, vacíos.
- **Correo de contacto.** Se usa `ig07644@gmail.com`. Si el oficial es otro, se
  cambia en el bloque `CONTACTO` de `generar.py`, en un solo sitio.
- **Envío de los formularios.** `FORMULARIO_DESTINO` está vacío: validan y avisan,
  pero no envían. Al poner ahí la URL de Formspree o Netlify Forms empiezan a
  funcionar sin tocar nada más.
- **Dominio propio.** Al comprarlo se sigue lo que explica `CNAME.ejemplo`.

## El logotipo

| Archivo | Para qué sirve |
|---|---|
| `assets/img/logo.webp` | El que ve la mayoría de visitantes (102 KB) |
| `assets/img/logo.png` | Respaldo para navegadores antiguos (86 KB, paleta de 256 colores) |
| `assets/img/logo-original.png` | Copia maestra tal como se recibió, 1024 × 1024 |
| `assets/img/sello.webp` | Emblema pequeño del encabezado, 48 px de alto (respaldo: `sello.png`) |
| `assets/img/favicon.png` | Icono de la pestaña del navegador, 64 × 64 |
| `assets/img/emblema.svg` | Versión vectorial del emblema, útil para imprimir a gran tamaño |
| `assets/img/sello.svg` | Versión vectorial del escudo sin la cinta |

Los cuatro primeros salen del mismo original, así que todos muestran el logotipo
verdadero. El navegador elige solo el formato: si acepta WebP carga el ligero, y si
no, el PNG.

Si más adelante regeneras las versiones web desde el original:

```bash
python3 -c "
from PIL import Image
src = Image.open('assets/img/logo-original.png')
rec = src.crop(src.getchannel('A').getbbox())   # quita el margen transparente

grande = rec.copy(); grande.thumbnail((674, 674), Image.LANCZOS)
grande.save('assets/img/logo.webp', quality=82, method=6)
grande.quantize(colors=256, method=Image.FASTOCTREE).save('assets/img/logo.png', optimize=True)

sello = rec.copy(); sello.thumbnail((160, 160), Image.LANCZOS)
sello.save('assets/img/sello.webp', quality=92, method=6)
sello.save('assets/img/sello.png', optimize=True)

w, h = rec.size; lado = int(w*0.72)
fav = rec.crop(((w-lado)//2, int(h*0.10), (w-lado)//2+lado, int(h*0.10)+lado))
fav.resize((64, 64), Image.LANCZOS).save('assets/img/favicon.png', optimize=True)
"
```

## Cómo cambiar los colores

Todos los colores están definidos como variables al principio de
`assets/css/estilo.css`, dentro del bloque `:root`. Cambiarlos ahí los cambia en
todas las páginas de golpe.

```css
:root {
  --negro:      #0d1f38;   /* azul marino: cabeceras oscuras y pie */
  --negro-osc:  #071426;   /* base de los degradados oscuros */
  --oro:        #c9a227;   /* rótulos pequeños y detalles dorados */
  --oro-claro:  #e4c669;   /* dorado sobre fondo oscuro */
  --hueso:      #f5f3ee;   /* fondo claro */
  --acento:     #1a4f95;   /* enlaces y botones */
  --acento-osc: #123a70;   /* al pasar el ratón */
  --filete:     var(--acento);          /* líneas de tarjetas y separadores */
  --brillo:     rgba(30, 90, 168, .34); /* resplandor de las cabeceras */
}
```

Debajo hay un bloque `@media (prefers-color-scheme: dark)` con los mismos roles para
el modo oscuro; conviene ajustarlo a la vez.

**El sitio no tiene interruptor de tema**: sigue automáticamente el ajuste de
apariencia del sistema operativo del visitante, y cambia en el momento si este lo
cambia, sin recargar la página.

Al elegir un acento nuevo, comprueba que el texto se siga leyendo: `--acento` debe
contrastar al menos 4,5 a 1 con el fondo claro. Si el acento es claro (un dorado, por
ejemplo), pon `--acento-texto: #14161a` para que las letras de los botones sean
oscuras en vez de blancas.

### Otras paletas listas para pegar

Sustituye los valores del bloque anterior por los de la que prefieras.

**Vino y crema**
```css
--negro: #1a1214;  --negro-osc: #0d0709;  --oro: #b8912f;  --oro-claro: #dcbb6a;
--hueso: #f7f2ea;  --acento: #7d1128;  --acento-osc: #560b1c;
--brillo: rgba(125, 17, 40, .38);
```

**Verde profundo y bronce**
```css
--negro: #0f1f19;  --negro-osc: #06120d;  --oro: #a8763a;  --oro-claro: #cf9d5f;
--hueso: #f4f2ec;  --acento: #19513e;  --acento-osc: #124232;
--brillo: rgba(29, 92, 70, .36);
```

**Grafito y oro** (el acento es claro, así que hay que cambiar también `--acento-texto`)
```css
--negro: #14161a;  --negro-osc: #08090b;  --oro: #a8842c;  --oro-claro: #d9bb6a;
--hueso: #f6f5f2;  --acento: #8f6d1f;  --acento-osc: #7c5d17;
--filete: var(--oro);  --brillo: rgba(168, 132, 44, .30);
```

## Notas técnicas

- Sin dependencias externas: no carga fuentes, scripts ni CSS de terceros.
- Responsivo, con menú móvil y navegación por teclado.
- Tema claro u oscuro automático según el sistema del visitante, sin interruptor.
- El menú resalta la página en la que estás.
- Respeta `prefers-reduced-motion`.
- El submenú «El proyecto» funciona sin JavaScript: su disparador es un enlace real
  a `que-es.html` y el CSS lo despliega con el puntero o el foco mientras el JS no
  se haya cargado.
- La cuenta regresiva está oculta a los lectores de pantalla (anunciar los segundos
  sería insoportable); en su lugar hay un resumen que solo cambia una vez al día.
- Los formularios abren el programa de correo del visitante (no requieren servidor).
  Si prefieres recibir los envíos en una bandeja sin abrir el correo, se puede
  conectar un servicio como Formspree cambiando el `<form>`.

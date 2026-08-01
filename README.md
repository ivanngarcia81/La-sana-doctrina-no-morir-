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
index.html                Portada: logotipo, presentación y accesos a todo el sitio
que-es.html               ¿Qué es? + Un Movimiento de Dios
apostasia.html            Enfrentando la Apostasía
mision.html               Nuestra Misión: los cuatro compromisos
iglesias.html             Iglesias que Viven la Sana Doctrina
remanente.html            ¿Eres Parte del Remanente? + suscripción
pastores.html             Pastores Defensores (videos del congreso)
congreso.html             Próximo congreso, cuenta regresiva y programa
contacto.html             Formulario y contacto directo
assets/css/estilo.css     Estilos (paleta azul marino y oro + tema claro/oscuro)
assets/js/main.js         Menú móvil, tema, animaciones, formularios
assets/img/logo.webp      Logotipo oficial (el que se muestra en la portada)
assets/img/logo.png       Respaldo del logotipo para navegadores antiguos
assets/img/logo-original.png  Copia maestra del logotipo, 1024 × 1024
assets/img/sello.svg      Escudo compacto para el encabezado y el favicon
assets/img/emblema.svg    Versión vectorial del emblema completo
assets/video/             Carpeta para los videos de los pastores
```

### Si hay que cambiar el menú o el pie de página

El encabezado (con el menú) y el pie se repiten en las nueve páginas, porque un sitio
estático no tiene forma de compartirlos. Si se agrega o se quita una sección, hay que
hacer el cambio en los nueve archivos `.html`. Lo demás —textos, imágenes, colores—
se edita en su propia página sin tocar las otras.

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

El congreso se celebra una vez al año y en una ciudad distinta, así que se actualiza
**en un solo lugar**: al principio de `assets/js/main.js` está el bloque `CONGRESO`.

```js
var CONGRESO = {
  edicion: 'Edición 2027',
  sede:    'Ciudad de Panamá, Panamá',
  fechas:  '16, 17 y 18 de julio de 2027',
  inicio:  '2027-07-16T09:00:00-05:00',
  fin:     '2027-07-18T23:59:00-05:00'
};
```

- `inicio` y `fin` van en formato ISO con la zona horaria de la sede
  (`-05:00` para Colombia y Panamá, `-04:00` para Nueva York en verano).
- Con eso se actualizan solos: la tarjeta de `congreso.html`, la cuenta regresiva y
  el aviso de la portada. No hay que tocar nada más.

La página se comporta sola en los tres casos:

| Situación | Qué muestra |
|---|---|
| Datos vacíos | «Sede por anunciar» + «Estamos preparando la próxima edición» |
| Falta para el congreso | Cuenta regresiva en días, horas, minutos y segundos |
| Congreso en curso | «¡El congreso está en curso! Bienvenidos todos» |
| Ya terminó | «Esta edición ya se celebró. Pronto anunciaremos la sede del próximo» |

Debajo de esa tarjeta, en `congreso.html`, va el programa por jornadas de la última
edición. Cuando se anuncie una nueva, reemplaza los tres textos de las jornadas y
cambia el título `Última edición · …`.

Para publicar el historial de congresos ya celebrados hay una plantilla lista como
comentario al final de esa misma página (`EDICIONES ANTERIORES`).

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

- **Sede y fechas del próximo congreso**: el de Cartagena (17–19 de julio de 2026)
  ya se celebró, así que la tarjeta está en modo «por anunciar». En cuanto se
  definan, se rellenan los cinco datos del bloque CONGRESO explicado arriba.
- **Fecha del tercer día de Cartagena**: en la captura no aparecía. Como el congreso
  empezó el viernes 17, se puso «domingo 19 julio 2026»; conviene confirmarlo.
- **Correo de contacto**: se usa `ig07644@gmail.com` en los dos formularios y en la
  tarjeta de contacto. Si el correo oficial es otro, cámbialo en `contacto.html` y en
  `remanente.html` (atributos `data-destino` y los enlaces `mailto:`).
- **Vista previa al compartir**: `og:image` apunta a una ruta relativa. Cuando el
  sitio tenga dominio propio conviene poner la dirección completa
  (`https://tudominio.com/assets/img/logo.png`) para que el logo salga al pegar el
  enlace en WhatsApp o Facebook.

## El logotipo

| Archivo | Para qué sirve |
|---|---|
| `assets/img/logo.webp` | El que ve la mayoría de visitantes (93 KB) |
| `assets/img/logo.png` | Respaldo para navegadores antiguos (455 KB) |
| `assets/img/logo-original.png` | Copia maestra tal como se recibió, 1024 × 1024 |
| `assets/img/sello.svg` | Escudo pequeño del encabezado y del icono de la pestaña |
| `assets/img/emblema.svg` | Versión vectorial completa, útil para imprimir a gran tamaño |

Para cambiar el logotipo basta con reemplazar `logo.webp` y `logo.png`. El navegador
elige solo el formato: si acepta WebP carga el ligero, y si no, el PNG.

El escudo del encabezado se deja en SVG a propósito: a 42 píxeles de alto el logotipo
completo con la cinta no se leería, y el sello solo (escudo y espada) se distingue
mucho mejor.

Si más adelante regeneras las versiones web desde el original:

```bash
python3 -c "
from PIL import Image
im = Image.open('assets/img/logo-original.png')
im = im.crop(im.getchannel('A').getbbox())   # quita el margen transparente
im.thumbnail((680, 680), Image.LANCZOS)
im.save('assets/img/logo.webp', quality=90, method=6)
im.save('assets/img/logo.png', optimize=True)
"
```

## Cómo cambiar los colores

Todos los colores están definidos como variables al principio de
`assets/css/estilo.css`, dentro del bloque `:root`. Cambiarlos ahí los cambia en las
nueve páginas de golpe.

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

Debajo hay dos bloques más —`prefers-color-scheme: dark` y `[data-tema="oscuro"]`—
con los mismos roles para el tema oscuro; conviene ajustarlos a la vez.

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
- Tema claro/oscuro automático, con botón para forzar la preferencia.
- El menú resalta la página en la que estás.
- Respeta `prefers-reduced-motion`.
- Los formularios abren el programa de correo del visitante (no requieren servidor).
  Si prefieres recibir los envíos en una bandeja sin abrir el correo, se puede
  conectar un servicio como Formspree cambiando el `<form>`.

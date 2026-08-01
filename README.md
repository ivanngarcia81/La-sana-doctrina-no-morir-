# La Sana Doctrina No Morirá

Sitio web independiente del proyecto **La Sana Doctrina No Morirá**, construido a partir
del contenido de la página original en `ipdfv.com/la-sana-doctrina-no-morira`, pero con
identidad propia y en su propio dominio/repositorio.

Es un sitio **estático**: solo HTML, CSS y JavaScript. No necesita servidor, base de
datos ni instalación de dependencias.

## Estructura

```
index.html                Página única con todas las secciones
assets/css/estilo.css     Estilos (paleta del emblema + tema claro/oscuro)
assets/js/main.js         Menú móvil, tema, animaciones, formularios
assets/img/emblema.svg    Emblema completo (escudo, espada y cinta)
assets/img/sello.svg      Versión compacta para el encabezado y el favicon
assets/video/             Carpeta para los videos de los pastores
```

## Secciones de la página

| Sección | Ancla |
|---|---|
| Portada — «Un Llamado a Permanecer Firmes en la Verdad» | `#inicio` |
| ¿Qué es «La Sana Doctrina No Morirá»? | `#que-es` |
| Enfrentando la Apostasía | `#apostasia` |
| Nuestra Misión (4 compromisos) | `#mision` |
| Iglesias que Viven la Sana Doctrina | `#iglesias` |
| ¿Eres Parte del Remanente? | `#remanente` |
| Un Movimiento de Dios | `#movimiento` |
| Pastores Defensores De La Sana Doctrina (videos) | `#pastores` |
| Próximo Congreso — Cartagena, Colombia | `#congreso` |
| Suscríbete para más información | `#suscribete` |
| Localización, horarios y contacto | `#contacto` |

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

## Cómo poner los videos reales

En la sección `#pastores` de `index.html` hay cinco bloques con un marco de video
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

Las instrucciones también están como comentario dentro del propio `index.html`.

## Qué falta por confirmar

- **Fecha del tercer día del congreso**: en la captura no aparece, por eso la tarjeta
  dice solo «Tercer día». Si es el domingo 19 de julio de 2026, cámbialo en la
  etiqueta `jornada__fecha`.
- **Correo de contacto**: se usa `ig07644@gmail.com` en los dos formularios y en la
  tarjeta de contacto. Si el correo oficial es otro, cámbialo en `index.html`
  (atributos `data-destino` y los enlaces `mailto:`).
- **Emblema**: `assets/img/emblema.svg` es una recreación en SVG del escudo con la
  espada y la cinta. Si tienes el archivo original en alta resolución (PNG o SVG),
  reemplázalo y quedará idéntico al de la iglesia.

## Notas técnicas

- Sin dependencias externas: no carga fuentes, scripts ni CSS de terceros.
- Responsivo, con menú móvil y navegación por teclado.
- Tema claro/oscuro automático, con botón para forzar la preferencia.
- El menú resalta la sección que se está leyendo.
- Respeta `prefers-reduced-motion`.
- Los formularios abren el programa de correo del visitante (no requieren servidor).
  Si prefieres recibir los envíos en una bandeja sin abrir el correo, se puede
  conectar un servicio como Formspree cambiando el `<form>`.

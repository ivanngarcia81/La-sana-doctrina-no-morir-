# La sana doctrina no morirá

Sitio web independiente para el ministerio de enseñanza **La sana doctrina no morirá**,
separado de la página de la congregación en `ipdfv.com` (que queda enlazada desde el pie
y desde la sección *Acerca*).

Es un sitio **estático**: solo HTML, CSS y JavaScript. No necesita servidor, base de datos
ni instalación de dependencias.

## Estructura

```
index.html          Portada: propósito, fundamentos, enseñanzas destacadas
ensenanzas.html     Biblioteca de estudios bíblicos
acerca.html         Visión, declaración de fe y compromisos
contacto.html       Formulario (abre el correo) y datos de contacto
assets/css/estilo.css   Estilos (incluye tema claro y oscuro)
assets/js/main.js       Menú móvil, tema, animaciones, formulario
assets/img/             Carpeta para logotipo e imágenes
```

## Cómo verlo en tu computadora

Abre `index.html` con doble clic, o levanta un servidor local:

```bash
python3 -m http.server 8000
# luego abre http://localhost:8000
```

## Cómo publicarlo con GitHub Pages

1. En GitHub, entra a **Settings → Pages**.
2. En *Source* elige **Deploy from a branch**.
3. Selecciona la rama (por ejemplo `main`) y la carpeta `/ (root)`.
4. Guarda. En unos minutos el sitio queda publicado.

El archivo `.nojekyll` ya está incluido para que GitHub publique los archivos tal cual.

## Qué personalizar

| Dónde | Qué cambiar |
|---|---|
| `contacto.html` | Correo (`data-destino` y el enlace), teléfono y horario |
| `acerca.html` | Declaración de fe y texto de la visión |
| `ensenanzas.html` | Reemplazar o ampliar los estudios |
| `assets/css/estilo.css` | Colores: variables `--tinta`, `--oro`, `--papel` al inicio |
| `assets/img/` | Colocar el logotipo y cambiar el sello `✝` del encabezado |

## Textos bíblicos

Las citas siguen la versión Reina-Valera 1960. Si se prefiere otra versión, se
pueden reemplazar directamente en el HTML.

## Notas técnicas

- Sin dependencias externas: no carga fuentes, scripts ni CSS de terceros.
- Responsivo, con menú móvil y navegación por teclado.
- Tema claro/oscuro automático, con botón para forzar la preferencia.
- Respeta `prefers-reduced-motion`.

# Cómo agregar un congreso

Todo lo que se ve de los congresos en el sitio sale de **`data/congresos.json`**.
No hay que tocar ningún HTML: se edita ese archivo, se ejecuta un comando y las
páginas se reescriben solas.

JSON no admite comentarios, por eso las explicaciones están aquí y no dentro
del archivo.

---

## Los tres pasos

**1. Abre `data/congresos.json`** y copia el bloque de un congreso que ya
exista, desde su `{` hasta su `}`. Pégalo como un bloque más dentro de
`"congresos"`, separado del anterior por una coma.

**2. Rellena los datos.** Lo único obligatorio es `slug`. Todo lo demás puede
quedar vacío (`""` para texto, `[]` para listas, `{}` para bloques) y
sencillamente no aparecerá en la página, sin dejar huecos.

**3. Ejecuta el generador** desde la carpeta del proyecto:

```
python3 generar.py
```

No hay que instalar nada. Después, sube los cambios a GitHub como siempre.

---

## Qué significa cada campo

### Identidad

| Campo | Para qué sirve |
|---|---|
| `slug` | La dirección de la página: `2026-cartagena` da `congresos/2026-cartagena/`. **Una vez publicado no se cambia nunca**, o se rompen los enlaces que la gente ya compartió. Solo minúsculas, números y guiones. |
| `edicion` | «Primera edición», «Segunda edición»… Se muestra sobre el título. |
| `nombre` | El nombre completo del congreso. |
| `tema` | El lema de esa edición, si lo tiene. |
| `descripcion` | Un párrafo de presentación. También es el texto que se ve al compartir el enlace por WhatsApp. |

### Fechas

| Campo | Para qué sirve |
|---|---|
| `fecha_inicio`, `fecha_fin` | Siempre en formato **`AAAA-MM-DD`**: `2026-07-17`. Es el único formato que entiende el generador. |
| `hora_inicio` | `19:00`, si se sabe. |
| `zona_horaria` | `America/Bogota`, `America/New_York`… |

> **El estado no se escribe.** No existe un campo «próximo» o «finalizado»: se
> calcula solo comparando las fechas con el día de hoy, tanto al generar el
> sitio como cada vez que alguien abre la página. Por eso un congreso que
> termina deja de anunciarse como próximo aunque nadie vuelva a generar nada.

### Lugar

`ciudad`, `estado`, `pais`, `direccion` (la dirección completa del local) y
`mapa` (el enlace de Google Maps). El mapa solo aparece si lo pones.

### Iglesias

Son **dos campos distintos** y los dos se muestran por separado:

- `iglesia_madre` — la iglesia que organiza el proyecto.
- `iglesia_anfitriona` — la congregación local que recibe el congreso en esa sede.

### Predicadores

Una lista. Cada predicador lleva `nombre`, `iglesia`, `ciudad`, `pais`, `foto`
y `bio_corta`. La `foto` es una ruta desde la raíz del proyecto, por ejemplo
`assets/img/predicadores/nombre.jpg`.

### Programa

Una lista de días. Cada día lleva:

- `fecha` en formato `AAAA-MM-DD` (el generador escribe solo «viernes 17 de julio»),
- `titulo` y `descripcion`,
- `bloques`: la lista de horas de ese día, cada una con `hora`, `actividad` y
  `predicador`. Si se deja vacía (`[]`) solo se ve el texto del día.

### Galería

Una lista de fotos ya publicadas en `assets/img/fotos/`. Cada una lleva:

- `archivo` — el nombre **sin extensión**: `congreso-oracion`, no
  `congreso-oracion.jpg`. Tienen que existir las dos versiones, `.webp` y `.jpg`.
- `ancho` y `alto` — las medidas reales en píxeles. Importan: sin ellas la
  página da un salto mientras carga la foto.
- `alt` — la descripción para quien no ve la imagen.
- `pie` — el texto bajo la foto, opcional.

### Lo demás

| Campo | Para qué sirve |
|---|---|
| `afiche` | Ruta de la imagen promocional, por ejemplo `assets/img/afiches/2027-panama.jpg`. Es la imagen que se ve al compartir el enlace por WhatsApp. Mientras no exista se muestra el sello del proyecto. |
| `modalidad` | `presencial`, `virtual` o `hibrido`. |
| `transmision` | Enlace de la transmisión en vivo, si la hay. |
| `logistica` | Bloque opcional con `estacionamiento`, `hospedajes`, `aeropuertos`, `transporte` y `ninos`. Cada uno aparece solo si tiene texto. |
| `faq` | Lista de `pregunta` y `respuesta`. |
| `contacto` | Contacto propio de ese congreso (`nombre`, `telefono`, `whatsapp`, `correo`). Si se deja vacío se usa el contacto general del sitio. |

---

## La entrada «por-anunciar»

Hay un congreso con `slug: "por-anunciar"` y todos los campos vacíos. Sirve
para que el sitio tenga algo que mostrar mientras no hay fecha confirmada.

Cuando se confirme la próxima sede, **no lo rellenes**: crea un bloque nuevo
con su `slug` definitivo (`2027-panama`, por ejemplo) y borra el de
`por-anunciar`. Así el enlace de cada edición nace ya con su dirección buena y
nunca cambia.

---

## Errores frecuentes

- **Una coma de más o de menos.** Es lo que más falla. Entre bloque y bloque va
  una coma; después del último, no. Si `python3 generar.py` se queja de
  `JSONDecodeError`, es esto: el mensaje dice la línea.
- **Fechas al revés.** `17-07-2026` no vale. Es `2026-07-17`.
- **Comillas rectas.** Dentro del JSON las comillas de programación son `"`. Si
  necesitas comillas dentro de un texto, usa las tipográficas: `“ ”`.
- **Olvidar ejecutar el generador.** Editar el JSON no cambia el sitio por sí
  solo. Hay que ejecutar `python3 generar.py` y subir los archivos que cambien.

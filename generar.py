#!/usr/bin/env python3
"""Genera todas las páginas del sitio a partir de una plantilla común.

    python3 generar.py

Se ejecuta a mano después de tocar este archivo, data/congresos.json o
cualquier texto del sitio. Escribe el HTML ya terminado: los buscadores y
la vista previa de WhatsApp leen el contenido sin ejecutar JavaScript.

No necesita instalar nada: solo Python 3.

FASE DE DISEÑO: los formularios no envían a ningún servicio y los datos de
contacto son provisionales.
"""
import datetime
import json
import os

# Raíz del sitio = la carpeta donde vive este archivo. Así funciona en
# cualquier equipo sin editar rutas.
RAIZ = os.path.dirname(os.path.abspath(__file__))

V = '?v=15'                      # invalidación de caché de los activos

# ==================================================================
#  CONFIGURACIÓN — LOS ÚNICOS VALORES QUE HAY QUE TOCAR A MANO
# ==================================================================

# Dominio público del sitio. Aparece solo en los metadatos que exigen una
# URL absoluta (canonical, og:, sitemap); todos los enlaces internos y las
# imágenes van con rutas relativas.
#
# AL COMPRAR EL DOMINIO PROPIO: cambiar esta línea, renombrar CNAME.ejemplo
# a CNAME con el dominio dentro y volver a ejecutar este archivo.
SITIO = 'https://ivanngarcia81.github.io/La-sana-doctrina-no-morir-/'

# Contacto del proyecto. Se escribe aquí una sola vez y sale en el pie de
# las páginas, en contacto.html y en las páginas de congreso que no tengan
# un contacto propio.
# FASE DE DISEÑO: datos provisionales.
CONTACTO = {
    'nombre':   'Pastor Junior Castillo',
    'telefono': '+1 862 241-6144',
    'pais_tel': 'EE.UU.',
    'whatsapp': '18622416144',   # solo dígitos, con el código de país
    'correo':   'ig07644@gmail.com',
}

# Destino de los formularios. FASE DE DISEÑO: vacío a propósito.
# Los formularios validan en el navegador pero no envían a ningún sitio.
# Para conectarlos más adelante basta con poner aquí la URL del servicio
# (Formspree, Netlify Forms, etc.); el HTML se adapta solo.
FORMULARIO_DESTINO = ''

# Fecha de la última revisión del contenido, para el sitemap.
ACTUALIZADO = '2026-08-04'


def tel_enlace():
    """El teléfono en el formato que exige tel:, sin espacios ni guiones.
       El signo + ya resuelve el código de salida de cada país: nunca se
       escribe 011 ni 00 delante."""
    return '+' + ''.join(c for c in CONTACTO['telefono'] if c.isdigit())

# (archivo, etiqueta, submenú)  — submenú None si es un enlace suelto
MENU = [
    ('index.html',     'Inicio',      None),
    (None,             'El proyecto', [('que-es.html',    '¿Qué es?'),
                                       ('apostasia.html', 'Apostasía'),
                                       ('mision.html',    'Misión')]),
    ('iglesias.html',  'Iglesias',    None),
    ('remanente.html', 'Remanente',   None),
    ('pastores.html',  'Pastores',    None),
    ('congresos/',     'Congresos',   None),
    ('contacto.html',  'Contacto',    None),
]

# Todas las páginas, para el pie (se muestran siempre las nueve)
TODAS = [
    ('index.html',     'Inicio'),
    ('que-es.html',    '¿Qué es?'),
    ('apostasia.html', 'Apostasía'),
    ('mision.html',    'Misión'),
    ('iglesias.html',  'Iglesias'),
    ('remanente.html', 'Remanente'),
    ('pastores.html',  'Pastores'),
    ('congresos/',     'Congresos'),
    ('contacto.html',  'Contacto'),
]


# ------------------------------------------------------------------
#  Encabezado y navegación
# ------------------------------------------------------------------
def dentro_de(destino, actual):
    """¿El enlace apunta a la página actual, o a la sección que la contiene?
       Devuelve 'pagina', 'seccion' o ''. Sirve para marcar «Congresos» en el
       menú cuando se está en la ficha de un congreso concreto."""
    if destino == actual:
        return 'pagina'
    if destino.endswith('/') and actual.startswith(destino):
        return 'seccion'
    return ''


def nav(actual, base=''):
    filas = []
    for archivo, etiqueta, submenu in MENU:
        if submenu is None:
            donde = dentro_de(archivo, actual)
            # aria-current="page" solo en la página exacta; en la sección
            # que la contiene basta con el resaltado visual.
            marca = {'pagina':  ' class="nav__enlace activo" aria-current="page"',
                     'seccion': ' class="nav__enlace activo"',
                     '':        ' class="nav__enlace"'}[donde]
            filas.append(f'        <li class="nav__item">'
                         f'<a href="{base}{archivo}"{marca}>{etiqueta}</a></li>')
        else:
            dentro = any(a == actual for a, _ in submenu)
            clase = 'nav__disparador activo' if dentro else 'nav__disparador'
            id_sub = 'submenu-proyecto'
            items = '\n'.join(
                f'            <li><a href="{base}{a}"'
                + (' class="activo" aria-current="page"' if a == actual else '')
                + f'>{e}</a></li>' for a, e in submenu)
            # Enlace real, no botón: sin JavaScript sigue llevando a la
            # primera página del grupo. El JS le añade el submenú.
            destino = base + submenu[0][0]
            filas.append(f"""        <li class="nav__item nav__grupo" data-grupo>
          <a href="{destino}" class="{clase}" aria-expanded="false"
             aria-controls="{id_sub}" aria-haspopup="true">
            {etiqueta}
            <svg class="nav__flecha" viewBox="0 0 12 12" width="11" height="11" aria-hidden="true">
              <path d="M2 4.5 6 8.5 10 4.5" fill="none" stroke="currentColor"
                    stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <ul class="nav__submenu" id="{id_sub}">
{items}
          </ul>
        </li>""")
    return '\n'.join(filas)


def encabezado(actual, base=''):
    return f"""<header class="encabezado">
  <div class="contenedor encabezado__fila">
    <a class="marca" href="{base}index.html">
      <picture class="marca__sello">
        <source srcset="{base}assets/img/sello.webp{V}" type="image/webp">
        <img src="{base}assets/img/sello.png{V}" alt="" width="159" height="160">
      </picture>
      <span class="marca__texto">
        <span class="marca__titulo">La Sana Doctrina</span>
        <span class="marca__lema">No Morirá</span>
      </span>
    </a>

    <nav class="nav" id="menu-principal" aria-label="Navegación principal">
      <ul class="nav__lista">
{nav(actual, base)}
      </ul>
    </nav>

    <div class="acciones">
      <button class="boton-menu" type="button" aria-label="Abrir menú"
              aria-expanded="false" aria-controls="menu-principal">
        <svg class="icono icono--barras" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
          <path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17"
                stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
        </svg>
        <svg class="icono icono--equis" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
          <path d="M5.5 5.5l13 13M18.5 5.5l-13 13"
                stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
  </div>
  <div class="encabezado__progreso" aria-hidden="true"></div>
</header>"""


# ------------------------------------------------------------------
#  Pie
# ------------------------------------------------------------------
def pie(actual, base=''):
    enlaces = '\n'.join(
        f'          <li><a href="{base}{a}"'
        + {'pagina':  ' class="pie__actual" aria-current="page"',
           'seccion': ' class="pie__actual"',
           '':        ''}[dentro_de(a, actual)]
        + f'>{e}</a></li>' for a, e in TODAS)
    return f"""<footer class="pie">
  <div class="contenedor">
    <div class="pie__rejilla">
      <div>
        <h4>La Sana Doctrina No Morirá</h4>
        <p class="pie__lema">
          Un llamado a permanecer firmes en la verdad. No es una organización, sino
          un clamor espiritual: ¡volver al fundamento de Cristo y su doctrina pura!
        </p>
      </div>

      <div>
        <h4>Secciones</h4>
        <ul class="pie__lista">
{enlaces}
        </ul>
      </div>

      <div>
        <h4>Contacto</h4>
        <!-- Los datos salen del bloque CONTACTO de generar.py: se cambian
             ahí una sola vez y se actualizan en todas las páginas. -->
        <ul class="pie__lista">
          <li>{CONTACTO['nombre']}</li>
          <li><a href="tel:{tel_enlace()}">{CONTACTO['telefono']} ({CONTACTO['pais_tel']})</a></li>
          <li><a href="https://wa.me/{CONTACTO['whatsapp']}"
                 target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:{CONTACTO['correo']}">{CONTACTO['correo']}</a></li>
        </ul>
      </div>
    </div>

    <div class="pie__final">
      <span>© <span data-anio>2026</span> La Sana Doctrina No Morirá. Todos los derechos reservados.</span>
      <span>“Retén la forma de las sanas palabras que de mí oíste…” — 2 Timoteo 1:13 · RVR1960</span>
    </div>
  </div>
</footer>"""


# ------------------------------------------------------------------
#  Documento
# ------------------------------------------------------------------
def pagina(archivo, titulo, descripcion, cuerpo, indexable=True,
           imagen='assets/img/logo.png', imagen_alt=None, cabeza='', extra=''):
    """Arma el documento completo.

       archivo  ruta relativa a la raíz del sitio, p. ej. 'contacto.html'
                o 'congresos/2026-cartagena/index.html'. De ahí se deducen
                solos la URL canónica y los '../' que necesitan los enlaces.
       imagen   ruta relativa de la imagen para compartir en redes. Se
                convierte en absoluta porque WhatsApp y Facebook no
                ejecutan JavaScript: la etiqueta tiene que venir escrita.
       cabeza   HTML extra dentro de <head>
       extra    HTML extra antes de cerrar <body>
    """
    titulo_completo = ('La Sana Doctrina No Morirá' if archivo == 'index.html'
                       else f'{titulo} — La Sana Doctrina No Morirá')

    # Profundidad: cada carpeta por encima de la raíz son unos '../'
    niveles = archivo.count('/')
    base = '../' * niveles

    # URL pública: las páginas 'index.html' se sirven por su carpeta
    ruta = '' if archivo == 'index.html' else archivo
    if ruta.endswith('/index.html'):
        ruta = ruta[:-len('index.html')]
    canonica = SITIO + ruta

    robots = '' if indexable else '\n<meta name="robots" content="noindex">'
    if imagen_alt is None:
        imagen_alt = 'Escudo con espada y la cinta «La sana doctrina no morirá»'
    imagen_abs = SITIO + imagen
    cabeza = ('\n' + cabeza) if cabeza else ''
    extra = ('\n' + extra) if extra else ''
    return f"""<!DOCTYPE html>
<html lang="es" class="sin-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo_completo}</title>
<meta name="description" content="{descripcion}">
<!-- El tema lo decide el sistema del visitante: color-scheme hace que
     también los controles nativos y las barras de desplazamiento se
     adapten, y theme-color tiñe la barra del navegador en cada modo. -->
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f5f3ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0e1621" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{canonica}">{robots}

<meta property="og:type" content="website">
<meta property="og:site_name" content="La Sana Doctrina No Morirá">
<meta property="og:title" content="{titulo_completo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:url" content="{canonica}">
<meta property="og:image" content="{imagen_abs}">
<meta property="og:image:alt" content="{imagen_alt}">
<meta property="og:locale" content="es_ES">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo_completo}">
<meta name="twitter:description" content="{descripcion}">
<meta name="twitter:image" content="{imagen_abs}">

<link rel="stylesheet" href="{base}assets/css/estilo.css{V}">
<link rel="icon" href="{base}assets/img/favicon.png{V}" type="image/png">
<link rel="apple-touch-icon" href="{base}assets/img/sello.png{V}">{cabeza}
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>

{encabezado(archivo, base)}

<main id="contenido">
{cuerpo}
</main>

{pie(archivo, base)}
{extra}
<script src="{base}assets/js/main.js{V}"></script>
</body>
</html>
"""


def cabecera(eyebrow, titulo, entrada=''):
    """Patrón común de las páginas interiores:
       rótulo dorado → H1 → subtítulo → separador azul."""
    parrafo = f'\n      <p class="portada__entrada">{entrada}</p>' if entrada else ''
    return f"""  <section class="portada portada--interior">
    <div class="contenedor">
      <p class="portada__antetitulo">{eyebrow}</p>
      <h1>{titulo}</h1>{parrafo}
      <div class="plomada plomada--clara"></div>
    </div>
  </section>
"""


FRANJA = """  <section class="franja">
    <div class="contenedor">
      <blockquote>
        “Porque vendrá tiempo cuando no sufrirán la sana doctrina; antes, teniendo
        comezón de oír, se amontonarán maestros conforme a sus propias
        concupiscencias.”
        <cite>2 Timoteo 4:3 · RVR1960</cite>
      </blockquote>
    </div>
  </section>
"""


def foto(nombre, alto, alt, clase='', pie='', prioridad=False, ancho=1600, base=''):
    """Foto real del congreso. WebP con respaldo JPG y medidas declaradas
       para que no salte la maquetación mientras carga."""
    carga = 'fetchpriority="high"' if prioridad else 'loading="lazy" decoding="async"'
    clases = ('foto ' + clase).strip()
    leyenda = f'\n      <figcaption class="foto__pie">{pie}</figcaption>' if pie else ''
    return f"""      <figure class="{clases}">
        <picture>
          <source srcset="{base}assets/img/fotos/{nombre}.webp{V}" type="image/webp">
          <img src="{base}assets/img/fotos/{nombre}.jpg{V}" width="{ancho}" height="{alto}"
               alt="{alt}" {carga}>
        </picture>{leyenda}
      </figure>"""


def campo(ident, nombre, etiqueta, tipo='text', requerido=False, auto='',
          opciones=None, area=False):
    """Un campo con su etiqueta y el hueco donde main.js escribe el error.
       El hueco va en el HTML para que el mensaje no desplace el resto de
       la página al aparecer."""
    req = ' required' if requerido else ''
    auto_attr = f' autocomplete="{auto}"' if auto else ''
    if opciones is not None:
        lista = '\n'.join(f'                <option>{o}</option>' for o in opciones)
        control = f'<select id="{ident}" name="{nombre}"{req}>\n{lista}\n              </select>'
    elif area:
        control = f'<textarea id="{ident}" name="{nombre}"{req}></textarea>'
    else:
        control = f'<input id="{ident}" name="{nombre}" type="{tipo}"{req}{auto_attr}>'
    return f"""            <div class="campo">
              <label for="{ident}">{etiqueta}</label>
              {control}
              <p class="campo__error" hidden></p>
            </div>"""


def formulario(asunto, campos, boton, clase=''):
    """Formulario con validación en el navegador y estado de envío.

       FASE DE DISEÑO: FORMULARIO_DESTINO está vacío, así que no se envía a
       ningún sitio. Al poner ahí la URL del servicio (Formspree, Netlify
       Forms…) el formulario empieza a enviar sin tocar nada más."""
    accion = (f' action="{FORMULARIO_DESTINO}" method="post"'
              if FORMULARIO_DESTINO else '')
    clases = ('formulario ' + clase).strip()
    return f"""      <form class="{clases}" data-formulario{accion}
            data-asunto="{asunto}" novalidate>
{campos}
        <div>
          <button class="boton boton--principal" type="submit">{boton}</button>
        </div>
        <p class="formulario__estado" role="status" aria-live="polite"
           data-estado-envio hidden></p>
      </form>"""


def tarjeta_enlace(href, indice, titulo, texto):
    return f"""        <a class="tarjeta tarjeta--enlace" href="{href}">
          <span class="tarjeta__indice">{indice}</span>
          <h3 class="tarjeta__titulo">{titulo}</h3>
          <p>{texto}</p>
        </a>"""


# ==================================================================
#  CONGRESOS — todo sale de data/congresos.json
# ==================================================================
with open(os.path.join(RAIZ, 'data', 'congresos.json'), encoding='utf-8') as f:
    CONGRESOS = json.load(f)['congresos']

HOY = datetime.date.today()

MESES = ('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
         'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre')
DIAS = ('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo')

ROTULO_ESTADO = {
    'por_anunciar': 'Por anunciar',
    'proximo':      'Próximo',
    'en_curso':     'En curso',
    'finalizado':   'Finalizado',
}


def _fecha(iso):
    return datetime.date.fromisoformat(iso) if iso else None


def estado_de(c):
    """El estado NUNCA se escribe en el JSON: se deduce de las fechas.

       El HTML se genera con el estado del día en que se ejecutó este
       archivo, y main.js lo vuelve a calcular al abrir la página. Así un
       congreso que ya pasó deja de anunciarse como próximo aunque nadie
       haya vuelto a generar el sitio."""
    ini = _fecha(c.get('fecha_inicio'))
    if not ini:
        return 'por_anunciar'
    fin = _fecha(c.get('fecha_fin')) or ini
    if HOY < ini:
        return 'proximo'
    if HOY <= fin:
        return 'en_curso'
    return 'finalizado'


def fechas_largas(c):
    """'viernes 17, sábado 18 y domingo 19 de julio de 2026'.
       Para periodos de más de tres días pasa a 'del … al …'."""
    ini = _fecha(c.get('fecha_inicio'))
    if not ini:
        return ''
    fin = _fecha(c.get('fecha_fin')) or ini
    dias = (fin - ini).days + 1
    if dias <= 3 and (ini.month, ini.year) == (fin.month, fin.year):
        nombres = []
        for i in range(dias):
            d = ini + datetime.timedelta(days=i)
            nombres.append(f'{DIAS[d.weekday()]} {d.day}')
        lista = nombres[0] if dias == 1 else ', '.join(nombres[:-1]) + ' y ' + nombres[-1]
        return f'{lista} de {MESES[ini.month - 1]} de {ini.year}'
    if ini.year != fin.year:
        return (f'del {ini.day} de {MESES[ini.month - 1]} de {ini.year} '
                f'al {fin.day} de {MESES[fin.month - 1]} de {fin.year}')
    if ini.month != fin.month:
        return (f'del {ini.day} de {MESES[ini.month - 1]} '
                f'al {fin.day} de {MESES[fin.month - 1]} de {ini.year}')
    return f'del {ini.day} al {fin.day} de {MESES[ini.month - 1]} de {ini.year}'


def fechas_cortas(c):
    """Versión compacta para las tarjetas del listado."""
    ini = _fecha(c.get('fecha_inicio'))
    if not ini:
        return 'Fecha por anunciar'
    fin = _fecha(c.get('fecha_fin')) or ini
    if ini == fin:
        return f'{ini.day} de {MESES[ini.month - 1]} de {ini.year}'
    if (ini.month, ini.year) == (fin.month, fin.year):
        return f'{ini.day}–{fin.day} de {MESES[ini.month - 1]} de {ini.year}'
    if ini.year == fin.year:
        return (f'{ini.day} de {MESES[ini.month - 1]} – '
                f'{fin.day} de {MESES[fin.month - 1]} de {ini.year}')
    return (f'{ini.day} de {MESES[ini.month - 1]} de {ini.year} – '
            f'{fin.day} de {MESES[fin.month - 1]} de {fin.year}')


def lugar(c):
    """El nombre corto de una sede, como se dice de viva voz: la ciudad con
       su estado si lo tiene («Newark, Nueva Jersey»), y si no, con el país
       («Cartagena, Colombia»). Sin ciudad, el estado con su país
       («Connecticut, Estados Unidos»)."""
    ciudad, estado, pais = (c.get('ciudad'), c.get('estado'), c.get('pais'))
    if ciudad:
        segundo = estado or pais
        return f'{ciudad}, {segundo}' if segundo else ciudad
    partes = [p for p in (estado, pais) if p]
    return ', '.join(partes) or 'Sede por anunciar'


def lugar_completo(c):
    partes = [p for p in (c.get('ciudad'), c.get('estado'), c.get('pais')) if p]
    return ', '.join(partes) or 'Sede por anunciar'


def momentos(c):
    """Inicio y fin para el archivo .ics y para Google Calendar.

       Un congreso de varios días se agenda como evento de día completo:
       es lo que corresponde y evita inventar una hora de cierre que no
       tenemos. Un evento de día completo tampoco se desplaza al cambiar
       de huso horario, que es la forma más segura de respetar la zona del
       congreso. El fin es exclusivo, por eso se suma un día."""
    ini = _fecha(c.get('fecha_inicio'))
    if not ini:
        return ('', '')
    fin = _fecha(c.get('fecha_fin')) or ini
    return (ini.isoformat(), (fin + datetime.timedelta(days=1)).isoformat())


def _orden(c):
    return c.get('fecha_inicio') or '9999-99-99'


PROXIMOS = sorted(
    [c for c in CONGRESOS if estado_de(c) in ('proximo', 'en_curso', 'por_anunciar')],
    key=_orden)
PASADOS = sorted([c for c in CONGRESOS if estado_de(c) == 'finalizado'],
                 key=_orden, reverse=True)


def datos_js():
    """Los mismos datos, incrustados en la propia página.

       Va en la página en vez de pedirse con fetch para que el contenido
       exista en el HTML: los buscadores y la vista previa de WhatsApp no
       ejecutan JavaScript. Este bloque solo alimenta lo que depende de la
       hora actual (estado y cuenta regresiva)."""
    ligeros = [{
        'slug':    c['slug'],
        'edicion': c.get('edicion', ''),
        'nombre':  c.get('nombre', ''),
        'lugar':   lugar(c),
        'fechas':  fechas_cortas(c),
        'inicio':  c.get('fecha_inicio', ''),
        'fin':     c.get('fecha_fin', ''),
    } for c in CONGRESOS]
    crudo = json.dumps(ligeros, ensure_ascii=False)
    # Un </script> dentro del texto cerraría la etiqueta antes de tiempo.
    crudo = crudo.replace('</', r'<\/')
    return f'<script type="application/json" id="datos-congresos">{crudo}</script>'


def insignia(c):
    est = estado_de(c)
    return (f'<span class="estado estado--{est}" data-estado '
            f'data-inicio="{c.get("fecha_inicio", "")}" '
            f'data-fin="{c.get("fecha_fin", "")}">{ROTULO_ESTADO[est]}</span>')


def imagen_de(c):
    """La imagen que representa a una edición, por orden de preferencia:

         1. el afiche oficial, si ya existe;
         2. la foto de portada, una de las de la galería;
         3. nada, y entonces se dibuja el sello del proyecto.

       Devuelve (ruta relativa, tipo, texto alternativo)."""
    if c.get('afiche'):
        return (c['afiche'], 'afiche',
                f'Afiche del congreso en {lugar(c)}')
    if c.get('portada'):
        nombre = c['portada']
        # El texto alternativo se reutiliza de la galería, para no
        # describir la misma foto dos veces con palabras distintas.
        alt = next((g.get('alt', '') for g in c.get('galeria', [])
                    if g.get('archivo') == nombre), '')
        return (f'assets/img/fotos/{nombre}.jpg', 'foto',
                alt or f'Fotografía del congreso en {lugar(c)}')
    return ('', '', '')


def afiche_img(c, base='', prioridad=False):
    """La imagen de la edición, con WebP y respaldo. Mientras no haya ni
       afiche ni foto se muestra el sello del proyecto, que encaja con el
       diseño en vez de dejar un hueco gris."""
    ruta, tipo, alt = imagen_de(c)
    carga = ('fetchpriority="high"' if prioridad
             else 'loading="lazy" decoding="async"')
    if tipo == 'foto':
        webp = ruta[:-4] + '.webp'
        return f"""<picture>
            <source srcset="{base}{webp}{V}" type="image/webp">
            <img class="afiche__imagen" src="{base}{ruta}{V}" alt="{alt}" {carga}>
          </picture>"""
    if tipo == 'afiche':
        return (f'<img class="afiche__imagen" src="{base}{ruta}{V}" '
                f'alt="{alt}" {carga}>')
    return f"""<span class="afiche__vacio" role="img"
              aria-label="Imagen pendiente de publicar">
          <img src="{base}assets/img/sello.png{V}" alt="" width="159" height="160"
               loading="lazy" decoding="async">
        </span>"""


def dato(etiqueta, valor):
    """Un par etiqueta/valor que desaparece si no hay dato."""
    if not valor:
        return ''
    return f"""            <div class="dato">
              <p class="dato__etiqueta">{etiqueta}</p>
              <p class="dato__valor">{valor}</p>
            </div>"""


def seccion_congreso(titulo, cuerpo, eyebrow='', alterna=False, ident=''):
    """Sección que solo se dibuja si tiene contenido."""
    if not cuerpo.strip():
        return ''
    clases = 'seccion seccion--alterna' if alterna else 'seccion'
    id_attr = f' id="{ident}"' if ident else ''
    rotulo = f'\n        <p class="seccion__eyebrow">{eyebrow}</p>' if eyebrow else ''
    return f"""  <section class="{clases}"{id_attr}>
    <div class="contenedor">
      <div class="seccion__encabezado revelar">{rotulo}
        <h2>{titulo}</h2>
        <div class="plomada"></div>
      </div>
{cuerpo}
    </div>
  </section>
"""


def el_proximo():
    """El congreso más cercano en el tiempo que todavía no ha terminado.
       Devuelve None si no hay ninguno con fecha confirmada."""
    con_fecha = [c for c in PROXIMOS if c.get('fecha_inicio')]
    return con_fecha[0] if con_fecha else None


def tarjeta_proximo(base=''):
    """Cuenta regresiva. La sede y las fechas van escritas en el HTML: sin
       JavaScript se sigue leyendo todo, solo falta el reloj. Cuando no hay
       fecha confirmada, en vez de un contador en cero se muestra el aviso."""
    c = el_proximo()
    if not c:
        return """      <article class="proximo revelar" data-proximo>
        <p class="proximo__edicion">Próxima edición</p>
        <h3 class="proximo__sede">Sede por anunciar</h3>
        <p class="proximo__fechas">Fecha por anunciar</p>
        <p class="cuenta__aviso">
          Estamos preparando la próxima edición. En cuanto se confirmen la sede
          y las fechas aparecerán aquí.
        </p>
        <div class="botones seccion__pie">
          <a class="boton boton--principal" href="{b}contacto.html">Proponer una sede</a>
        </div>
      </article>""".replace('{b}', base)
    return f"""      <article class="proximo revelar" data-proximo data-base="{base}"
               data-slug="{c['slug']}"
               data-inicio="{c['fecha_inicio']}" data-fin="{c.get('fecha_fin', '')}">
        <p class="proximo__edicion">{c.get('edicion', 'Próxima edición')}</p>
        <h3 class="proximo__sede">{lugar(c)}</h3>
        <p class="proximo__fechas">{fechas_largas(c)}</p>

        <!-- La cuenta se oculta a los lectores de pantalla: anunciar los
             segundos sería insoportable. El resumen de abajo la sustituye.
             Empieza oculta y la muestra el JS, para que sin JavaScript no
             se quede un marcador de guiones. -->
        <div class="cuenta" aria-hidden="true" hidden>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-dias>—</span><span class="cuenta__rotulo">Días</span></div>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-horas>—</span><span class="cuenta__rotulo">Horas</span></div>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-minutos>—</span><span class="cuenta__rotulo">Minutos</span></div>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-segundos>—</span><span class="cuenta__rotulo">Segundos</span></div>
        </div>
        <p class="cuenta__aviso" data-cuenta-mensaje hidden></p>
        <p class="visualmente-oculto" aria-live="polite" data-cuenta-resumen></p>

        <div class="botones seccion__pie">
          <a class="boton boton--principal" href="{base}congresos/{c['slug']}/">Ver detalles</a>
        </div>
      </article>"""


def aviso_portada(base=''):
    """La cinta del encabezado de la portada."""
    c = el_proximo()
    if c:
        marca, texto = 'Próximo congreso', f'{lugar(c)} · {fechas_cortas(c)}'
    else:
        marca, texto = 'Congreso anual', 'Próxima sede y fecha por anunciar'
    return f"""      <a class="aviso" href="{base}congresos/" data-aviso>
        <span class="aviso__marca" data-aviso-marca>{marca}</span>
        <span class="aviso__texto" data-aviso-texto>{texto}</span>
        <span class="aviso__flecha" aria-hidden="true">→</span>
      </a>"""


def bloque_proximos(base=''):
    """Sección de la portada: cuenta regresiva y tarjetas de lo que viene."""
    # Si ya hay una edición con fecha, la cuenta regresiva de arriba habla
    # de ella: repetirla en tarjeta sería decir dos veces lo mismo.
    otros = [c for c in PROXIMOS if c.get('fecha_inicio')][1:]
    tarjetas = '\n' + rejilla_congresos(otros, base) if otros else ''
    return f"""  <section class="seccion seccion--centrada" id="proximo-congreso">
    <div class="contenedor">
      <div class="seccion__encabezado revelar">
        <p class="seccion__eyebrow">Una ciudad distinta cada vez</p>
        <h2>Próximo congreso</h2>
        <div class="plomada"></div>
      </div>

{tarjeta_proximo(base)}{tarjetas}

      <p class="seccion__pie">
        <a class="boton boton--linea" href="{base}congresos/">Ver todas las ediciones</a>
      </p>
    </div>
  </section>
"""


def ficha(c):
    """La página de un congreso. Cada bloque aparece solo si tiene datos:
       mientras el congreso se organiza, la página va creciendo sola a
       medida que se rellena data/congresos.json."""
    b = '../../'          # profundidad: congresos/<slug>/index.html
    est = estado_de(c)
    ini_ics, fin_ics = momentos(c)
    titular = ' · '.join(p for p in (c.get('edicion'), lugar(c)) if p)

    # ---------- portada ----------
    tema = f'\n      <p class="portada__entrada">{c["tema"]}</p>' if c.get('tema') else ''
    partes = [f"""  <section class="portada portada--interior portada--congreso">
    <div class="contenedor">
      <p class="portada__antetitulo">{c.get('edicion', 'Congreso')}</p>
      {insignia(c)}
      <h1>{lugar(c)}</h1>
      <p class="portada__fechas">{fechas_largas(c) or 'Fecha por anunciar'}</p>{tema}
      <div class="plomada plomada--clara"></div>
    </div>
  </section>
"""]

    # ---------- afiche y descripción ----------
    descripcion = (f'<p class="texto-guia">{c["descripcion"]}</p>'
                   if c.get('descripcion') else '')
    partes.append(f"""  <section class="seccion" id="resumen">
    <div class="contenedor">
      <div class="afiche revelar">
        <figure class="afiche__marco afiche__marco--{imagen_de(c)[1] or 'vacio'}">
          {afiche_img(c, b, prioridad=True)}
        </figure>
        <div class="afiche__texto">
          <h2>{c.get('nombre', 'Congreso La Sana Doctrina No Morirá')}</h2>
          {descripcion}
          <p class="aviso-libre"><strong>Entrada libre.</strong> No se cobra
             inscripción ni boleta: el congreso es de acceso gratuito.</p>
          <div class="botones" data-acciones
               data-nombre="{c.get('nombre', 'Congreso La Sana Doctrina No Morirá')} — {lugar(c)}"
               data-inicio="{ini_ics}" data-fin="{fin_ics}"
               data-hasta="{c.get('fecha_fin', '')}"
               data-lugar="{lugar_completo(c)}"
               data-slug="{c['slug']}">
            <!-- Los dos botones nacen ocultos y los enseña main.js: sin
                 JavaScript no harían nada, así que es mejor que no estén. -->
            <button class="boton boton--principal" type="button" data-calendario
                    hidden>Agregar al calendario</button>
            <button class="boton boton--fantasma" type="button" data-compartir
                    hidden>Compartir</button>
          </div>
          <div class="compartir" id="compartir" data-compartir-lista hidden></div>
        </div>
      </div>
    </div>
  </section>
""")

    # ---------- datos prácticos ----------
    mapa = c.get('mapa', '')
    enlace_mapa = (f'<a href="{mapa}" target="_blank" rel="noopener">Ver en el mapa</a>'
                   if mapa else '')
    hora = c.get('hora_inicio', '')
    if hora and c.get('zona_horaria'):
        hora = f'{hora} ({c["zona_horaria"].split("/")[-1].replace("_", " ")})'
    modalidad = {'presencial': 'Presencial', 'virtual': 'Virtual',
                 'hibrido': 'Presencial y en línea'}.get(c.get('modalidad', ''), '')
    transmision = c.get('transmision', '')
    if transmision:
        transmision = (f'<a href="{transmision}" target="_blank" '
                       f'rel="noopener">Ver la transmisión</a>')
    practicos = ''.join([
        dato('Fechas', fechas_largas(c)),
        dato('Hora de inicio', hora),
        dato('Lugar', lugar_completo(c)),
        dato('Dirección', c.get('direccion', '')),
        dato('Mapa', enlace_mapa),
        dato('Modalidad', modalidad),
        dato('Transmisión en vivo', transmision),
        dato('Iglesia madre', c.get('iglesia_madre', '')),
        dato('Iglesia anfitriona', c.get('iglesia_anfitriona', '')),
    ])
    partes.append(seccion_congreso(
        'Datos del congreso', f'      <div class="tarjeta revelar">\n{practicos}\n      </div>'
        if practicos else '', eyebrow='Dónde y cuándo', alterna=True, ident='datos'))

    # ---------- predicadores ----------
    tarjetas = []
    for p in c.get('predicadores', []):
        procedencia = ', '.join(x for x in (p.get('iglesia'), p.get('ciudad'),
                                            p.get('pais')) if x)
        retrato = (f'<img class="predicador__foto" src="{b}{p["foto"]}{V}" alt="" '
                   f'loading="lazy" decoding="async">' if p.get('foto') else '')
        bio = f'<p>{p["bio_corta"]}</p>' if p.get('bio_corta') else ''
        tarjetas.append(f"""        <article class="tarjeta predicador">
          {retrato}
          <h3 class="tarjeta__titulo">{p.get('nombre', '')}</h3>
          <p class="predicador__procedencia">{procedencia}</p>
          {bio}
        </article>""")
    partes.append(seccion_congreso(
        'Predicadores invitados',
        '      <div class="rejilla rejilla--3 revelar">\n' + '\n'.join(tarjetas)
        + '\n      </div>' if tarjetas else '', eyebrow='Quiénes ministran',
        ident='predicadores'))

    # ---------- programa ----------
    jornadas = []
    for d in c.get('programa', []):
        rotulo = d.get('fecha', '')
        f_d = _fecha(rotulo)
        if f_d:
            rotulo = f'{DIAS[f_d.weekday()]} {f_d.day} de {MESES[f_d.month - 1]}'
        bloques = ''.join(
            f"""            <li>
              <span class="bloque__hora">{x.get('hora', '')}</span>
              <span class="bloque__actividad">{x.get('actividad', '')}</span>
              <span class="bloque__predicador">{x.get('predicador', '')}</span>
            </li>""" for x in d.get('bloques', []))
        lista = (f'\n          <ul class="bloques">\n{bloques}\n          </ul>'
                 if bloques else '')
        texto = f'\n          <p>{d["descripcion"]}</p>' if d.get('descripcion') else ''
        jornadas.append(f"""        <article class="jornada revelar">
          <p class="jornada__fecha">{rotulo}</p>
          <h3>{d.get('titulo', '')}</h3>{texto}{lista}
        </article>""")
    partes.append(seccion_congreso(
        'Programa', '      <div class="rejilla revelar">\n' + '\n'.join(jornadas)
        + '\n      </div>' if jornadas else '', eyebrow='Día por día',
        alterna=True, ident='programa'))

    # ---------- galería ----------
    imagenes = [foto(g['archivo'], g.get('alto', 900), g.get('alt', ''),
                     pie=g.get('pie', ''), ancho=g.get('ancho', 1600), base=b)
                for g in c.get('galeria', [])]
    partes.append(seccion_congreso(
        'Galería', '      <div class="galeria revelar">\n' + '\n'.join(imagenes)
        + '\n      </div>' if imagenes else '', eyebrow='Imágenes', ident='galeria'))

    # ---------- logística ----------
    ETIQUETAS = [('estacionamiento', 'Estacionamiento'),
                 ('hospedajes', 'Dónde alojarse'),
                 ('aeropuertos', 'Aeropuertos cercanos'),
                 ('transporte', 'Cómo llegar'),
                 ('ninos', 'Familias y niños')]
    log = c.get('logistica') or {}
    fichas = [f"""        <article class="tarjeta revelar">
          <span class="tarjeta__indice">{etiqueta}</span>
          <p>{log[clave]}</p>
        </article>""" for clave, etiqueta in ETIQUETAS if log.get(clave)]
    partes.append(seccion_congreso(
        'Antes de viajar', '      <div class="rejilla rejilla--3">\n'
        + '\n'.join(fichas) + '\n      </div>' if fichas else '',
        eyebrow='Logística', alterna=True, ident='logistica'))

    # ---------- preguntas frecuentes ----------
    preguntas = ''.join(f"""        <details class="pregunta revelar">
          <summary>{q.get('pregunta', '')}</summary>
          <p>{q.get('respuesta', '')}</p>
        </details>""" for q in c.get('faq', []))
    partes.append(seccion_congreso('Preguntas frecuentes', preguntas,
                                   eyebrow='Dudas', ident='faq'))

    # ---------- contacto ----------
    ct = c.get('contacto') or {}
    nombre_ct = ct.get('nombre') or CONTACTO['nombre']
    tel_ct = ct.get('telefono') or CONTACTO['telefono']
    wa_ct = ct.get('whatsapp') or CONTACTO['whatsapp']
    correo_ct = ct.get('correo') or CONTACTO['correo']
    solo_digitos = '+' + ''.join(x for x in tel_ct if x.isdigit())
    partes.append(f"""  <section class="seccion seccion--alterna" id="contacto-congreso">
    <div class="contenedor">
      <div class="seccion__encabezado revelar">
        <p class="seccion__eyebrow">Escríbenos</p>
        <h2>Contacto</h2>
        <div class="plomada"></div>
      </div>
      <div class="tarjeta revelar">
        <h3 class="tarjeta__titulo">{nombre_ct}</h3>
{dato('Teléfono', f'<a href="tel:{solo_digitos}">{tel_ct}</a>')}
{dato('WhatsApp', f'<a href="https://wa.me/{wa_ct}" target="_blank" rel="noopener">{tel_ct}</a>')}
{dato('Correo', f'<a href="mailto:{correo_ct}">{correo_ct}</a>')}
      </div>
      <p class="seccion__pie">
        <a class="boton boton--linea" href="{b}congresos/">Ver todos los congresos</a>
      </p>
    </div>
  </section>
""")

    # ---------- metadatos propios ----------
    resumen = (c.get('descripcion')
               or f'{c.get("edicion", "Congreso")} del Congreso La Sana Doctrina '
                  f'No Morirá en {lugar(c)}.')
    if c.get('fecha_inicio'):
        resumen = f'{resumen} {fechas_largas(c).capitalize()}. Entrada libre.'
    # Vista previa al compartir: el afiche si lo hay, si no la foto de la
    # edición, y solo como último recurso el logotipo genérico.
    ruta_img, _, alt_img = imagen_de(c)
    imagen = ruta_img or 'assets/img/logo.png'
    alt = alt_img or 'Escudo con espada y la cinta «La sana doctrina no morirá»'
    return {
        'archivo': f'congresos/{c["slug"]}/index.html',
        'titulo': titular or 'Congreso',
        'descripcion': resumen,
        'cuerpo': ''.join(partes),
        'imagen': imagen,
        'imagen_alt': alt,
        # Un congreso por anunciar no tiene nada que indexar todavía.
        'indexable': est != 'por_anunciar',
    }


def tarjeta_congreso(c, base=''):
    """Tarjeta del listado y de la portada."""
    return f"""        <a class="tarjeta tarjeta--enlace congreso-tarjeta"
           href="{base}congresos/{c['slug']}/">
          <span class="congreso-tarjeta__afiche">{afiche_img(c, base)}</span>
          <span class="congreso-tarjeta__texto">
            {insignia(c)}
            <span class="tarjeta__indice">{c.get('edicion', '')}</span>
            <h3 class="tarjeta__titulo">{lugar(c)}</h3>
            <p class="congreso-tarjeta__fechas">{fechas_cortas(c)}</p>
            <span class="congreso-tarjeta__mas">Ver detalles</span>
          </span>
        </a>"""


VACIO_PROXIMOS = """      <p class="vacio revelar">
        Estamos preparando la próxima edición. En cuanto se confirmen la sede
        y las fechas aparecerán aquí.
      </p>"""


def rejilla_congresos(lista, base=''):
    """Tarjetas de una lista de congresos, o el estado vacío si no hay
       ninguno con fecha confirmada. Una edición sin fecha no merece
       tarjeta: no habría nada que enseñar al entrar en ella."""
    con_fecha = [c for c in lista if c.get('fecha_inicio')]
    if not con_fecha:
        return VACIO_PROXIMOS
    return ('      <div class="rejilla rejilla--congresos revelar">\n'
            + '\n'.join(tarjeta_congreso(c, base) for c in con_fecha)
            + '\n      </div>')


def listado_congresos():
    """congresos/index.html — próximos arriba, pasados abajo."""
    b = '../'
    proximos = rejilla_congresos(PROXIMOS, b)
    pasados = rejilla_congresos(PASADOS, b) if PASADOS else ''
    return (cabecera('Una ciudad distinta cada vez', 'Congresos',
                     'El Congreso “La Sana Doctrina No Morirá” cambia de sede en '
                     'cada edición, para que la enseñanza alcance a más iglesias '
                     'y más pueblos.')
            + seccion_congreso('Próximos congresos', proximos,
                               eyebrow='Lo que viene', ident='proximos')
            + seccion_congreso('Ediciones anteriores', pasados,
                               eyebrow='Lo ya celebrado', alterna=True,
                               ident='anteriores'))


# ============================================================
#  INICIO
# ============================================================
INICIO = f"""  <section class="portada portada--inicio" id="inicio">
    <div class="contenedor">
      <!-- Logotipo oficial. Para cambiarlo basta con reemplazar los archivos
           assets/img/logo.webp y assets/img/logo.png. -->
      <picture class="portada__emblema">
        <source srcset="assets/img/logo.webp{V}" type="image/webp">
        <img src="assets/img/logo.png{V}" width="668" height="674" fetchpriority="high"
             alt="Emblema: escudo y espada con la cinta «La sana doctrina no morirá»">
      </picture>
      <p class="portada__antetitulo">La Sana Doctrina No Morirá</p>
      <h1>Un llamado a permanecer firmes en la verdad</h1>
      <p class="portada__cita">
        “Retén la forma de las sanas palabras que de mí oíste…”
        <cite>2 Timoteo 1:13 · RVR1960</cite>
      </p>

{aviso_portada()}

      <div class="botones">
        <a class="boton boton--principal" href="remanente.html">¿Eres parte del remanente?</a>
        <a class="boton boton--fantasma" href="que-es.html">Conoce el proyecto</a>
      </div>
    </div>
  </section>

""" + bloque_proximos() + f"""
  <section class="seccion seccion--centrada">
    <div class="contenedor contenedor--angosto">
      <div class="revelar">
        <p class="seccion__eyebrow">El proyecto</p>
        <h2>Un frente común por la verdad bíblica</h2>
        <div class="plomada"></div>
        <p class="texto-guia">
          <strong>“La Sana Doctrina No Morirá”</strong> es un proyecto nacido en el
          corazón de Dios para este tiempo final. Es una visión que une a las
          <strong>iglesias conservadoras</strong> comprometidas con la verdad bíblica,
          en un frente común contra la creciente <strong>apostasía</strong>, la
          <strong>herejía</strong>, y las <strong>mentiras disfrazadas de evangelio</strong>.
        </p>
        <p class="seccion__pie">
          <a class="boton boton--linea" href="que-es.html">Seguir leyendo</a>
        </p>
      </div>
    </div>
  </section>

  <section class="seccion seccion--alterna seccion--centrada">
    <div class="contenedor">
      <div class="seccion__encabezado revelar">
        <p class="seccion__eyebrow">Recorrido</p>
        <h2>Explora el movimiento</h2>
        <div class="plomada"></div>
      </div>

      <div class="rejilla rejilla--3 revelar">
{tarjeta_enlace('que-es.html', 'Fundamento', '¿Qué es «La Sana Doctrina No Morirá»?',
                'Un clamor espiritual para volver al fundamento de Cristo y su doctrina pura.')}
{tarjeta_enlace('apostasia.html', 'El tiempo que vivimos', 'Enfrentando la apostasía',
                'Mensajes que entretienen pero no santifican, promesas sin cruz, éxito sin obediencia.')}
{tarjeta_enlace('mision.html', 'Compromisos', 'Nuestra misión',
                'Unir, confrontar, denunciar y afirmar la verdad de las Escrituras.')}
{tarjeta_enlace('iglesias.html', 'El distintivo', 'Iglesias que viven la sana doctrina',
                'Viven en santidad, predican la Palabra sin alterarla y disciernen los tiempos.')}
{tarjeta_enlace('pastores.html', 'Testimonios', 'Pastores defensores',
                'Siervos que se levantaron como firmes defensores de la sana doctrina.')}
{tarjeta_enlace('congresos/', 'Las sedes', 'Los congresos',
                'Varias ediciones al año, cada una en una ciudad distinta, para que la '
                'enseñanza alcance más pueblos.')}
      </div>
    </div>
  </section>

{FRANJA}
  <section class="seccion seccion--centrada">
    <div class="contenedor contenedor--angosto">
      <div class="revelar">
        <h2>¿Eres parte del remanente?</h2>
        <div class="plomada"></div>
        <p class="texto-guia">
          Si tu iglesia defiende la sana doctrina, vive conforme a la Palabra y
          <strong>no transige con el error</strong>, te invitamos a
          <strong>unirte a este proyecto de unidad y restauración</strong>.
        </p>
        <div class="botones seccion__pie">
          <a class="boton boton--principal" href="contacto.html">Quiero unirme</a>
          <a class="boton boton--linea" href="remanente.html">Leer el llamado</a>
        </div>
      </div>
    </div>
  </section>
"""

# ============================================================
#  ¿QUÉ ES?
# ============================================================
QUE_ES = cabecera(
    'El proyecto', '¿Qué es “La Sana Doctrina No Morirá”?',
    'No es una organización, sino un clamor espiritual.'
) + """
  <section class="seccion seccion--centrada" id="que-es">
    <div class="contenedor contenedor--angosto">
      <div class="revelar">
        <p class="texto-guia">
          <strong>“La Sana Doctrina No Morirá”</strong> es un proyecto nacido en el
          corazón de Dios para este tiempo final. Es una visión que une a las
          <strong>iglesias conservadoras</strong> comprometidas con la verdad bíblica,
          en un frente común contra la creciente <strong>apostasía</strong>, la
          <strong>herejía</strong>, y las <strong>mentiras disfrazadas de evangelio</strong>.
        </p>

        <p class="texto-guia">
          En un mundo donde la verdad está siendo diluida con levadura doctrinal,
          este movimiento levanta bandera de <strong>fidelidad a la Palabra</strong>.
          No es una organización, sino un clamor espiritual:
          <strong>¡volver al fundamento de Cristo y su doctrina pura!</strong>
        </p>
      </div>
    </div>
  </section>

  <section class="seccion seccion--alterna seccion--centrada" id="movimiento">
    <div class="contenedor contenedor--angosto">
      <div class="revelar">
        <p class="seccion__eyebrow">El remanente</p>
        <h2>Un movimiento de Dios</h2>
        <div class="plomada"></div>

        <div class="lemas">
          <p class="lema">No es un nombre, es un <span>propósito</span>.</p>
          <p class="lema">No es un grupo más, es un <span>remanente fiel</span>.</p>
        </div>

        <p class="texto-guia">
          Dios está levantando una generación que no se arrodilla ante Baal, que no
          vende su mensaje por fama o ganancias, que anhela la pureza del Evangelio
          y no se avergüenza de proclamar la verdad, aunque sea impopular.
        </p>

        <div class="botones seccion__pie">
          <a class="boton boton--principal" href="mision.html">Ver nuestra misión</a>
          <a class="boton boton--linea" href="apostasia.html">Enfrentando la apostasía</a>
        </div>
      </div>
    </div>
  </section>
"""

# ============================================================
#  APOSTASÍA
# ============================================================
APOSTASIA = cabecera(
    'El tiempo que vivimos', 'Enfrentando la apostasía',
    'Vivimos tiempos que el apóstol Pablo anunció con claridad.'
) + """
  <section class="seccion" id="apostasia">
    <div class="contenedor">
      <div class="duo revelar">
        <div class="medida">
          <p><strong>Vivimos tiempos profetizados por el apóstol Pablo:</strong></p>
          <blockquote class="cita">
            “Porque vendrá tiempo cuando no sufrirán la sana doctrina…”
            <cite>2 Timoteo 4:3 · RVR1960</cite>
          </blockquote>
          <p>
            Hoy muchos buscan mensajes que entretienen pero no santifican, promesas
            sin cruz, éxito sin obediencia. Frente a esta realidad,
            <strong>“La Sana Doctrina No Morirá”</strong> es un
            <strong>grito de alerta</strong>, una <strong>convocatoria a la fidelidad</strong>.
          </p>
          <p class="seccion__pie">
            <a class="boton boton--linea" href="mision.html">Nuestra respuesta: la misión</a>
          </p>
        </div>

        <div>
          <div class="tarjeta">
            <span class="tarjeta__indice">Lo que se predica hoy</span>
            <h3 class="tarjeta__titulo">Mensajes que entretienen pero no santifican</h3>
            <p>Promesas sin cruz. Éxito sin obediencia. Emoción sin transformación.</p>
          </div>
          <div class="tarjeta tarjeta--seguida">
            <span class="tarjeta__indice">Nuestra respuesta</span>
            <h3 class="tarjeta__titulo">Un grito de alerta y una convocatoria a la fidelidad</h3>
            <p>Volver al fundamento de Cristo y a su doctrina pura, sin negociarla.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

""" + FRANJA

# ============================================================
#  MISIÓN
# ============================================================
MISION = cabecera(
    'Nuestra misión', 'Cuatro compromisos que nos definen',
    'Lo que este movimiento se propone hacer, y por qué.'
) + """
  <section class="seccion seccion--centrada" id="mision">
    <div class="contenedor">
      <div class="rejilla rejilla--2 revelar">
        <article class="tarjeta">
          <span class="tarjeta__indice">Compromiso I</span>
          <h3 class="tarjeta__titulo">Unir a las iglesias de sana doctrina</h3>
          <p>Bajo un mismo sentir: defender la verdad y rechazar la falsedad.</p>
        </article>

        <article class="tarjeta">
          <span class="tarjeta__indice">Compromiso II</span>
          <h3 class="tarjeta__titulo">Confrontar las falsas enseñanzas</h3>
          <p>
            Profetas mentirosos y predicadores corruptos que distorsionan el
            Evangelio por ganancia deshonesta.
          </p>
        </article>

        <article class="tarjeta">
          <span class="tarjeta__indice">Compromiso III</span>
          <h3 class="tarjeta__titulo">Denunciar la levadura doctrinal</h3>
          <p>
            La que contamina el mensaje puro de Cristo: prosperidad sin
            arrepentimiento, emociones sin transformación, religiosidad sin santidad.
          </p>
        </article>

        <article class="tarjeta">
          <span class="tarjeta__indice">Compromiso IV</span>
          <h3 class="tarjeta__titulo">Afirmar la verdad de las Escrituras</h3>
          <p>Como norma suprema de fe y conducta.</p>
        </article>
      </div>

      <div class="botones seccion__pie">
        <a class="boton boton--principal" href="iglesias.html">Iglesias que lo viven</a>
        <a class="boton boton--linea" href="contacto.html">Sumar mi iglesia</a>
      </div>
    </div>
  </section>
"""

# ============================================================
#  IGLESIAS
# ============================================================
IGLESIAS = cabecera(
    'El distintivo', 'Iglesias que viven la sana doctrina',
    'Las iglesias que se identifican con este llamado.'
) + """
  <section class="seccion seccion--centrada" id="iglesias">
    <div class="contenedor contenedor--angosto">
      <ul class="lista-marcada revelar">
        <li><strong>Viven en santidad</strong>: no por tradición, sino por convicción.</li>
        <li><strong>Predican la Palabra sin alterarla</strong>: sin añadir ni quitar.</li>
        <li><strong>Disciernen los tiempos</strong>: no se dejan seducir por modas espirituales ni espectáculos religiosos.</li>
        <li><strong>Examinan todo a la luz de la Biblia</strong> y no por popularidad o apariencias.</li>
      </ul>

      <div class="botones seccion__pie">
        <a class="boton boton--principal" href="remanente.html">¿Eres parte del remanente?</a>
        <a class="boton boton--linea" href="contacto.html">Sumar mi iglesia</a>
      </div>
    </div>
  </section>

""" + FRANJA

# ============================================================
#  REMANENTE
# ============================================================
REMANENTE = cabecera(
    'El llamado', '¿Eres parte del remanente?',
    'La batalla por la verdad sigue vigente.'
) + """
  <section class="seccion seccion--centrada" id="remanente">
    <div class="contenedor contenedor--angosto">
      <div class="revelar">
        <p class="texto-guia">
          Si tu iglesia defiende la sana doctrina, vive conforme a la Palabra y
          <strong>no transige con el error</strong>, te invitamos a
          <strong>unirte a este proyecto de unidad y restauración</strong>.
          La batalla por la verdad sigue vigente, y
          <strong>la sana doctrina no morirá</strong> porque ha sido plantada por
          Dios mismo.
        </p>
        <div class="botones seccion__pie">
          <a class="boton boton--principal" href="contacto.html">Quiero unirme</a>
          <a class="boton boton--linea" href="#suscribete">Recibir información</a>
        </div>
      </div>
    </div>
  </section>

  <section class="seccion seccion--alterna seccion--centrada" id="suscribete">
    <div class="contenedor contenedor--angosto">
      <div class="seccion__encabezado revelar">
        <p class="seccion__eyebrow">Mantente conectado</p>
        <h2>Quiero unirme al remanente</h2>
        <div class="plomada"></div>
        <p>Si tu iglesia defiende la sana doctrina y no transige con el error,
           escríbenos y conversamos.</p>
      </div>

""" + formulario('Unirse al remanente', '\n'.join([
    '          <div class="dosxdos">',
    campo('r-iglesia', 'iglesia', 'Nombre de la iglesia', requerido=True,
          auto='organization'),
    campo('r-pastor', 'pastor', 'Pastor', requerido=True, auto='name'),
    '          </div>',
    '          <div class="dosxdos">',
    campo('r-ciudad', 'ciudad', 'Ciudad', requerido=True),
    campo('r-estado', 'estado', 'Estado o provincia'),
    '          </div>',
    '          <div class="dosxdos">',
    campo('r-pais', 'pais', 'País', requerido=True, auto='country-name'),
    campo('r-telefono', 'telefono', 'Teléfono', tipo='tel', auto='tel'),
    '          </div>',
    campo('r-correo', 'correo', 'Correo electrónico', tipo='email',
          requerido=True, auto='email'),
    campo('r-mensaje', 'mensaje', 'Mensaje', area=True, requerido=True),
]), 'Unirme al remanente', clase='revelar') + """
    </div>
  </section>
"""

# ============================================================
#  PASTORES
# ============================================================
VIDEOS = [('Testimonio 1', '01:35'), ('Testimonio 2', '01:06'), ('Testimonio 3', '01:33'),
          ('Testimonio 4', '01:45'), ('Testimonio 5', '01:17')]

tarjetas_video = '\n'.join(f"""        <figure class="video">
          <div class="video__marco">
            <picture>
              <source srcset="assets/img/poster-video.webp{V}" type="image/webp">
              <img class="video__poster" src="assets/img/poster-video.jpg{V}" alt=""
                   width="800" height="450" loading="lazy" decoding="async">
            </picture>
            <span class="video__play" aria-hidden="true"></span>
          </div>
          <figcaption class="video__pie"><strong>{t}</strong><span>{d}</span></figcaption>
        </figure>""" for t, d in VIDEOS)

PREDICACION = f"""  <section class="seccion seccion--alterna seccion--centrada" id="predicacion">
    <div class="contenedor">
      <div class="seccion__encabezado revelar">
        <p class="seccion__eyebrow">Galería</p>
        <h2>Momentos de predicación</h2>
        <div class="plomada"></div>
      </div>

      <h3 class="programa__titulo revelar">Connecticut · 22, 23 y 24 de mayo de 2026</h3>

      <div class="galeria revelar">
{foto("predicacion-1", 966, "Predicador con micrófono y la mano levantada durante el mensaje", ancho=1089)}
{foto("predicacion-2", 1200, "Predicador en el púlpito con los pastores sentados detrás")}
{foto("predicacion-3", 900, "Ministración desde el púlpito durante el congreso")}
{foto("predicacion-4", 900, "Predicación en el púlpito, con la pantalla del auditorio al fondo")}
{foto("predicacion-5", 900, "Dos ministros en el púlpito durante la predicación")}
{foto("predicacion-6", 900, "Momento de oración con las manos levantadas en el púlpito")}
{foto("predicacion-7", 900, "Predicador dirigiéndose a la congregación desde la plataforma")}
{foto("predicacion-8", 900, "Vista general del auditorio durante una de las sesiones")}
      </div>
    </div>
  </section>
"""

PASTORES_GALERIA = f"""      <div class="galeria galeria--natural revelar">
{foto("pastor-retrato-1", 1400, "Retrato de un pastor con su Biblia", ancho=1231, prioridad=True)}
{foto("pastor-retrato-2", 1400, "Retrato de un pastor con su Biblia", ancho=1050)}
{foto("pastor-predicando-1", 1400, "Pastor predicando desde el púlpito", ancho=1050)}
{foto("pastor-predicando-2", 1400, "Ministra predicando desde el púlpito", ancho=1050)}
{foto("pastor-predicando-3", 1050, "Ministra leyendo la Palabra desde el púlpito", ancho=1400)}
{foto("pastor-predicando-4", 1050, "Ministra predicando con los pastores de pie detrás", ancho=1400)}
{foto("pastor-predicando-5", 788, "Predicador dirigiéndose a la congregación", ancho=1400)}
      </div>
"""

PASTORES = cabecera(
    'Testimonios del congreso', 'Pastores defensores de la sana doctrina',
    'Siervos de Dios que se levantaron como firmes defensores de la verdad.'
) + f"""
  <section class="seccion seccion--centrada" id="pastores">
    <div class="contenedor">
      <div class="seccion__encabezado revelar">
        <p>
          En cada edición del Congreso “La Sana Doctrina No Morirá” hemos sido
          honrados con la participación de pastores comprometidos con la verdad
          inmutable del Evangelio. Estos siervos de Dios no solo asistieron, sino que
          se levantaron como firmes defensores de la sana doctrina en medio de un
          tiempo donde muchos se desvían del consejo bíblico.
        </p>
      </div>

""" + PASTORES_GALERIA + f"""

      <!--
        FASE DE DISEÑO — Los marcos muestran un póster provisional
        (assets/img/poster-video.jpg) para que no salgan negros. Cuando estén
        los videos reales, sustituye el <div class="video__marco"> por:

          <video class="video__medio" controls preload="metadata"
                 poster="assets/img/poster-video.jpg">
            <source src="assets/video/pastor-1.mp4" type="video/mp4">
          </video>

        o, si van en YouTube:

          <div class="video__marco">
            <iframe class="video__medio" src="https://www.youtube.com/embed/ID"
                    title="Testimonio" allowfullscreen loading="lazy"></iframe>
          </div>
      -->
      <div class="rejilla rejilla--3 revelar">
{tarjetas_video}
      </div>

      <div class="botones seccion__pie">
        <a class="boton boton--linea" href="congresos/">Ver los congresos</a>
      </div>
    </div>
  </section>
""" + PREDICACION

# ============================================================
#  CONTACTO
# ============================================================
CUERPO_CONTACTO = cabecera(
    'Escríbenos', 'Contacto',
    'Si tu iglesia quiere sumarse al movimiento, proponer una sede para el '
    'próximo congreso o hacer una consulta, este es el camino.'
) + """
  <section class="seccion" id="contacto">
    <div class="contenedor">
      <div class="duo revelar">
        <!-- FASE DE DISEÑO: el envío se conecta más adelante -->
""" + formulario('Contacto', '\n'.join([
    '          <div class="dosxdos">',
    campo('c-nombre', 'nombre', 'Nombre completo', requerido=True, auto='name'),
    campo('c-iglesia', 'iglesia', 'Iglesia o ministerio', auto='organization'),
    '          </div>',
    '          <div class="dosxdos">',
    campo('c-correo', 'correo', 'Correo electrónico', tipo='email',
          requerido=True, auto='email'),
    campo('c-ciudad', 'ciudad', 'Ciudad y país'),
    '          </div>',
    campo('c-motivo', 'motivo', 'Motivo', opciones=[
        'Mi iglesia quiere unirse al movimiento',
        'Proponer una sede para el próximo congreso',
        'Información sobre el congreso',
        'Invitación a predicar o enseñar',
        'Pregunta bíblica o doctrinal',
        'Petición de oración',
        'Otro']),
    campo('c-mensaje', 'mensaje', 'Mensaje', area=True, requerido=True),
]), 'Enviar mensaje') + """

""" + f"""
        <div>
          <!-- Los datos salen del bloque CONTACTO de este archivo -->
          <div class="tarjeta">
            <span class="tarjeta__indice">Contacto directo</span>
            <h3 class="tarjeta__titulo">{CONTACTO['nombre']}</h3>
{dato('Teléfono', f"<a href='tel:{tel_enlace()}'>{CONTACTO['telefono']} ({CONTACTO['pais_tel']})</a>")}
{dato('WhatsApp', f"<a href='https://wa.me/{CONTACTO['whatsapp']}' target='_blank' rel='noopener'>{CONTACTO['telefono']}</a>")}
{dato('Correo', f"<a href='mailto:{CONTACTO['correo']}'>{CONTACTO['correo']}</a>")}
          </div>
          </div>

          <div class="tarjeta tarjeta--seguida">
            <span class="tarjeta__indice">Sedes</span>
            <h3 class="tarjeta__titulo">Lleva el congreso a tu ciudad</h3>
            <p>
              El congreso se celebra cada año en un lugar distinto. Si tu iglesia
              desea recibirlo, escríbenos y conversamos sobre los requisitos y las
              fechas disponibles.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# ============================================================
#  404
# ============================================================
NO_ENCONTRADA = cabecera(
    'Error 404', 'No encontramos esa página',
    'Puede que el enlace haya cambiado o que la dirección esté mal escrita.'
) + """
  <section class="seccion seccion--centrada">
    <div class="contenedor contenedor--angosto">
      <div class="revelar">
        <p class="texto-guia">
          Desde aquí puedes volver al inicio o ir directamente a cualquier sección
          del sitio.
        </p>
        <div class="botones seccion__pie">
          <a class="boton boton--principal" href="index.html">Volver al inicio</a>
          <a class="boton boton--linea" href="contacto.html">Contacto</a>
        </div>
      </div>
    </div>
  </section>
"""



PAGINAS = [
    ('index.html', 'Inicio',
     'Un llamado a permanecer firmes en la verdad: proyecto que une a las iglesias '
     'conservadoras comprometidas con la verdad bíblica frente a la apostasía.', INICIO, True),
    ('que-es.html', '¿Qué es “La Sana Doctrina No Morirá”?',
     'Qué es «La Sana Doctrina No Morirá»: un clamor espiritual para volver al '
     'fundamento de Cristo y su doctrina pura.', QUE_ES, True),
    ('apostasia.html', 'Enfrentando la apostasía',
     'Enfrentando la apostasía: vivimos tiempos que el apóstol Pablo anunció con '
     'claridad en 2 Timoteo 4:3.', APOSTASIA, True),
    ('mision.html', 'Cuatro compromisos que nos definen',
     'Cuatro compromisos que nos definen: unir a las iglesias de sana doctrina, '
     'confrontar las falsas enseñanzas, denunciar la levadura doctrinal y afirmar '
     'la verdad de las Escrituras.', MISION, True),
    ('iglesias.html', 'Iglesias que viven la sana doctrina',
     'Iglesias que viven la sana doctrina: viven en santidad, predican la Palabra '
     'sin alterarla, disciernen los tiempos y examinan todo a la luz de la Biblia.',
     IGLESIAS, True),
    ('remanente.html', '¿Eres parte del remanente?',
     '¿Eres parte del remanente? Si tu iglesia defiende la sana doctrina y no '
     'transige con el error, únete a este proyecto de unidad y restauración.',
     REMANENTE, True),
    ('pastores.html', 'Pastores defensores de la sana doctrina',
     'Pastores defensores de la sana doctrina: siervos de Dios que se levantaron '
     'como firmes defensores de la verdad inmutable del Evangelio.', PASTORES, True),
    ('congresos/index.html', 'Congresos',
     'Todas las ediciones del Congreso «La Sana Doctrina No Morirá»: las que '
     'vienen y las ya celebradas. Entrada libre.', listado_congresos(), True),
    ('contacto.html', 'Contacto',
     'Contacto: escríbenos para sumar tu iglesia al movimiento, proponer una sede '
     'para el próximo congreso o hacer una consulta.', CUERPO_CONTACTO, True),
    ('404.html', 'No encontramos esa página',
     'No encontramos esa página. Vuelve al inicio o ve directamente a cualquier '
     'sección del sitio.', NO_ENCONTRADA, False),
]

def escribir(archivo, texto):
    destino = os.path.join(RAIZ, archivo)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(texto)
    print('escrito:', archivo)


# Solo la portada lleva los datos incrustados: es la única con cuenta
# regresiva, y por tanto la única que necesita saber cuál es la edición más
# cercana en el momento de abrirse. El resto de páginas ya trae escrito
# todo lo que muestra.
CON_DATOS = {'index.html'}

for archivo, titulo, descripcion, cuerpo, indexable in PAGINAS:
    extra = datos_js() if archivo in CON_DATOS else ''
    escribir(archivo, pagina(archivo, titulo, descripcion, cuerpo, indexable,
                             extra=extra))

# ---------------- fichas de cada congreso ----------------
# Una edición sin fecha confirmada no tiene página propia: nada enlazaría a
# ella y no habría nada que leer dentro. Aparece como estado vacío en el
# listado hasta que se le pongan fechas.
for c in [x for x in CONGRESOS if x.get('fecha_inicio')]:
    d = ficha(c)
    escribir(d['archivo'],
             pagina(d['archivo'], d['titulo'], d['descripcion'], d['cuerpo'],
                    d['indexable'], imagen=d['imagen'], imagen_alt=d['imagen_alt']))

# ---------------- congreso.html: redirección ----------------
# La página vieja se compartió por WhatsApp y está en enlaces ajenos, así
# que no puede desaparecer: reenvía al listado. rel="canonical" le dice al
# buscador cuál es la dirección buena y noindex evita que compitan entre sí.
escribir('congreso.html', f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Congresos — La Sana Doctrina No Morirá</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{SITIO}congresos/">
<meta http-equiv="refresh" content="0; url=congresos/">
<link rel="stylesheet" href="assets/css/estilo.css{V}">
<link rel="icon" href="assets/img/favicon.png{V}" type="image/png">
</head>
<body>
<main id="contenido">
  <section class="portada portada--interior">
    <div class="contenedor">
      <h1>Esta página se mudó</h1>
      <p class="portada__entrada">
        Los congresos están ahora en <a href="congresos/">congresos</a>.
      </p>
    </div>
  </section>
</main>
</body>
</html>
""")

# ---------------- sitemap y robots ----------------
# El sitemap es el único archivo, junto con las etiquetas canonical y og:,
# donde el estándar exige la URL completa. Sale de la constante SITIO.
rutas = [(a, '1.0' if a == 'index.html' else '0.8') for a, _ in TODAS]
rutas += [(f'congresos/{c["slug"]}/', '0.7') for c in CONGRESOS
          if estado_de(c) != 'por_anunciar']
urls = '\n'.join(
    f'  <url>\n    <loc>{SITIO}{"" if a == "index.html" else a}</loc>\n'
    f'    <lastmod>{ACTUALIZADO}</lastmod>\n'
    f'    <priority>{prioridad}</priority>\n  </url>'
    for a, prioridad in rutas)

with open(os.path.join(RAIZ, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")

with open(os.path.join(RAIZ, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(f"""User-agent: *
Allow: /
Disallow: /404.html

Sitemap: {SITIO}sitemap.xml
""")
print('escritos: sitemap.xml, robots.txt')

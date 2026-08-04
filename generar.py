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


def tarjeta_enlace(href, indice, titulo, texto):
    return f"""        <a class="tarjeta tarjeta--enlace" href="{href}">
          <span class="tarjeta__indice">{indice}</span>
          <h3 class="tarjeta__titulo">{titulo}</h3>
          <p>{texto}</p>
        </a>"""


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

      <a class="aviso" href="congreso.html" data-aviso>
        <span class="aviso__marca" data-aviso-marca>Congreso anual</span>
        <span class="aviso__texto" data-aviso-texto>Próxima sede y fecha por anunciar</span>
        <span class="aviso__flecha" aria-hidden="true">→</span>
      </a>

      <div class="botones">
        <a class="boton boton--principal" href="remanente.html">¿Eres parte del remanente?</a>
        <a class="boton boton--fantasma" href="que-es.html">Conoce el proyecto</a>
      </div>
    </div>
  </section>

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
{tarjeta_enlace('congreso.html', 'Cada año', 'El congreso',
                'Una vez al año, en una ciudad distinta, para que la enseñanza alcance más pueblos.')}
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
        <h2>Suscríbete para más información</h2>
        <div class="plomada"></div>
        <p>Recibe las fechas del congreso y los anuncios del movimiento.</p>
      </div>

      <!-- FASE DE DISEÑO: el envío se conecta más adelante -->
      <form class="formulario revelar" data-formulario-contacto
            data-destino="ig07644@gmail.com" data-asunto="Suscripción">
        <div class="dosxdos">
          <div class="campo">
            <label for="nombre">Nombre</label>
            <input id="nombre" name="nombre" type="text" required autocomplete="given-name">
          </div>
          <div class="campo">
            <label for="apellido">Apellido</label>
            <input id="apellido" name="apellido" type="text" autocomplete="family-name">
          </div>
        </div>

        <div class="campo">
          <label for="correo">Correo electrónico</label>
          <input id="correo" name="correo" type="email" required autocomplete="email">
        </div>

        <div>
          <button class="boton boton--principal" type="submit">Suscribirme</button>
        </div>
        <p class="ayuda">Al enviar se abrirá tu programa de correo con los datos ya escritos.</p>
      </form>
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
        <a class="boton boton--linea" href="congreso.html">Ver el próximo congreso</a>
      </div>
    </div>
  </section>
""" + PREDICACION

# ============================================================
#  CONGRESO
# ============================================================
GALERIA = f"""  <section class="seccion seccion--alterna seccion--centrada" id="galeria">
    <div class="contenedor">
      <div class="seccion__encabezado revelar">
        <p class="seccion__eyebrow">Galería</p>
        <h2>Imágenes del congreso</h2>
        <div class="plomada"></div>
      </div>

      <h3 class="programa__titulo revelar">Newark, Nueva Jersey · 23, 24 y 25 de mayo de 2025</h3>

      <!-- PENDIENTE: faltan las fotos de Cartagena, Colombia (17, 18 y 19 de
           julio de 2026). Cuando lleguen se añade debajo otro bloque igual:
           un <h3 class="programa__titulo revelar"> con el rótulo de la
           edición y su propio <div class="galeria revelar">.
           Las fotos de Connecticut (22, 23 y 24 de mayo de 2026) están en
           la galería de pastores.html. -->
      <div class="galeria revelar">
{foto("pastores-grupo", 900,
      "Grupo de pastores con sus Biblias frente al emblema de La Sana Doctrina No Morirá",
      pie="Los pastores")}
{foto("congreso-cartel", 900,
      "Presentación del cartel de bienvenida al congreso",
      pie="Bienvenida al congreso")}
{foto("congreso-oracion", 1200,
      "Momento de oración junto al cartel de bienvenida al congreso",
      pie="Oración de apertura")}
{foto("congreso-asamblea", 900,
      "Asistentes al congreso reunidos frente al emblema de La Sana Doctrina No Morirá",
      pie="Los asistentes")}
{foto("congreso-grupo-1", 900,
      "Grupo de asistentes al congreso frente al emblema",
      pie="Hermanas participantes")}
{foto("congreso-grupo-2", 900,
      "Tres asistentes al congreso frente al emblema",
      pie="Participantes del congreso")}
      </div>
    </div>
  </section>
"""

CONGRESO = cabecera(
    'Cada año, en una ciudad distinta', 'El congreso',
    'El Congreso “La Sana Doctrina No Morirá” se celebra una vez al año y cada '
    'edición se realiza en un lugar diferente, para que la enseñanza alcance a '
    'más iglesias y más pueblos.'
) + """
  <section class="seccion seccion--centrada" id="congreso">
    <div class="contenedor">
      <div class="seccion__encabezado revelar">
        <p class="seccion__eyebrow">Próxima cita</p>
        <h2>Próximo congreso</h2>
        <div class="plomada"></div>
      </div>

      <!-- La sede y las fechas se editan en assets/js/main.js, en el bloque
           CONGRESO que está al principio del archivo. -->
      <article class="proximo revelar" data-proximo>
        <p class="proximo__edicion" data-proximo-edicion>Próxima edición</p>
        <h3 class="proximo__sede" data-proximo-sede>Sede por anunciar</h3>
        <p class="proximo__fechas" data-proximo-fechas>Fechas por anunciar</p>

        <!-- La cuenta se oculta a los lectores de pantalla: anunciar los
             segundos sería insoportable. El resumen de abajo la sustituye. -->
        <div class="cuenta" aria-hidden="true" hidden>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-dias>—</span><span class="cuenta__rotulo">Días</span></div>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-horas>—</span><span class="cuenta__rotulo">Horas</span></div>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-minutos>—</span><span class="cuenta__rotulo">Minutos</span></div>
          <div class="cuenta__caja"><span class="cuenta__cifra" data-segundos>—</span><span class="cuenta__rotulo">Segundos</span></div>
        </div>
        <p class="cuenta__aviso" data-cuenta-mensaje hidden></p>
        <p class="visualmente-oculto" aria-live="polite" data-cuenta-resumen></p>

        <div class="botones seccion__pie">
          <a class="boton boton--principal" href="contacto.html">Quiero asistir</a>
          <a class="boton boton--fantasma" href="remanente.html#suscribete">Avísenme la fecha</a>
        </div>
      </article>

      <!-- Programa de las ediciones ya celebradas. El contenido lo genera
           main.js a partir del array EDICIONES; no se escribe aquí para no
           tener los mismos datos en dos sitios. -->
      <div data-ediciones></div>
      <!-- Para publicar otra edición pasada basta con añadir un objeto más
           al array EDICIONES de assets/js/main.js. -->
    </div>
  </section>

""" + GALERIA

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
        <form class="formulario" data-formulario-contacto
              data-destino="ig07644@gmail.com" data-asunto="Contacto">
          <div class="dosxdos">
            <div class="campo">
              <label for="c-nombre">Nombre completo</label>
              <input id="c-nombre" name="nombre" type="text" required autocomplete="name">
            </div>
            <div class="campo">
              <label for="c-iglesia">Iglesia o ministerio</label>
              <input id="c-iglesia" name="iglesia" type="text" autocomplete="organization">
            </div>
          </div>

          <div class="dosxdos">
            <div class="campo">
              <label for="c-correo">Correo electrónico</label>
              <input id="c-correo" name="correo" type="email" required autocomplete="email">
            </div>
            <div class="campo">
              <label for="c-ciudad">Ciudad y país</label>
              <input id="c-ciudad" name="ciudad" type="text">
            </div>
          </div>

          <div class="campo">
            <label for="c-motivo">Motivo</label>
            <select id="c-motivo" name="motivo">
              <option>Mi iglesia quiere unirse al movimiento</option>
              <option>Proponer una sede para el próximo congreso</option>
              <option>Información sobre el congreso</option>
              <option>Invitación a predicar o enseñar</option>
              <option>Pregunta bíblica o doctrinal</option>
              <option>Petición de oración</option>
              <option>Otro</option>
            </select>
          </div>

          <div class="campo">
            <label for="c-mensaje">Mensaje</label>
            <textarea id="c-mensaje" name="mensaje" required></textarea>
          </div>

          <div>
            <button class="boton boton--principal" type="submit">Enviar mensaje</button>
          </div>
          <p class="ayuda">Al enviar se abrirá tu programa de correo con el mensaje ya redactado.</p>
        </form>

        <div>
          <!-- FASE DE DISEÑO: datos provisionales -->
          <div class="tarjeta">
            <span class="tarjeta__indice">Contacto directo</span>
            <h3 class="tarjeta__titulo">Pastor Junior Castillo</h3>
            <div class="dato">
              <p class="dato__etiqueta">Teléfono</p>
              <p class="dato__valor"><a href="tel:+18622416144">+1 862 241-6144 (EE.UU.)</a></p>
            </div>
            <div class="dato">
              <p class="dato__etiqueta">WhatsApp</p>
              <p class="dato__valor">
                <a href="https://wa.me/18622416144"
                   target="_blank" rel="noopener">+1 862 241-6144</a>
              </p>
            </div>
            <div class="dato">
              <p class="dato__etiqueta">Correo</p>
              <p class="dato__valor"><a href="mailto:ig07644@gmail.com">ig07644@gmail.com</a></p>
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
    ('congreso.html', 'El congreso',
     'El congreso «La Sana Doctrina No Morirá» se celebra una vez al año y cada '
     'edición se realiza en una ciudad diferente.', CONGRESO, True),
    ('contacto.html', 'Contacto',
     'Contacto: escríbenos para sumar tu iglesia al movimiento, proponer una sede '
     'para el próximo congreso o hacer una consulta.', CUERPO_CONTACTO, True),
    ('404.html', 'No encontramos esa página',
     'No encontramos esa página. Vuelve al inicio o ve directamente a cualquier '
     'sección del sitio.', NO_ENCONTRADA, False),
]

for archivo, titulo, descripcion, cuerpo, indexable in PAGINAS:
    with open(os.path.join(RAIZ, archivo), 'w', encoding='utf-8') as f:
        f.write(pagina(archivo, titulo, descripcion, cuerpo, indexable))
    print('escrito:', archivo)

# ---------------- sitemap y robots ----------------
hoy = '2026-08-01'
urls = '\n'.join(
    f'  <url>\n    <loc>{SITIO}{"" if a == "index.html" else a}</loc>\n'
    f'    <lastmod>{hoy}</lastmod>\n'
    f'    <priority>{"1.0" if a == "index.html" else "0.8"}</priority>\n  </url>'
    for a, _ in TODAS)

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

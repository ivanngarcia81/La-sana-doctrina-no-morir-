/* ============================================================
   La Sana Doctrina No Morirá — comportamiento del sitio
   Sin librerías externas.
   ============================================================ */
(function () {
  'use strict';

  /* ============================================================
     PRÓXIMO CONGRESO — ESTE ES EL ÚNICO BLOQUE QUE HAY QUE
     ACTUALIZAR CADA AÑO. Se usa en la página del congreso y en
     el aviso de la portada.

       edicion  Nombre de la edición, p. ej. 'Edición 2027'
       sede     Ciudad y país,        p. ej. 'Ciudad de Panamá, Panamá'
       fechas   Texto de las fechas,  p. ej. '16, 17 y 18 de julio de 2027'
       inicio   Inicio en formato ISO con zona horaria,
                p. ej. '2027-07-16T09:00:00-05:00'
       fin      Cierre en el mismo formato

     Si se dejan vacíos, la página muestra sola el aviso
     "sede y fecha por anunciar".
     ============================================================ */
  var CONGRESO = {
    edicion: '',
    sede: '',
    fechas: '',
    inicio: '',
    fin: ''
  };

  /* ---------- Menú móvil ---------- */
  var botonMenu = document.querySelector('.boton-menu');
  var nav = document.querySelector('.nav');

  function pintarMenu(abierto) {
    nav.classList.toggle('abierto', abierto);
    botonMenu.classList.toggle('es-abierto', abierto);
    botonMenu.setAttribute('aria-expanded', String(abierto));
    botonMenu.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
  }

  if (botonMenu && nav) {
    botonMenu.addEventListener('click', function () {
      pintarMenu(!nav.classList.contains('abierto'));
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') pintarMenu(false);
    });
  }

  /* ---------- Tema claro / oscuro ---------- */
  var botonTema = document.querySelector('.boton-tema');
  var raiz = document.documentElement;

  function aplicarTema(tema) {
    if (tema === 'claro' || tema === 'oscuro') {
      raiz.setAttribute('data-tema', tema);
    } else {
      raiz.removeAttribute('data-tema');
    }
    if (botonTema) {
      var oscuroActivo = tema === 'oscuro' ||
        (!tema && window.matchMedia('(prefers-color-scheme: dark)').matches);
      botonTema.classList.toggle('es-oscuro', oscuroActivo);
      botonTema.setAttribute('aria-label',
        oscuroActivo ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
    }
  }

  var guardado = null;
  try { guardado = localStorage.getItem('lsd-tema'); } catch (e) { /* sin almacenamiento */ }
  aplicarTema(guardado);

  if (botonTema) {
    botonTema.addEventListener('click', function () {
      var actual = raiz.getAttribute('data-tema');
      if (!actual) {
        actual = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'oscuro' : 'claro';
      }
      var nuevo = actual === 'oscuro' ? 'claro' : 'oscuro';
      aplicarTema(nuevo);
      try { localStorage.setItem('lsd-tema', nuevo); } catch (e) { /* sin almacenamiento */ }
    });
  }

  /* ---------- Revelar secciones al desplazarse ---------- */
  var revelables = document.querySelectorAll('.revelar');
  if ('IntersectionObserver' in window && revelables.length) {
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visible');
          observador.unobserve(entrada.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    revelables.forEach(function (el) { observador.observe(el); });
  } else {
    revelables.forEach(function (el) { el.classList.add('visible'); });
  }

  /* ---------- Próximo congreso: aviso y cuenta regresiva ----------
     Los datos salen del bloque CONGRESO de arriba. El aviso funciona en
     cualquier página que lo incluya; la cuenta regresiva, en la página
     del congreso.                                                        */
  var proximo = document.querySelector('[data-proximo]');
  var avisoMarca = document.querySelector('[data-aviso-marca]');
  var avisoTexto = document.querySelector('[data-aviso-texto]');

  if (proximo || avisoMarca) {
    var sede   = (CONGRESO.sede || '').trim();
    var fechas = (CONGRESO.fechas || '').trim();
    var inicio = new Date(CONGRESO.inicio).getTime();
    var fin    = new Date(CONGRESO.fin).getTime();
    if (isNaN(fin)) fin = inicio;

    var cuenta = proximo && proximo.querySelector('.cuenta');
    var mensaje = proximo && proximo.querySelector('[data-cuenta-mensaje]');
    var casillas = {
      dias: cuenta && cuenta.querySelector('[data-dias]'),
      horas: cuenta && cuenta.querySelector('[data-horas]'),
      minutos: cuenta && cuenta.querySelector('[data-minutos]'),
      segundos: cuenta && cuenta.querySelector('[data-segundos]')
    };

    /* Sede, fechas y nombre de la edición en la tarjeta */
    if (proximo) {
      [['[data-proximo-edicion]', CONGRESO.edicion],
       ['[data-proximo-sede]', sede],
       ['[data-proximo-fechas]', fechas]].forEach(function (par) {
        var el = proximo.querySelector(par[0]);
        if (el && par[1]) el.textContent = par[1];
      });
    }

    function dosCifras(n) { return n < 10 ? '0' + n : String(n); }

    function anunciar(texto) {
      if (cuenta) cuenta.hidden = true;
      if (mensaje) { mensaje.textContent = texto; mensaje.hidden = false; }
    }

    function pintarAviso(marca, texto) {
      if (avisoMarca) avisoMarca.textContent = marca;
      if (avisoTexto) avisoTexto.textContent = texto;
    }

    function refrescar() {
      var ahora = Date.now();

      /* Todavía no hay fecha anunciada */
      if (isNaN(inicio) || !sede) {
        anunciar('Estamos preparando la próxima edición. Muy pronto anunciaremos la sede y las fechas.');
        pintarAviso('Congreso anual', 'Próxima sede y fecha por anunciar');
        return true;
      }

      /* El congreso ya empezó */
      if (inicio - ahora <= 0) {
        if (ahora <= fin) {
          anunciar('¡El congreso está en curso! Bienvenidos todos.');
          pintarAviso('En curso', sede + ' · ' + fechas);
        } else {
          anunciar('Esta edición ya se celebró. Pronto anunciaremos la sede del próximo congreso.');
          pintarAviso('Congreso anual', 'Próxima sede y fecha por anunciar');
        }
        return true;
      }

      /* Falta para el congreso: se actualiza la cuenta regresiva */
      if (cuenta) cuenta.hidden = false;
      if (mensaje) mensaje.hidden = true;
      pintarAviso('Próximo congreso', sede + (fechas ? ' · ' + fechas : ''));

      var seg = Math.floor((inicio - ahora) / 1000);
      if (casillas.dias) casillas.dias.textContent = Math.floor(seg / 86400);
      if (casillas.horas) casillas.horas.textContent = dosCifras(Math.floor(seg / 3600) % 24);
      if (casillas.minutos) casillas.minutos.textContent = dosCifras(Math.floor(seg / 60) % 60);
      if (casillas.segundos) casillas.segundos.textContent = dosCifras(seg % 60);
      return false;
    }

    if (!refrescar()) {
      var reloj = setInterval(function () {
        if (refrescar()) clearInterval(reloj);
      }, 1000);
    }
  }

  /* ---------- Año actual en el pie ---------- */
  var anio = document.querySelector('[data-anio]');
  if (anio) anio.textContent = String(new Date().getFullYear());

  /* ---------- Formularios (abren el programa de correo) ---------- */
  var formularios = document.querySelectorAll('[data-formulario-contacto]');

  Array.prototype.forEach.call(formularios, function (formulario) {
    formulario.addEventListener('submit', function (e) {
      e.preventDefault();

      var destino = formulario.getAttribute('data-destino') || '';
      var etiqueta = formulario.getAttribute('data-asunto') || 'Mensaje del sitio';
      var datos = new FormData(formulario);
      var lineas = [];

      datos.forEach(function (valor, clave) {
        var texto = String(valor).trim();
        if (!texto) return;
        lineas.push(clave.charAt(0).toUpperCase() + clave.slice(1) + ': ' + texto);
      });

      var asunto = '[La Sana Doctrina No Morirá] ' + etiqueta;
      var cuerpo = lineas.join('\n');

      window.location.href = 'mailto:' + destino +
        '?subject=' + encodeURIComponent(asunto) +
        '&body=' + encodeURIComponent(cuerpo);
    });
  });
})();

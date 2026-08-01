/* ============================================================
   La Sana Doctrina No Morirá — comportamiento del sitio
   Sin librerías externas.
   ============================================================ */
(function () {
  'use strict';

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

  /* ---------- Resaltar la sección visible en el menú ---------- */
  var enlaces = Array.prototype.slice.call(
    document.querySelectorAll('.nav a[href^="#"]')
  );
  var secciones = enlaces
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if ('IntersectionObserver' in window && secciones.length) {
    var espia = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        enlaces.forEach(function (a) {
          a.classList.toggle('activo',
            a.getAttribute('href') === '#' + entrada.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    secciones.forEach(function (s) { espia.observe(s); });
  }

  /* ---------- Logo original, si está disponible ----------
     Basta con copiar el archivo del logotipo a assets/img/ con el nombre
     logo.png (o logo.webp / logo.jpg). Si existe, sustituye al emblema
     dibujado en vectores; si no existe, no pasa nada.                      */
  var emblema = document.querySelector('[data-emblema]');

  if (emblema) {
    var candidatos = ['assets/img/logo.png', 'assets/img/logo.webp', 'assets/img/logo.jpg'];

    (function probar(i) {
      if (i >= candidatos.length) return;
      var prueba = new Image();
      prueba.onload = function () { emblema.src = candidatos[i]; };
      prueba.onerror = function () { probar(i + 1); };
      prueba.src = candidatos[i];
    })(0);
  }

  /* ---------- Próximo congreso: datos, aviso y cuenta regresiva ----------
     Toda la información sale de los atributos data-* del bloque
     <article data-proximo> que está en index.html. Si están vacíos o la
     fecha ya pasó, la página muestra sola el aviso correspondiente.        */
  var proximo = document.querySelector('[data-proximo]');

  if (proximo) {
    var dato = function (nombre) {
      return (proximo.getAttribute('data-' + nombre) || '').trim();
    };
    var pon = function (selector, texto) {
      var el = proximo.querySelector(selector);
      if (el && texto) el.textContent = texto;
    };

    var edicion = dato('edicion');
    var sede    = dato('sede');
    var fechas  = dato('fechas');
    var inicio  = new Date(dato('inicio')).getTime();
    var fin     = new Date(dato('fin')).getTime();
    if (isNaN(fin)) fin = inicio;

    pon('[data-proximo-edicion]', edicion);
    pon('[data-proximo-sede]', sede);
    pon('[data-proximo-fechas]', fechas);

    var cuenta = proximo.querySelector('.cuenta');
    var mensaje = proximo.querySelector('[data-cuenta-mensaje]');
    var avisoMarca = document.querySelector('[data-aviso-marca]');
    var avisoTexto = document.querySelector('[data-aviso-texto]');

    var casillas = {
      dias: cuenta && cuenta.querySelector('[data-dias]'),
      horas: cuenta && cuenta.querySelector('[data-horas]'),
      minutos: cuenta && cuenta.querySelector('[data-minutos]'),
      segundos: cuenta && cuenta.querySelector('[data-segundos]')
    };

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

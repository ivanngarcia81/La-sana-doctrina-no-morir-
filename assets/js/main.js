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

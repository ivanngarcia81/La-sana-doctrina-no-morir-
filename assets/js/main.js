/* ============================================================
   La sana doctrina no morirá — comportamiento del sitio
   Sin librerías externas.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Menú móvil ---------- */
  var botonMenu = document.querySelector('.boton-menu');
  var nav = document.querySelector('.nav');

  if (botonMenu && nav) {
    botonMenu.addEventListener('click', function () {
      var abierto = nav.classList.toggle('abierto');
      botonMenu.setAttribute('aria-expanded', String(abierto));
      botonMenu.textContent = abierto ? '✕' : '☰';
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('abierto');
        botonMenu.setAttribute('aria-expanded', 'false');
        botonMenu.textContent = '☰';
      }
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
      botonTema.textContent = oscuroActivo ? '☀' : '☾';
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
      var prefiereOscuro = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (!actual) actual = prefiereOscuro ? 'oscuro' : 'claro';
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
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    revelables.forEach(function (el) { observador.observe(el); });
  } else {
    revelables.forEach(function (el) { el.classList.add('visible'); });
  }

  /* ---------- Año actual en el pie ---------- */
  var anio = document.querySelector('[data-anio]');
  if (anio) anio.textContent = String(new Date().getFullYear());

  /* ---------- Formulario de contacto (abre el correo) ---------- */
  var formulario = document.querySelector('[data-formulario-contacto]');
  if (formulario) {
    formulario.addEventListener('submit', function (e) {
      e.preventDefault();
      var destino = formulario.getAttribute('data-destino') || '';
      var datos = new FormData(formulario);
      var nombre = (datos.get('nombre') || '').toString().trim();
      var correo = (datos.get('correo') || '').toString().trim();
      var motivo = (datos.get('motivo') || '').toString().trim();
      var mensaje = (datos.get('mensaje') || '').toString().trim();

      var asunto = '[La sana doctrina no morirá] ' + (motivo || 'Mensaje del sitio');
      var cuerpo =
        'Nombre: ' + nombre + '\n' +
        'Correo: ' + correo + '\n' +
        'Motivo: ' + motivo + '\n\n' +
        mensaje;

      window.location.href = 'mailto:' + destino +
        '?subject=' + encodeURIComponent(asunto) +
        '&body=' + encodeURIComponent(cuerpo);
    });
  }
})();

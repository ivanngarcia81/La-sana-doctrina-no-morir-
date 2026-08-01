/* ============================================================
   La Sana Doctrina No Morirá — comportamiento del sitio
   Sin librerías externas.
   ============================================================ */
(function () {
  'use strict';

  /* Marca que el JavaScript está activo: el CSS usa .sin-js para desplegar
     el submenú solo con el puntero o el foco cuando esto no se ejecuta. */
  document.documentElement.classList.remove('sin-js');

  /* ============================================================
     CONGRESO y EDICIONES SON LOS DOS ÚNICOS BLOQUES QUE HAY QUE
     ACTUALIZAR CADA AÑO. Todo lo demás del sitio se alimenta de aquí.
     ============================================================ */

  /* ------------------------------------------------------------
     PRÓXIMO CONGRESO. Se usa en la página del congreso y en el
     aviso de la portada.

       edicion  Nombre de la edición, p. ej. 'Edición 2027'
       sede     Ciudad y país,        p. ej. 'Ciudad de Panamá, Panamá'
       fechas   Texto de las fechas,  p. ej. '16, 17 y 18 de julio de 2027'
       inicio   Inicio en formato ISO con zona horaria,
                p. ej. '2027-07-16T09:00:00-05:00'
       fin      Cierre en el mismo formato

     Si se dejan vacíos, la página muestra sola el aviso
     "sede y fecha por anunciar".
     ------------------------------------------------------------ */
  var CONGRESO = {
    edicion: '',
    sede: '',
    fechas: '',
    inicio: '',
    fin: ''
  };

  /* ------------------------------------------------------------
     EDICIONES YA CELEBRADAS. De aquí sale el programa por jornadas
     que aparece en congreso.html, para no tener los mismos datos
     escritos también en el HTML.

     La más reciente va primero. Cada edición lleva:

       edicion   Nombre de la edición, p. ej. 'Edición 2026'
       sede      Ciudad y país
       fechas    Texto del periodo, p. ej. 'julio de 2026'
       jornadas  Una entrada por día, cada una con:
                   fecha   Rótulo del día
                   titulo  Título de la jornada
                   texto   Descripción

     Para publicar otra edición basta con añadir un objeto más.
     ------------------------------------------------------------ */
  var EDICIONES = [
    {
      edicion: 'Edición 2026',
      sede: 'Cartagena, Colombia',
      fechas: 'julio de 2026',
      jornadas: [
        {
          fecha: 'Viernes 17 julio 2026',
          titulo: 'La Sana Doctrina No Morirá · Apertura en Cartagena, Colombia',
          texto: 'Con gozo en el Señor, damos inicio al Congreso “La Sana Doctrina No ' +
                 'Morirá”, un espacio dedicado a exaltar la verdad de la Palabra de Dios y ' +
                 'afirmar nuestra fe en tiempos de confusión doctrinal. Hoy nos congregamos ' +
                 'con un solo propósito: defender, vivir y proclamar la sana doctrina que ha ' +
                 'sido transmitida por los apóstoles y permanece viva por el Espíritu Santo. ' +
                 '¡Bienvenidos todos!'
        },
        {
          fecha: 'Sábado 18 julio 2026',
          titulo: 'La Sana Doctrina No Morirá · Segundo día',
          texto: 'Damos la bienvenida al segundo día de nuestro Congreso “La Sana Doctrina ' +
                 'No Morirá”, agradeciendo al Señor por lo que ya ha comenzado a hacer en ' +
                 'medio de nosotros. Hoy continuamos fortaleciendo nuestras convicciones ' +
                 'bíblicas, recibiendo enseñanza sólida y edificándonos unos a otros en el ' +
                 'amor y la verdad de Cristo. Que cada palabra y cada momento de este día ' +
                 'glorifique a Dios y afirme nuestro compromiso con Su doctrina eterna.'
        },
        {
          fecha: 'Domingo 19 julio 2026',
          titulo: 'La Sana Doctrina No Morirá · Tercer día',
          texto: 'En este tercer día del congreso, nos reunimos con un mismo propósito: ' +
                 'afirmar la verdad de la Palabra de Dios y permanecer firmes en la sana ' +
                 'doctrina. Será un tiempo de enseñanza, predicación y edificación ' +
                 'espiritual, donde la iglesia será llamada a no callar ante la apostasía, ' +
                 'sino a defender con fidelidad el evangelio de Jesucristo.'
        }
      ]
    }
  ];

  /* ---------- Menú principal ----------
     Un solo comportamiento para escritorio y móvil:
       · el botón hamburguesa abre y cierra el panel a pantalla completa
       · los grupos con submenú se abren con clic, Enter o Espacio
       · Escape cierra el submenú abierto y devuelve el foco al disparador
       · un clic fuera cierra lo que estuviera abierto                     */
  var botonMenu = document.querySelector('.boton-menu');
  var nav = document.querySelector('.nav');
  var grupos = Array.prototype.slice.call(document.querySelectorAll('[data-grupo]'));

  function pintarGrupo(grupo, abierto) {
    var disparador = grupo.querySelector('.nav__disparador');
    grupo.classList.toggle('abierto', abierto);
    if (disparador) disparador.setAttribute('aria-expanded', String(abierto));
  }

  function cerrarGrupos(excepto) {
    grupos.forEach(function (g) { if (g !== excepto) pintarGrupo(g, false); });
  }

  /* ¿El dispositivo tiene puntero y espacio para el menú horizontal? */
  var conHover = window.matchMedia('(hover: hover) and (min-width: 1101px)').matches;

  /* Al cerrar con Escape se devuelve el foco al disparador; sin esta
     bandera, ese foco volvería a abrir el submenú al instante. */
  var ignorarFoco = false;

  grupos.forEach(function (grupo) {
    var disparador = grupo.querySelector('.nav__disparador');
    if (!disparador) return;

    var alternar = function () {
      var abierto = !grupo.classList.contains('abierto');
      cerrarGrupos(grupo);
      pintarGrupo(grupo, abierto);
    };

    /* El disparador es un enlace real a la primera página del grupo.
       · Con puntero: el submenú ya se abrió al pasar por encima, así que
         el clic hace lo natural en un enlace, navegar.
       · Sin puntero (táctil): se cancela la navegación y el toque
         despliega, que es lo que se espera en un móvil.
       Sin JavaScript no se ejecuta nada de esto y el enlace navega. */
    disparador.addEventListener('click', function (e) {
      if (conHover) return;
      e.preventDefault();
      alternar();
    });

    /* En un enlace la barra espaciadora no dispara click por sí sola */
    disparador.addEventListener('keydown', function (e) {
      if (e.key !== ' ' && e.key !== 'Spacebar') return;
      e.preventDefault();
      alternar();
    });

    /* Al llegar con el teclado se despliega, para que Tab pueda entrar
       en las opciones. Con el ratón no, porque de eso ya se ocupa hover. */
    disparador.addEventListener('focus', function () {
      if (ignorarFoco) return;
      if (typeof disparador.matches === 'function' &&
          disparador.matches(':focus-visible')) {
        cerrarGrupos(grupo);
        pintarGrupo(grupo, true);
      }
    });

    /* En escritorio también se abre al pasar el puntero. El cierre lleva
       un margen de 260 ms para que dé tiempo a llegar al submenú aunque el
       puntero salga un instante del grupo. */
    if (conHover) {
      var temporizador = null;

      grupo.addEventListener('mouseenter', function () {
        clearTimeout(temporizador);
        cerrarGrupos(grupo);
        pintarGrupo(grupo, true);
      });

      grupo.addEventListener('mouseleave', function () {
        clearTimeout(temporizador);
        temporizador = setTimeout(function () { pintarGrupo(grupo, false); }, 260);
      });
    }

    /* El foco sale del grupo con Tab: se cierra solo */
    grupo.addEventListener('focusout', function (e) {
      if (!grupo.contains(e.relatedTarget)) pintarGrupo(grupo, false);
    });
  });

  function pintarMenu(abierto) {
    if (!nav || !botonMenu) return;
    nav.classList.toggle('abierto', abierto);
    botonMenu.classList.toggle('es-abierto', abierto);
    botonMenu.setAttribute('aria-expanded', String(abierto));
    botonMenu.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
    document.body.classList.toggle('sin-scroll', abierto);
    if (!abierto) cerrarGrupos(null);
  }

  if (botonMenu && nav) {
    botonMenu.addEventListener('click', function () {
      pintarMenu(!nav.classList.contains('abierto'));
    });

    nav.addEventListener('click', function (e) {
      /* El disparador despliega su submenú; no cierra el panel */
      if (e.target.closest('a') && !e.target.closest('.nav__disparador')) pintarMenu(false);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var grupoAbierto = grupos.filter(function (g) { return g.classList.contains('abierto'); })[0];
    if (grupoAbierto) {
      pintarGrupo(grupoAbierto, false);
      var d = grupoAbierto.querySelector('.nav__disparador');
      if (d) {
        ignorarFoco = true;
        d.focus();
        setTimeout(function () { ignorarFoco = false; }, 0);
      }
      return;
    }
    if (nav && nav.classList.contains('abierto')) {
      pintarMenu(false);
      if (botonMenu) botonMenu.focus();
    }
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('[data-grupo]')) cerrarGrupos(null);
  });

  /* Al pasar a escritorio se descarta el estado del panel móvil */
  window.matchMedia('(min-width: 1101px)').addEventListener('change', function (ev) {
    if (ev.matches) pintarMenu(false);
  });

  /* ---------- Encabezado: sombra y barra de progreso de lectura ---------- */
  var encabezado = document.querySelector('.encabezado');
  var progreso = document.querySelector('.encabezado__progreso');

  if (encabezado) {
    var pendiente = false;

    var pintarEncabezado = function () {
      pendiente = false;
      var y = window.scrollY || document.documentElement.scrollTop;
      encabezado.classList.toggle('encabezado--fijo', y > 8);

      if (progreso) {
        var alto = document.documentElement.scrollHeight - window.innerHeight;
        var avance = alto > 0 ? Math.min(1, Math.max(0, y / alto)) : 0;
        progreso.style.transform = 'scaleX(' + avance + ')';
      }
    };

    var alDesplazar = function () {
      if (pendiente) return;
      pendiente = true;
      window.requestAnimationFrame(pintarEncabezado);
    };

    pintarEncabezado();
    window.addEventListener('scroll', alDesplazar, { passive: true });
    window.addEventListener('resize', alDesplazar, { passive: true });
  }

  /* ---------- Ediciones ya celebradas ----------
     Se dibujan desde el array EDICIONES para no repetir los datos en el
     HTML. Va antes del observador de .revelar para que también las anime. */
  var zonaEdiciones = document.querySelector('[data-ediciones]');

  if (zonaEdiciones && EDICIONES.length) {
    var trozos = [];

    EDICIONES.forEach(function (ed, i) {
      var rotulo = (i === 0 ? 'Última edición' : ed.edicion);
      trozos.push('<h3 class="programa__titulo revelar">' +
                  rotulo + ' · ' + ed.sede + ' — ' + ed.fechas + '</h3>');
      trozos.push('<div class="rejilla rejilla--3 revelar">');
      ed.jornadas.forEach(function (j) {
        trozos.push('<article class="jornada">' +
                    '<p class="jornada__fecha">' + j.fecha + '</p>' +
                    '<h3 class="tarjeta__titulo">' + j.titulo + '</h3>' +
                    '<p>' + j.texto + '</p>' +
                    '</article>');
      });
      trozos.push('</div>');
    });

    zonaEdiciones.innerHTML = trozos.join('');
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
    /* Resumen para lectores de pantalla: la cuenta visible está marcada
       como aria-hidden porque anunciar los segundos sería insoportable.
       Este párrafo solo cambia cuando cambia el número de días. */
    var resumen = proximo && proximo.querySelector('[data-cuenta-resumen]');
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
      resumir(texto);
    }

    function resumir(texto) {
      /* Escribir el mismo texto volvería a anunciarlo, así que solo se
         toca el nodo cuando el contenido cambia de verdad. */
      if (resumen && resumen.textContent !== texto) resumen.textContent = texto;
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
      var dias = Math.floor(seg / 86400);
      resumir(dias === 1 ? 'Falta 1 día para el congreso'
                         : 'Faltan ' + dias + ' días para el congreso');
      if (casillas.dias) casillas.dias.textContent = dias;
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

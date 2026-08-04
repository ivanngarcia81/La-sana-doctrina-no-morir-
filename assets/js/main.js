/* ============================================================
   La Sana Doctrina No Morirá — comportamiento del sitio
   Sin librerías externas.
   ============================================================ */
(function () {
  'use strict';

  /* Marca que el JavaScript está activo: el CSS usa .sin-js para desplegar
     el submenú solo con el puntero o el foco cuando esto no se ejecuta. */
  document.documentElement.classList.remove('sin-js');

  /* Los datos de los congresos ya no viven aquí: están en
     data/congresos.json y generar.py los escribe en el HTML. Este archivo
     solo se ocupa de lo que depende de la hora en que se abre la página
     (el estado de cada congreso y la cuenta regresiva) y de los botones
     de calendario y de compartir.

     Para cambiar sedes, fechas o programas: data/congresos.json. */
  function datosCongresos() {
    var caja = document.getElementById('datos-congresos');
    if (!caja) return [];
    try { return JSON.parse(caja.textContent) || []; }
    catch (e) { return []; }
  }

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

  /* ---------- Estado de cada congreso ----------
     El HTML sale con el estado del día en que se generó el sitio. Aquí se
     vuelve a calcular con la fecha del visitante, para que una edición que
     ya pasó deje de anunciarse como próxima aunque nadie haya regenerado
     el sitio en meses. Las fechas se comparan como texto AAAA-MM-DD, que
     ordena igual que el calendario y no arrastra husos horarios. */
  var ROTULOS = {
    por_anunciar: 'Por anunciar',
    proximo: 'Próximo',
    en_curso: 'En curso',
    finalizado: 'Finalizado'
  };

  function dosCifras(n) { return n < 10 ? '0' + n : String(n); }

  function hoyISO() {
    var d = new Date();
    return d.getFullYear() + '-' + dosCifras(d.getMonth() + 1) + '-' + dosCifras(d.getDate());
  }

  function estadoDe(inicio, fin) {
    if (!inicio) return 'por_anunciar';
    var hoy = hoyISO();
    if (hoy < inicio) return 'proximo';
    if (hoy <= (fin || inicio)) return 'en_curso';
    return 'finalizado';
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-estado]'), function (el) {
    var est = estadoDe(el.getAttribute('data-inicio'), el.getAttribute('data-fin'));
    el.className = 'estado estado--' + est;
    el.textContent = ROTULOS[est];
  });

  /* ---------- Cuenta regresiva ----------
     La sede y las fechas ya vienen escritas en el HTML; aquí solo se añade
     el reloj y se corrige el mensaje cuando el congreso empieza o termina. */
  var proximo = document.querySelector('[data-proximo]');
  var avisoMarca = document.querySelector('[data-aviso-marca]');
  var avisoTexto = document.querySelector('[data-aviso-texto]');

  if (proximo) {
    /* La tarjeta se generó apuntando a la edición más cercana del día en
       que se construyó el sitio. Si esa ya pasó y hay otra por delante, se
       asciende aquí: así la portada no se queda anclada a un congreso
       terminado mientras nadie vuelve a generar. */
    var pendientes = datosCongresos().filter(function (c) {
      return c.inicio && estadoDe(c.inicio, c.fin) !== 'finalizado';
    }).sort(function (a, b) { return a.inicio < b.inicio ? -1 : 1; });

    var elegido = pendientes[0];
    if (elegido && elegido.slug !== proximo.getAttribute('data-slug')) {
      var raiz = proximo.getAttribute('data-base') || '';
      proximo.setAttribute('data-slug', elegido.slug);
      proximo.setAttribute('data-inicio', elegido.inicio);
      proximo.setAttribute('data-fin', elegido.fin || '');
      [['.proximo__edicion', elegido.edicion],
       ['.proximo__sede', elegido.lugar],
       ['.proximo__fechas', elegido.fechas]].forEach(function (par) {
        var el = proximo.querySelector(par[0]);
        if (el && par[1]) el.textContent = par[1];
      });
      var enlace = proximo.querySelector('.botones a');
      if (enlace) {
        enlace.href = raiz + 'congresos/' + elegido.slug + '/';
        enlace.textContent = 'Ver detalles';
      }
    }
  }

  if (proximo && proximo.getAttribute('data-inicio')) {
    var inicioISO = proximo.getAttribute('data-inicio');
    var finISO = proximo.getAttribute('data-fin') || inicioISO;
    /* Sin hora anunciada, la cuenta va al primer minuto del día de apertura,
       en la hora local de quien mira. */
    var inicio = new Date(inicioISO + 'T00:00:00').getTime();
    var fin = new Date(finISO + 'T23:59:59').getTime();

    var cuenta = proximo.querySelector('.cuenta');
    var mensaje = proximo.querySelector('[data-cuenta-mensaje]');
    /* Resumen para lectores de pantalla: la cuenta visible está marcada
       como aria-hidden porque anunciar los segundos sería insoportable.
       Este párrafo solo cambia cuando cambia el número de días. */
    var resumen = proximo.querySelector('[data-cuenta-resumen]');
    var casillas = {
      dias: proximo.querySelector('[data-dias]'),
      horas: proximo.querySelector('[data-horas]'),
      minutos: proximo.querySelector('[data-minutos]'),
      segundos: proximo.querySelector('[data-segundos]')
    };

    var resumir = function (texto) {
      /* Escribir el mismo texto volvería a anunciarlo, así que solo se
         toca el nodo cuando el contenido cambia de verdad. */
      if (resumen && resumen.textContent !== texto) resumen.textContent = texto;
    };

    var anunciar = function (texto) {
      if (cuenta) cuenta.hidden = true;
      if (mensaje) { mensaje.textContent = texto; mensaje.hidden = false; }
      resumir(texto);
    };

    var pintarAviso = function (marca, texto) {
      if (avisoMarca) avisoMarca.textContent = marca;
      if (avisoTexto) avisoTexto.textContent = texto;
    };

    var sede = (proximo.querySelector('.proximo__sede') || {}).textContent || '';
    var fechas = (proximo.querySelector('.proximo__fechas') || {}).textContent || '';

    var refrescar = function () {
      var ahora = Date.now();

      if (ahora >= inicio) {
        if (ahora <= fin) {
          anunciar('¡El congreso está en curso! Bienvenidos todos.');
          pintarAviso('En curso', sede);
        } else {
          anunciar('Esta edición ya se celebró. Pronto anunciaremos la sede del próximo congreso.');
          pintarAviso('Congreso anual', 'Próxima sede y fecha por anunciar');
        }
        return true;
      }

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
    };

    if (!refrescar()) {
      var reloj = setInterval(function () {
        if (refrescar()) clearInterval(reloj);
      }, 1000);
    }
  }

  /* ---------- Agregar al calendario y compartir ----------
     El .ics se arma aquí mismo, sin librerías. Un congreso de varios días
     se agenda como evento de día completo: es lo correcto y así no se
     desplaza al cambiar de huso horario. En el formato .ics el día de fin
     es exclusivo, por eso generar.py ya suma uno. */
  var acciones = document.querySelector('[data-acciones]');

  if (acciones) {
    var congreso = {
      nombre: acciones.getAttribute('data-nombre') || 'Congreso',
      inicio: acciones.getAttribute('data-inicio') || '',
      fin: acciones.getAttribute('data-fin') || '',
      lugar: acciones.getAttribute('data-lugar') || '',
      slug: acciones.getAttribute('data-slug') || 'congreso'
    };
    var sinGuiones = function (iso) { return iso.replace(/-/g, ''); };

    var escaparICS = function (t) {
      return String(t || '').replace(/\\/g, '\\\\').replace(/;/g, '\\;')
        .replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
    };

    var sello = function () {
      return new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
    };

    var textoICS = function () {
      return [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//La Sana Doctrina No Morira//ES',
        'CALSCALE:GREGORIAN',
        'BEGIN:VEVENT',
        'UID:' + congreso.slug + '@lasanadoctrinanomorira',
        'DTSTAMP:' + sello(),
        'DTSTART;VALUE=DATE:' + sinGuiones(congreso.inicio),
        'DTEND;VALUE=DATE:' + sinGuiones(congreso.fin),
        'SUMMARY:' + escaparICS(congreso.nombre),
        'LOCATION:' + escaparICS(congreso.lugar),
        'DESCRIPTION:' + escaparICS('Entrada libre. ' + location.href),
        'URL:' + location.href,
        'END:VEVENT',
        'END:VCALENDAR'
      ].join('\r\n');   /* el formato .ics exige fin de línea CRLF */
    };

    var botonCal = acciones.querySelector('[data-calendario]');
    if (botonCal && congreso.inicio) {
      botonCal.hidden = false;
      botonCal.addEventListener('click', function () {
        var blob = new Blob([textoICS()], { type: 'text/calendar;charset=utf-8' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = congreso.slug + '.ics';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        /* Se libera algo después: revocarla en el acto cancela la descarga
           en algunos navegadores. */
        setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
      });

      /* Google Calendar, para quien vive en el calendario del navegador */
      var google = document.createElement('a');
      google.className = 'boton boton--linea';
      google.target = '_blank';
      google.rel = 'noopener';
      google.textContent = 'Google Calendar';
      google.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
        + '&text=' + encodeURIComponent(congreso.nombre)
        + '&dates=' + sinGuiones(congreso.inicio) + '/' + sinGuiones(congreso.fin)
        + '&location=' + encodeURIComponent(congreso.lugar)
        + '&details=' + encodeURIComponent('Entrada libre. ' + location.href);
      acciones.appendChild(google);
    }

    var botonComp = acciones.querySelector('[data-compartir]');
    var listaComp = document.querySelector('[data-compartir-lista]');

    if (botonComp) {
      botonComp.hidden = false;
      botonComp.addEventListener('click', function () {
        var datos = {
          title: congreso.nombre,
          text: congreso.nombre + ' — entrada libre.',
          url: location.href
        };
        if (navigator.share) {
          navigator.share(datos).catch(function () { /* cancelado por quien comparte */ });
          return;
        }
        /* Sin API nativa: se despliega la lista de siempre */
        if (!listaComp) return;
        if (!listaComp.childNodes.length) {
          var texto = encodeURIComponent(datos.text + ' ' + location.href);
          listaComp.innerHTML =
            '<a class="boton boton--linea" target="_blank" rel="noopener" href="https://wa.me/?text='
            + texto + '">WhatsApp</a>'
            + '<a class="boton boton--linea" target="_blank" rel="noopener" '
            + 'href="https://www.facebook.com/sharer/sharer.php?u='
            + encodeURIComponent(location.href) + '">Facebook</a>'
            + '<button class="boton boton--linea" type="button" data-copiar>Copiar enlace</button>';

          var copiar = listaComp.querySelector('[data-copiar]');
          copiar.addEventListener('click', function () {
            var listo = function () {
              copiar.textContent = 'Enlace copiado';
              setTimeout(function () { copiar.textContent = 'Copiar enlace'; }, 2500);
            };
            if (navigator.clipboard) {
              navigator.clipboard.writeText(location.href).then(listo, function () {});
            } else {
              /* Navegadores viejos: campo temporal y execCommand */
              var campo = document.createElement('input');
              campo.value = location.href;
              document.body.appendChild(campo);
              campo.select();
              try { document.execCommand('copy'); listo(); } catch (e) {}
              document.body.removeChild(campo);
            }
          });
        }
        listaComp.hidden = !listaComp.hidden;
        botonComp.setAttribute('aria-expanded', String(!listaComp.hidden));
      });
      botonComp.setAttribute('aria-expanded', 'false');
      if (listaComp && listaComp.id) botonComp.setAttribute('aria-controls', listaComp.id);
    }
  }

  /* ---------- Año actual en el pie ---------- */
  var anio = document.querySelector('[data-anio]');
  if (anio) anio.textContent = String(new Date().getFullYear());

  /* ---------- Formularios ----------
     FASE DE DISEÑO: no envían a ningún servicio. La validación y los
     mensajes ya funcionan; cuando se rellene FORMULARIO_DESTINO en
     generar.py el formulario saldrá con action y este mismo código lo
     enviará, sin tocar nada más.

     Se usa novalidate para escribir los mensajes en español y junto al
     campo que falla, en vez de los globos del navegador, que se pierden
     al desplazarse. */
  function mensajeDe(campo) {
    var v = campo.validity;
    if (v.valueMissing) {
      return campo.tagName === 'SELECT' ? 'Elige una opción.' : 'Falta rellenar este campo.';
    }
    if (v.typeMismatch && campo.type === 'email') {
      return 'Escribe un correo válido, como nombre@ejemplo.com.';
    }
    if (v.typeMismatch && campo.type === 'tel') return 'Revisa el número de teléfono.';
    if (v.tooShort) return 'Escribe al menos ' + campo.minLength + ' caracteres.';
    return 'Revisa este dato.';
  }

  function pintarCampo(campo) {
    var caja = campo.parentNode;
    var aviso = caja && caja.querySelector ? caja.querySelector('.campo__error') : null;
    if (campo.checkValidity()) {
      campo.removeAttribute('aria-invalid');
      if (aviso) { aviso.textContent = ''; aviso.hidden = true; }
      return true;
    }
    campo.setAttribute('aria-invalid', 'true');
    if (aviso) { aviso.textContent = mensajeDe(campo); aviso.hidden = false; }
    return false;
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-formulario]'), function (form) {
    var estado = form.querySelector('[data-estado-envio]');
    var boton = form.querySelector('button[type="submit"]');

    var avisar = function (texto, clase) {
      if (!estado) return;
      estado.textContent = texto;
      estado.className = 'formulario__estado' + (clase ? ' ' + clase : '');
      estado.hidden = false;
    };

    /* Se revalida al salir del campo, pero solo después del primer intento
       de envío: corregir a alguien mientras escribe molesta. */
    var intentado = false;
    Array.prototype.forEach.call(form.elements, function (campo) {
      if (!campo.name) return;
      campo.addEventListener('blur', function () { if (intentado) pintarCampo(campo); });
      campo.addEventListener('input', function () { if (intentado) pintarCampo(campo); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      intentado = true;

      var malos = Array.prototype.filter.call(form.elements, function (campo) {
        return campo.name && !pintarCampo(campo);
      });

      if (malos.length) {
        avisar(malos.length === 1 ? 'Falta un dato por revisar.'
                                  : 'Faltan ' + malos.length + ' datos por revisar.',
               'formulario__estado--error');
        malos[0].focus();
        return;
      }

      var destino = form.getAttribute('action');
      if (!destino) {
        /* Todavía sin conectar: se dice claro, en vez de fingir un envío. */
        avisar('El formulario aún no está conectado. Mientras tanto puedes '
               + 'escribirnos por WhatsApp o al correo que aparece al pie de la página.',
               'formulario__estado--aviso');
        return;
      }

      if (boton) boton.disabled = true;
      avisar('Enviando…', '');

      fetch(destino, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      }).then(function (r) {
        if (!r.ok) throw new Error('respuesta ' + r.status);
        form.reset();
        intentado = false;
        avisar('Mensaje enviado. Gracias por escribir: respondemos en cuanto podamos.',
               'formulario__estado--exito');
      }).catch(function () {
        avisar('No se pudo enviar. Revisa tu conexión e inténtalo de nuevo, o '
               + 'escríbenos por WhatsApp.', 'formulario__estado--error');
      }).then(function () {
        if (boton) boton.disabled = false;
      });
    });
  });
})();

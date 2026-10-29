/**
 * ==========================================================
 * JAGUAR CORP
 * Sistema de Facturación de Clientes
 * ==========================================================
 *
 * Archivo: app.js
 *
 * Descripción:
 * Controla las interacciones generales de la interfaz web.
 *
 * Funcionalidades:
 * 1. Menú lateral responsive.
 * 2. Navegación activa.
 * 3. Notificaciones SweetAlert2.
 * 4. Accesibilidad del menú.
 *
 * Tecnologías:
 * - JavaScript
 * - Bootstrap 5
 * - SweetAlert2
 */


/* ==========================================================
   1. INICIALIZACIÓN DE LA APLICACIÓN
========================================================== */

/**
 * Espera a que el navegador termine de cargar el HTML.
 *
 * Esto permite acceder de forma segura a los elementos
 * de la página antes de utilizarlos.
 */

document.addEventListener("DOMContentLoaded", function () {

    inicializarMenu();

    inicializarNavegacion();

    mostrarMensajesFlask();

});


/* ==========================================================
   2. MENÚ LATERAL
========================================================== */

/**
 * Configura el botón que abre y cierra el menú lateral.
 *
 * En pantallas pequeñas, el menú funciona como un
 * panel desplegable.
 *
 * En pantallas grandes, puede contraerse si los estilos
 * CSS incluyen esa funcionalidad.
 */

function inicializarMenu() {

    const sidebar = document.getElementById("sidebar");

    const menuToggle = document.getElementById("menuToggle");

    // Comprobar que ambos elementos existan.
    if (!sidebar || !menuToggle) {
        return;
    }

    // Abrir o cerrar el menú.
    menuToggle.addEventListener("click", function () {

        const menuAbierto = sidebar.classList.toggle("show");

        // Informar a tecnologías de asistencia
        // sobre el estado actual del menú.
        menuToggle.setAttribute(
            "aria-expanded",
            String(menuAbierto)
        );

    });


    // Cerrar el menú al presionar Escape.
    document.addEventListener("keydown", function (evento) {

        if (evento.key === "Escape") {

            cerrarMenu();

        }

    });


    // Cerrar el menú al hacer clic fuera de él
    // únicamente en pantallas pequeñas.
    document.addEventListener("click", function (evento) {

        const pantallaPequena = window.innerWidth <= 768;

        if (!pantallaPequena) {
            return;
        }

        const clicDentroMenu = sidebar.contains(
            evento.target
        );

        const clicBoton = menuToggle.contains(
            evento.target
        );

        if (!clicDentroMenu && !clicBoton) {

            cerrarMenu();

        }

    });


    // Cerrar el menú cuando cambia el tamaño
    // de la ventana hacia una pantalla grande.
    window.addEventListener("resize", function () {

        if (window.innerWidth > 768) {

            cerrarMenu();

        }

    });


    /**
     * Cierra el menú lateral.
     */
    function cerrarMenu() {

        sidebar.classList.remove("show");

        menuToggle.setAttribute(
            "aria-expanded",
            "false"
        );

    }

}


/* ==========================================================
   3. NAVEGACIÓN ACTIVA
========================================================== */

/**
 * Comprueba qué enlace corresponde a la página actual.
 *
 * El estado principal se establece desde Jinja2
 * en base.html.
 *
 * Esta función refuerza la accesibilidad al mantener
 * el atributo aria-current.
 */

function inicializarNavegacion() {

    const enlaces = document.querySelectorAll(
        ".sidebar-nav .nav-link"
    );

    enlaces.forEach(function (enlace) {

        const estaActivo = enlace.classList.contains(
            "active"
        );

        if (estaActivo) {

            enlace.setAttribute(
                "aria-current",
                "page"
            );

        } else {

            enlace.removeAttribute(
                "aria-current"
            );

        }

    });

}


/* ==========================================================
   4. NOTIFICACIONES DE FLASK
========================================================== */

/**
 * Obtiene los mensajes flash enviados desde Python.
 *
 * Los mensajes se encuentran en base.html:
 *
 * <div class="flash-message"
 *      data-category="success"
 *      data-message="Factura registrada">
 * </div>
 *
 * SweetAlert2 muestra el mensaje en una ventana.
 */

function mostrarMensajesFlask() {

    const mensajes = document.querySelectorAll(
        ".flash-message"
    );

    // Si no existen mensajes, no hacemos nada.
    if (mensajes.length === 0) {
        return;
    }

    // Comprobar que SweetAlert2 esté disponible.
    if (typeof Swal === "undefined") {

        console.error(
            "Jaguar Corp: SweetAlert2 no está disponible."
        );

        return;
    }

    // Convertir los mensajes en una lista.
    const notificaciones = Array.from(mensajes);

    // Mostrar los mensajes uno después de otro.
    mostrarSiguienteMensaje(notificaciones, 0);

}


/* ==========================================================
   5. MOSTRAR MENSAJES EN ORDEN
========================================================== */

/**
 * Muestra cada notificación de forma secuencial.
 *
 * Args:
 *     mensajes: Lista de elementos HTML.
 *     indice: Posición del mensaje actual.
 *
 * JavaScript no utiliza anotaciones Args como Python,
 * pero documentamos los parámetros para facilitar
 * la comprensión del código.
 */

function mostrarSiguienteMensaje(mensajes, indice) {

    // Finalizar cuando no queden mensajes.
    if (indice >= mensajes.length) {
        return;
    }

    const mensaje = mensajes[indice];

    const categoria = mensaje.dataset.category;

    const texto = mensaje.dataset.message;

    // Determinar el tipo de alerta.
    let icono = "info";

    let titulo = "Información";

    switch (categoria) {

        case "success":

            icono = "success";

            titulo = "Operación exitosa";

            break;

        case "error":

            icono = "error";

            titulo = "Ha ocurrido un error";

            break;

        case "warning":

            icono = "warning";

            titulo = "Advertencia";

            break;

        default:

            icono = "info";

            titulo = "Información";

    }

    // Mostrar la notificación.
    Swal.fire({

        icon: icono,

        title: titulo,

        text: texto,

        confirmButtonText: "Aceptar",

        confirmButtonColor: "#0066ff",

        allowOutsideClick: true

    }).then(function () {

        // Mostrar el siguiente mensaje.
        mostrarSiguienteMensaje(
            mensajes,
            indice + 1
        );

    });

}
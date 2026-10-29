document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // ELEMENTOS DEL FORMULARIO
    // ==========================================

    const formulario = document.getElementById("formFactura");
    const campoFecha = document.getElementById("fecha");
    const campoMonto = document.getElementById("monto");
    const campoEstado = document.getElementById("estado_pago");
    const campoCliente = document.getElementById("cliente");

    if (!formulario || !campoFecha || !campoMonto || !campoEstado) {
        return;
    }


    // ==========================================
    // FECHA ACTUAL
    // ==========================================

    function obtenerFechaActual() {

        const hoy = new Date();

        const anio = hoy.getFullYear();

        const mes = String(
            hoy.getMonth() + 1
        ).padStart(2, "0");

        const dia = String(
            hoy.getDate()
        ).padStart(2, "0");

        return `${anio}-${mes}-${dia}`;
    }

    campoFecha.value = obtenerFechaActual();


    // ==========================================
    // VALIDAR MONTO Y ESTADO
    // ==========================================

    function validarMontoEstado() {

        const monto = Number(campoMonto.value);
        const estado = campoEstado.value;

        campoMonto.setCustomValidity("");

        if (
            campoMonto.value !== "" &&
            estado === "Pagado" &&
            monto <= 0
        ) {
            campoMonto.setCustomValidity(
                "Una factura pagada debe tener un monto mayor que cero."
            );
        }

    }

    campoMonto.addEventListener("input", validarMontoEstado);

    campoEstado.addEventListener("change", validarMontoEstado);


    // ==========================================
    // VALIDACIÓN DEL FORMULARIO
    // ==========================================

    formulario.addEventListener("submit", function (evento) {

        validarMontoEstado();

        // Evitar nombres compuestos solamente por espacios.
        if (campoCliente.value.trim() === "") {

            campoCliente.setCustomValidity(
                "Debes ingresar el nombre del cliente."
            );

        } else {

            campoCliente.setCustomValidity("");

        }

        if (!formulario.checkValidity()) {

            evento.preventDefault();

            formulario.reportValidity();

        }

    });

    campoCliente.addEventListener("input", function () {
        campoCliente.setCustomValidity("");
    });


    // ==========================================
    // BOTÓN LIMPIAR
    // ==========================================

    formulario.addEventListener("reset", function () {

        setTimeout(function () {

            campoFecha.value = obtenerFechaActual();

            campoMonto.setCustomValidity("");
            campoCliente.setCustomValidity("");

        }, 0);

    });

});
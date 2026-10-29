document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // CONFIRMAR EL PAGO
    // ==========================================

    const formPagar = document.getElementById("formPagar");

    if (formPagar) {

        formPagar.addEventListener("submit", function (evento) {

            evento.preventDefault();

            Swal.fire({

                title: "¿Confirmar pago?",

                text: "La factura cambiará su estado a Pagado.",

                icon: "question",

                showCancelButton: true,

                confirmButtonColor: "#198754",

                cancelButtonColor: "#6c757d",

                confirmButtonText: "Sí, registrar pago",

                cancelButtonText: "Cancelar"

            }).then(function (resultado) {

                if (resultado.isConfirmed) {

                    formPagar.submit();

                }

            });

        });

    }


    // ==========================================
    // CONFIRMAR DESCUENTO
    // ==========================================

    const formDescuento = document.getElementById("formDescuento");

    if (formDescuento) {

        formDescuento.addEventListener("submit", function (evento) {

            evento.preventDefault();

            // Validar los campos del formulario.
            if (!formDescuento.reportValidity()) {
                return;
            }

            const porcentaje = document.getElementById(
                "porcentaje"
            ).value;

            Swal.fire({

                title: "¿Aplicar descuento?",

                text: `Se aplicará un descuento del ${porcentaje}%.`,

                icon: "question",

                showCancelButton: true,

                confirmButtonColor: "#0066ff",

                cancelButtonText: "Cancelar",

                confirmButtonText: "Sí, aplicar"

            }).then(function (resultado) {

                if (resultado.isConfirmed) {

                    formDescuento.submit();

                }

            });

        });

    }


    // ==========================================
    // CONFIRMAR ELIMINACIÓN
    // ==========================================

    const formEliminar = document.getElementById(
        "formEliminarDetalle"
    );

    if (formEliminar) {

        formEliminar.addEventListener("submit", function (evento) {

            evento.preventDefault();

            Swal.fire({

                title: "¿Eliminar esta factura?",

                text: "La factura y su historial serán eliminados.",

                icon: "warning",

                showCancelButton: true,

                confirmButtonColor: "#dc3545",

                cancelButtonColor: "#6c757d",

                confirmButtonText: "Sí, eliminar",

                cancelButtonText: "Cancelar"

            }).then(function (resultado) {

                if (resultado.isConfirmed) {

                    formEliminar.submit();

                }

            });

        });

    }

});
    document.addEventListener("DOMContentLoaded", function () {

        // Obtener todos los formularios de eliminación.
        const formularios = document.querySelectorAll(
            ".form-eliminar"
        );

        formularios.forEach(function (formulario) {

            formulario.addEventListener("submit", function (evento) {

                // Evitar eliminar inmediatamente.
                evento.preventDefault();

                // Guardar el formulario seleccionado.
                const formularioActual = this;

                // Mostrar confirmación con SweetAlert2.
                Swal.fire({

                    title: "¿Eliminar factura?",

                    text: "Esta acción no se puede deshacer.",

                    icon: "warning",

                    showCancelButton: true,

                    confirmButtonColor: "#dc3545",

                    cancelButtonColor: "#6c757d",

                    confirmButtonText: "Sí, eliminar",

                    cancelButtonText: "Cancelar"

                }).then(function (resultado) {

                    // Enviar el formulario solamente
                    // si el usuario confirma.
                    if (resultado.isConfirmed) {

                        formularioActual.submit();

                    }

                });

            });

        });

    });
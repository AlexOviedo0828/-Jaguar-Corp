# Importamos datetime para trabajar con fechas y horas.
from datetime import datetime
# Importamos las herramientas de Flask que necesita nuestra aplicación web.
from flask import (

    Flask,             # Permite crear nuestra aplicación web.

    abort,             # Muestra un error HTTP, por ejemplo 404,
                        # cuando una factura no existe.

    flash,             # Guarda mensajes temporales de éxito o error
                        # para mostrarlos al usuario.

    redirect,          # Redirige al usuario hacia otra página.

    render_template,   # Permite mostrar nuestros archivos HTML
                        # y enviarles información desde Python.

    request,           # Permite recibir los datos enviados por el usuario,
                        # como formularios, búsquedas y filtros.

    url_for,           # Genera la dirección de una página utilizando
                        # el nombre de su función en Flask.
)


# Importamos nuestra clase Factura_Cliente.
from factura_cliente import Factura_Cliente

# 1. CONFIGURACIÓN DE FLASK

# Creamos la aplicación web utilizando Flask.
# __name__ permite identificar el archivo principal.
app = Flask(__name__)

# Esta clave permite utilizar los mensajes flash.

app.secret_key = "jaguar-corp-prototipo"

# 2. ALMACENAMIENTO TEMPORAL

# Creamos un diccionario vacío para guardar las facturas.
# Cada factura se identifica por su número.
facturas_registradas = {}

# Este diccionario guarda las actividades realizadas
# sobre cada factura, como creación, descuentos y pagos.
historial_facturas = {}

# Número que se asignará a la próxima factura.
# La primera factura comenzará con el número 1001.
siguiente_numero_factura = 1001

# 3. REGISTRAR ACTIVIDADES

def registrar_historial(numero, accion, detalle):
    # Comprobamos si la factura tiene un historial.
    # Si no existe, creamos una lista vacía.
    if numero not in historial_facturas:
        historial_facturas[numero] = []

    # Agregamos una nueva actividad al historial.
    historial_facturas[numero].append({

        # datetime.now() obtiene la fecha y hora actual.
        # strftime() permite mostrarla con el formato indicado.
        "fecha": datetime.now().strftime("%d-%m-%Y %H:%M"),

        "accion": accion,
        "detalle": detalle
    })

# 4. CONVERTIR FECHAS

def convertir_fecha(fecha_html):
    # strptime() interpreta el texto como una fecha.
    fecha = datetime.strptime(
        fecha_html,
        "%Y-%m-%d"
    )
    # strftime() convierte la fecha al formato que necesitamos.
    return fecha.strftime("%d-%m-%Y")

# 5. PÁGINA PRINCIPAL

# Esta ruta corresponde a la página de inicio.
@app.route("/")
def inicio():
    """
    Muestra la página principal con las estadísticas
    de las facturas registradas.
    """
    # values() obtiene todas las facturas del diccionario.
    # list() convierte esos valores en una lista.
    facturas = list(facturas_registradas.values())

    # Creamos un diccionario con las estadísticas.
    estadisticas = {

        # len() cuenta cuántas facturas tenemos.
        "total_facturas": len(facturas),

        # sum() suma los montos de todas las facturas.
        "monto_total": sum(
            factura.get_monto()
            for factura in facturas
        ),

        # Contamos las facturas que están pendientes.
        "pendientes": sum(
            factura.get_estado_pago() == "Pendiente"
            for factura in facturas
        ),

        # Contamos las facturas que están pagadas.
        "pagadas": sum(
            factura.get_estado_pago() == "Pagado"
            for factura in facturas
        )
    }

    # Mostramos index.html y enviamos las estadísticas.
    return render_template(
        "index.html",
        estadisticas=estadisticas
    )

# 6. CREAR UNA NUEVA FACTURA

# GET permite mostrar el formulario.
# POST permite recibir los datos enviados por el usuario.
@app.route("/nueva-factura", methods=["GET", "POST"])
def nueva_factura():
    # global permite modificar esta variable
    # que fue creada fuera de la función.
    global siguiente_numero_factura

    # Comprobamos si el usuario envió el formulario.
    if request.method == "POST":

        # try permite intentar ejecutar el código.
        # Si ocurre un error, se controla con except.
        try:
            # Obtenemos el nombre del cliente.
            # get() obtiene el dato del formulario.
            # strip() elimina espacios al inicio y al final.
            cliente = request.form.get("cliente", "").strip()

            # Obtenemos el monto ingresado.
            # float() lo convierte en un número decimal.
            monto = float(
                request.form.get("monto", "")
            )

            # Obtenemos la fecha y la convertimos.
            fecha = convertir_fecha(
                request.form.get("fecha", "")
            )

            # Obtenemos el estado de pago.
            # Si no viene informado, usamos Pendiente.
            estado = request.form.get(
                "estado_pago",
                "Pendiente"
            )

            # Asignamos el próximo número disponible.
            numero = siguiente_numero_factura

            # Creamos un objeto de nuestra clase.
            # La clase valida los datos recibidos.
            factura = Factura_Cliente(
                cliente=cliente,
                numero_factura=numero,
                monto=monto,
                fecha=fecha,
                estado_pago=estado
            )

            # Guardamos la factura en el diccionario.
            # Utilizamos su número como clave.
            facturas_registradas[numero] = factura

            # Registramos la creación de la factura.
            registrar_historial(
                numero,
                "Creación",
                "Factura registrada correctamente."
            )

            # Aumentamos el número para la siguiente factura.
            siguiente_numero_factura += 1

            # flash() prepara un mensaje de confirmación.
            flash(
                f"Factura #{numero} registrada correctamente.",
                "success"
            )

            # redirect() envía al usuario a otra página.
            # url_for() construye la dirección de esa página.
            return redirect(
                url_for(
                    "detalle_factura",
                    numero=numero
                )
            )

        # Si los datos tienen errores, mostramos el mensaje.
        except (ValueError, TypeError) as error:
            flash(str(error), "error")

    # Mostramos el formulario y el próximo número disponible.
    return render_template(
        "nueva_factura.html",
        siguiente_numero=siguiente_numero_factura
    )

# 7. LISTADO DE FACTURAS

@app.route("/facturas")
def facturas():
    # request.args obtiene los datos enviados en la URL.
    # strip() elimina espacios innecesarios.
    # lower() convierte el texto a minúsculas.
    busqueda = request.args.get(
        "buscar",
        ""
    ).strip().lower()
    # Obtenemos el estado seleccionado en el filtro.
    estado = request.args.get(
        "estado",
        ""
    ).strip()
    # Convertimos las facturas guardadas en una lista.
    listado = list(facturas_registradas.values())
    # Si el usuario escribió algo en el buscador,
    # filtramos las facturas que coincidan.
    if busqueda:

        listado = [
            factura
            for factura in listado
            if (
                # Buscamos coincidencias en el nombre del cliente.
                busqueda in factura.get_cliente().lower()

                or

                # También buscamos por número de factura.
                # str() convierte el número en texto.
                busqueda in str(
                    factura.get_numero_factura()
                )
            )
        ]

    # Si el estado es válido, aplicamos el filtro.
    if estado in ("Pendiente", "Pagado"):

        listado = [
            factura
            for factura in listado
            if factura.get_estado_pago() == estado
        ]

    # sort() ordena la lista.
    # reverse=True muestra primero los números más altos.
    listado.sort(
        key=lambda factura: factura.get_numero_factura(),
        reverse=True
    )

    # Enviamos las facturas y los filtros al HTML.
    return render_template(
        "facturas.html",
        facturas=listado,
        busqueda=busqueda,
        estado=estado
    )


# 8. DETALLE DE UNA FACTURA


# <int:numero> indica que la URL recibe un número entero.
@app.route("/factura/<int:numero>")
def detalle_factura(numero):

    # Buscamos la factura utilizando su número.
    factura = facturas_registradas.get(numero)

    # Si la factura no existe, mostramos el error 404.
    if factura is None:
        abort(404)

    # Obtenemos su historial.
    # Si no tiene actividades, utilizamos una lista vacía.
    historial = historial_facturas.get(
        numero,
        []
    )

    # reversed() invierte el orden del historial.
    # Así mostramos primero las actividades recientes.
    return render_template(
        "detalle_factura.html",
        factura=factura,
        historial=list(reversed(historial))
    )
# 9. APLICAR DESCUENTO

# Esta ruta recibe los descuentos mediante POST.
@app.route(
    "/factura/<int:numero>/descuento",
    methods=["POST"]
)
def aplicar_descuento(numero):

    # Buscamos la factura que recibirá el descuento.
    factura = facturas_registradas.get(numero)

    # Si no existe, mostramos el error 404.
    if factura is None:
        abort(404)

    try:
        # Obtenemos el porcentaje desde el formulario.
        # float() lo convierte en un número decimal.
        porcentaje = float(
            request.form.get(
                "porcentaje",
                ""
            )
        )
        # Guardamos el monto antes del descuento.
        monto_anterior = factura.get_monto()

        # Utilizamos el método de nuestra clase
        # para intentar aplicar el descuento.
        resultado = factura.aplicar_descuento(
            porcentaje
        )
        # Si el método devuelve False,
        # significa que no se aplicó el descuento.
        if not resultado:
            raise ValueError(
                "El descuento debe estar entre 0 y 100 %."
            )

        # Consultamos el monto después del descuento.
        monto_nuevo = factura.get_monto()

        # Calculamos cuánto dinero se descontó.
        descuento = monto_anterior - monto_nuevo

        # Guardamos la actividad en el historial.
        registrar_historial(
            numero,
            "Descuento",
            (
                f"Descuento del {porcentaje:g}% aplicado. "
                f"Rebaja: ${descuento:,.2f}."
            )
        )

        # Informamos que el descuento fue aplicado.
        flash(
            "Descuento aplicado correctamente.",
            "success"
        )

    # Controlamos los errores en el porcentaje.
    except (ValueError, TypeError) as error:
        flash(
            str(error),
            "error"
        )

    # Regresamos a la página de detalle.
    return redirect(
        url_for(
            "detalle_factura",
            numero=numero
        )
    )

# 10. MARCAR FACTURA COMO PAGADA

@app.route(
    "/factura/<int:numero>/pagar",
    methods=["POST"]
)
def marcar_pagado(numero):
    

    # Buscamos la factura correspondiente.
    factura = facturas_registradas.get(numero)

    # Si no existe, mostramos el error 404.
    if factura is None:
        abort(404)

    # Comprobamos si la factura ya fue pagada.
    if factura.get_estado_pago() == "Pagado":

        flash(
            "La factura ya está pagada.",
            "error"
        )

    # Intentamos registrar el pago utilizando
    # el método marcar_pagado() de nuestra clase.
    elif factura.marcar_pagado():

        # Si el pago fue válido, registramos la actividad.
        registrar_historial(
            numero,
            "Pago",
            "Factura marcada como pagada."
        )

        flash(
            "Factura marcada como pagada.",
            "success"
        )

    # Si el monto es cero, el pago no se registra.
    else:

        flash(
            "No se puede pagar una factura con monto cero.",
            "error"
        )

    # Regresamos al detalle de la factura.
    return redirect(
        url_for(
            "detalle_factura",
            numero=numero
        )
    )

# 11. ELIMINAR FACTURA

@app.route(
    "/factura/<int:numero>/eliminar",
    methods=["POST"]
)
def eliminar_factura(numero):


    # Comprobamos que la factura exista.
    if numero not in facturas_registradas:
        abort(404)

    # del elimina la factura del diccionario.
    del facturas_registradas[numero]

    # pop() elimina el historial de la factura.
    # None evita un error si el historial no existe.
    historial_facturas.pop(
        numero,
        None
    )

    # Mostramos un mensaje de confirmación.
    flash(
        "Factura eliminada correctamente.",
        "success"
    )

    # Regresamos al listado de facturas.
    return redirect(
        url_for("facturas")
    )

# 12. EJECUTAR APLICACIÓN

# Esta condición comprueba si ejecutamos directamente app.py.
if __name__ == "__main__":

    # Iniciamos el servidor de Flask.
    # debug=True permite visualizar errores durante el desarrollo.
    app.run(debug=True)
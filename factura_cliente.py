# datetime permite trabajar con fechas.
from datetime import datetime

# isfinite permite comprobar que un número
# no sea infinito ni un valor NaN.
from math import isfinite

# 1. CREAR LA CLASE


# Esta clase representa una factura de nuestro sistema.
class Factura_Cliente:

    """
    Representa una factura de Jaguar Corp.

    Atributos:
        cliente: nombre del cliente.
        numero_factura: número de identificación.
        monto: valor de la factura.
        fecha: fecha de emisión.
        estado_pago: Pendiente o Pagado.
    """

    # 2. CONSTRUCTOR

    def __init__(
        self,
        cliente,
        numero_factura,
        monto=0.0,
        fecha="",
        estado_pago="Pendiente"
    ):
        """
        Se ejecuta cuando creamos una nueva factura.

        cliente y numero_factura son obligatorios.

        Los demás atributos son opcionales porque
        tienen valores predeterminados.
        """
        # Utilizamos los métodos SET para guardar
        # los datos y comprobar que sean válidos.
        self.set_cliente(cliente)
        self.set_numero_factura(numero_factura)
        self.set_monto(monto)
        self.set_fecha(fecha)
        self.set_estado_pago(estado_pago)

    # 3. MÉTODOS GET

    # Los métodos GET permiten consultar información.

    def get_cliente(self):
        """Devuelve el nombre del cliente."""
        return self.cliente

    def get_numero_factura(self):
        """Devuelve el número de factura."""
        return self.numero_factura

    def get_monto(self):
        """Devuelve el monto de la factura."""
        return self.monto

    def get_fecha(self):
        """Devuelve la fecha de la factura."""
        return self.fecha

    def get_estado_pago(self):
        """Devuelve el estado de pago."""
        return self.estado_pago

    # 4. MÉTODOS SET


    # Los métodos SET permiten modificar información.
    # También verifican que los datos sean correctos.

    def set_cliente(self, cliente):
        """Valida y modifica el nombre del cliente."""

        # isinstance() comprueba el tipo de dato.
        # En este caso, verificamos que sea texto.
        if not isinstance(cliente, str):
            raise TypeError(
                "El cliente debe ser un texto."
            )

        # strip() elimina los espacios innecesarios.
        # Si el nombre queda vacío, mostramos un error.
        if not cliente.strip():
            raise ValueError(
                "El nombre del cliente no puede estar vacío."
            )

        # Guardamos el nombre sin espacios adicionales.
        self.cliente = cliente.strip()

    def set_numero_factura(self, numero_factura):
        """Valida y modifica el número de factura."""

        # type() identifica el tipo de dato.
        # Comprobamos que sea un número entero.
        if type(numero_factura) is not int:
            raise TypeError(
                "El número de factura debe ser un entero."
            )

        # No permitimos números negativos ni cero.
        if numero_factura <= 0:
            raise ValueError(
                "El número de factura debe ser mayor que cero."
            )

        # Guardamos el número de factura.
        self.numero_factura = numero_factura

    def set_monto(self, monto):
        """Valida y modifica el monto de la factura."""

        # Rechazamos los valores True y False.
        # Aunque Python los considera relacionados
        # con los enteros, no representan montos.
        if isinstance(monto, bool):
            raise TypeError(
                "El monto debe ser un número."
            )

        # Verificamos que el monto sea numérico.
        if not isinstance(monto, (int, float)):
            raise TypeError(
                "El monto debe ser un número."
            )

        # isfinite() rechaza valores infinitos o NaN.
        if not isfinite(monto):
            raise ValueError(
                "El monto debe ser un número finito."
            )

        # No permitimos montos negativos.
        if monto < 0:
            raise ValueError(
                "El monto no puede ser negativo."
            )

        # float() convierte el monto a número decimal.
        self.monto = float(monto)

    def set_fecha(self, fecha):
        """Valida y modifica la fecha de la factura."""

        # Comprobamos que la fecha sea un texto.
        if not isinstance(fecha, str):
            raise TypeError(
                "La fecha debe ser un texto."
            )

        # Si el usuario no indica una fecha,
        # utilizamos automáticamente la fecha actual.
        if not fecha.strip():

            # now() obtiene la fecha actual.
            # strftime() permite darle el formato deseado.
            self.fecha = datetime.now().strftime(
                "%d-%m-%Y"
            )
            return

        # Intentamos convertir el texto en una fecha.
        try:
            fecha_validada = datetime.strptime(
                fecha.strip(),
                "%d-%m-%Y"
            )

        # Si la fecha es incorrecta, mostramos un error.
        except ValueError as error:
            raise ValueError(
                "La fecha debe tener formato DD-MM-AAAA "
                "y ser una fecha válida."
            ) from error

        # Guardamos la fecha con el formato correcto.
        self.fecha = fecha_validada.strftime(
            "%d-%m-%Y"
        )

    def set_estado_pago(self, estado_pago):
        """Valida y modifica el estado de pago."""

        # Comprobamos que el estado sea texto.
        if not isinstance(estado_pago, str):
            raise TypeError(
                "El estado de pago debe ser un texto."
            )

        # strip() elimina espacios.
        # capitalize() coloca la primera letra en mayúscula.
        estado_pago = estado_pago.strip().capitalize()

        # Solo aceptamos dos estados.
        if estado_pago not in ("Pendiente", "Pagado"):
            raise ValueError(
                "El estado debe ser Pendiente o Pagado."
            )

        # No permitimos marcar como pagada
        # una factura que tenga monto cero.
        if estado_pago == "Pagado" and self.monto <= 0:
            raise ValueError(
                "No se puede marcar como pagada "
                "una factura con monto cero."
            )

        # Guardamos el estado de pago.
        self.estado_pago = estado_pago

    # ==================================================
    # 5. APLICAR DESCUENTOS
    # ==================================================

    def aplicar_descuento(self, porcentaje):
        """
        Aplica un descuento al monto de la factura.

        Devuelve True si el descuento fue aplicado.
        Devuelve False si el descuento es inválido.
        """

        # No aceptamos valores booleanos.
        if isinstance(porcentaje, bool):
            return False

        # El porcentaje debe ser un número.
        if not isinstance(porcentaje, (int, float)):
            return False

        # Rechazamos valores infinitos o NaN.
        if not isfinite(porcentaje):
            return False

        # Solo permitimos descuentos entre 0 y 100.
        if not 0 <= porcentaje <= 100:
            return False

        # Calculamos cuánto dinero se descontará.
        descuento = self.monto * porcentaje / 100

        # Calculamos el monto después del descuento.
        nuevo_monto = self.monto - descuento

        # Si la factura ya está pagada,
        # no permitimos que su monto quede en cero.
        if self.estado_pago == "Pagado":
            if nuevo_monto <= 0:
                return False

        # Actualizamos el monto de la factura.
        self.monto = nuevo_monto

        # Indicamos que el descuento fue aplicado.
        return True

    # 6. MARCAR FACTURA COMO PAGADA

    def marcar_pagado(self):
        """
        Cambia el estado de una factura a Pagado.

        Solo permite registrar el pago cuando
        el monto de la factura es mayor que cero.
        """

        # Si el monto es cero, rechazamos el pago.
        if self.monto <= 0:
            return False

        # Cambiamos el estado de la factura.
        self.estado_pago = "Pagado"

        # Indicamos que la operación fue correcta.
        return True

    # 7. MOSTRAR FACTURA

    def mostrar_factura(self):
        """
        Devuelve un resumen de la factura
        en formato de texto.
        """

        # Formateamos el monto con dos decimales.
        monto_formateado = f"{self.monto:,.2f}"

        # Adaptamos los separadores al formato chileno:
        # punto para miles y coma para decimales.
        monto_formateado = (
            monto_formateado
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        # Creamos el texto con los datos de la factura.
        factura = (
            "\n====================================\n"
            "             JAGUAR CORP\n"
            "        SISTEMA DE FACTURACIÓN\n"
            "====================================\n"
            f"Número de factura: {self.numero_factura}\n"
            f"Cliente: {self.cliente}\n"
            f"Fecha: {self.fecha}\n"
            f"Monto: ${monto_formateado}\n"
            f"Estado de pago: {self.estado_pago}\n"
            "===================================="
        )

        # Devolvemos el resumen como una cadena de texto.
        return factura
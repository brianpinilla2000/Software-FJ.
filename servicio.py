
# ============================================
# GESTION DE SERVICIOS
# PROYECTO SOFTWARE FJ - UNAD
# ============================================

# Importamos ABC y abstractmethod para crear una clase abstracta.
from abc import ABC, abstractmethod

# Importamos la clase Entidad.
from entidades import Entidad

# Importamos las excepciones y funciones de registro.
from logs import (
    DatosInvalidosError,
    registrar_evento,
    registrar_error
)


# ============================================
# CLASE ABSTRACTA SERVICIO
# ============================================

class Servicio(Entidad, ABC):

    def __init__(self, identificador, nombre, tarifa):

        try:
            # Inicializamos la clase padre.
            super().__init__(identificador)

            # Validamos el nombre.
            if not isinstance(nombre, str) or not nombre.strip():
                raise DatosInvalidosError(
                    "El nombre del servicio es obligatorio."
                )

            # Validamos que la tarifa sea numérica y positiva.
            if (
                isinstance(tarifa, bool)
                or not isinstance(tarifa, (int, float))
                or tarifa <= 0
            ):
                raise DatosInvalidosError(
                    "La tarifa debe ser un numero mayor que cero."
                )

            # Guardamos los datos del servicio.
            self.nombre = nombre.strip()
            self.tarifa = float(tarifa)

            # Registramos el servicio creado.
            registrar_evento(
                f"Servicio creado correctamente: {self.nombre}"
            )

        except DatosInvalidosError as error:

            registrar_error(
                f"Error al crear servicio: {error}"
            )

            raise

        except Exception as error:

            registrar_error(
                f"Error inesperado al crear servicio: {error}"
            )

            raise DatosInvalidosError(
                "No fue posible crear el servicio."
            ) from error

    # Método abstracto para validar parámetros.
    @abstractmethod
    def validar_parametros(self):
        pass

    # Método abstracto para calcular costos.
    @abstractmethod
    def calcular_costo(
        self,
        cantidad=1,
        impuesto=0,
        descuento=0
    ):
        pass

    # Método auxiliar para calcular el costo final.
    def _calcular_total(self, cantidad, impuesto, descuento):

        self.validar_parametros()

        # Validamos la cantidad.
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
            or cantidad <= 0
        ):
            raise DatosInvalidosError(
                "La cantidad debe ser mayor que cero."
            )

        # Validamos el impuesto.
        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or impuesto < 0
            or impuesto > 100
        ):
            raise DatosInvalidosError(
                "El impuesto debe estar entre 0 y 100."
            )

        # Validamos el descuento.
        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or descuento < 0
            or descuento > 100
        ):
            raise DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )

        # Calculamos el subtotal.
        subtotal = self.tarifa * cantidad

        # Calculamos el descuento.
        valor_descuento = subtotal * (descuento / 100)

        # Calculamos el subtotal con descuento.
        subtotal_descuento = subtotal - valor_descuento

        # Calculamos el impuesto.
        valor_impuesto = subtotal_descuento * (impuesto / 100)

        # Calculamos el total.
        total = subtotal_descuento + valor_impuesto

        registrar_evento(
            f"Costo calculado para {self.nombre}: ${total:,.2f}"
        )

        return total


# ============================================
# CLASE SALA
# ============================================

class Sala(Servicio):

    def validar_parametros(self):

        if self.tarifa <= 0:
            raise DatosInvalidosError(
                "La tarifa de la sala debe ser positiva."
            )

    def calcular_costo(
        self,
        cantidad=1,
        impuesto=0,
        descuento=0
    ):

        try:
            return self._calcular_total(
                cantidad,
                impuesto,
                descuento
            )

        except Exception as error:

            registrar_error(
                f"Error al calcular costo de sala: {error}"
            )

            raise

    def describir(self):

        return (
            f"Sala: {self.nombre} | "
            f"Tarifa: ${self.tarifa:,.2f}"
        )


# ============================================
# CLASE EQUIPO
# ============================================

class Equipo(Servicio):

    def validar_parametros(self):

        if self.tarifa <= 0:
            raise DatosInvalidosError(
                "La tarifa del equipo debe ser positiva."
            )

    def calcular_costo(
        self,
        cantidad=1,
        impuesto=0,
        descuento=0
    ):

        try:
            return self._calcular_total(
                cantidad,
                impuesto,
                descuento
            )

        except Exception as error:

            registrar_error(
                f"Error al calcular costo de equipo: {error}"
            )

            raise

    def describir(self):

        return (
            f"Equipo: {self.nombre} | "
            f"Tarifa: ${self.tarifa:,.2f}"
        )


# ============================================
# CLASE ASESORIA
# ============================================

class Asesoria(Servicio):

    def validar_parametros(self):

        if self.tarifa <= 0:
            raise DatosInvalidosError(
                "La tarifa de la asesoria debe ser positiva."
            )

    def calcular_costo(
        self,
        cantidad=1,
        impuesto=0,
        descuento=0
    ):

        try:
            return self._calcular_total(
                cantidad,
                impuesto,
                descuento
            )

        except Exception as error:

            registrar_error(
                f"Error al calcular costo de asesoria: {error}"
            )

            raise

    def describir(self):

        return (
            f"Asesoria: {self.nombre} | "
            f"Tarifa: ${self.tarifa:,.2f}"
        )

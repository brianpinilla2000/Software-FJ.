
# ============================================
# GESTION DE RESERVAS
# PROYECTO SOFTWARE FJ - UNAD
# ============================================

from entidades import Entidad
from datetime import datetime

from logs import (
    DatosInvalidosError,
    ReservaError,
    OperacionNoPermitidaError,
    registrar_evento,
    registrar_error
)


# ============================================
# CLASE RESERVA
# ============================================

class Reserva(Entidad):

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        fecha,
        hora,
        duracion=1
    ):

        try:
            super().__init__(identificador)

            if cliente is None:
                raise DatosInvalidosError(
                    "La reserva debe tener un cliente."
                )

            if servicio is None:
                raise DatosInvalidosError(
                    "La reserva debe tener un servicio."
                )

            if not isinstance(fecha, str) or not fecha.strip():
                raise DatosInvalidosError(
                    "La fecha es obligatoria."
                )

            if not isinstance(hora, str) or not hora.strip():
                raise DatosInvalidosError(
                    "La hora es obligatoria."
                )

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                datetime.strptime(hora, "%H:%M")

            except ValueError as error:
                raise DatosInvalidosError(
                    "La fecha o la hora tienen un formato invalido."
                ) from error

            if (
                isinstance(duracion, bool)
                or not isinstance(duracion, int)
                or duracion <= 0
            ):
                raise DatosInvalidosError(
                    "La duracion debe ser un numero entero mayor que cero."
                )

            self.cliente = cliente
            self.servicio = servicio
            self.fecha = fecha
            self.hora = hora
            self.duracion = duracion

            self.estado = "Pendiente"

            registrar_evento(
                f"Reserva {self.identificador} creada correctamente."
            )

        except (DatosInvalidosError, ValueError) as error:

            registrar_error(
                f"Error al crear reserva: {error}"
            )

            raise

        except Exception as error:

            registrar_error(
                f"Error inesperado al crear reserva: {error}"
            )

            raise ReservaError(
                "No fue posible crear la reserva."
            ) from error

    # ========================================
    # CONFIRMAR RESERVA
    # ========================================

    def confirmar(self):

        try:
            if self.estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "Solo se pueden confirmar reservas pendientes."
                )

            self.estado = "Confirmada"

            registrar_evento(
                f"Reserva {self.identificador} confirmada."
            )

            return "Reserva confirmada correctamente."

        except OperacionNoPermitidaError as error:

            registrar_error(
                f"Error al confirmar reserva: {error}"
            )

            raise

    # ========================================
    # CANCELAR RESERVA
    # ========================================

    def cancelar(self):

        try:
            if self.estado not in ("Pendiente", "Confirmada"):
                raise OperacionNoPermitidaError(
                    "No se puede cancelar una reserva procesada o cancelada."
                )

            self.estado = "Cancelada"

            registrar_evento(
                f"Reserva {self.identificador} cancelada."
            )

            return "Reserva cancelada correctamente."

        except OperacionNoPermitidaError as error:

            registrar_error(
                f"Error al cancelar reserva: {error}"
            )

            raise

    # ========================================
    # PROCESAR RESERVA
    # ========================================

    def procesar(self):

        try:
            if self.estado != "Confirmada":
                raise OperacionNoPermitidaError(
                    "La reserva debe estar confirmada para procesarse."
                )

            costo = self.servicio.calcular_costo(
                cantidad=self.duracion
            )

            self.estado = "Procesada"

            registrar_evento(
                f"Reserva {self.identificador} procesada. "
                f"Costo: ${costo:,.2f}"
            )

            return costo

        except OperacionNoPermitidaError as error:

            registrar_error(
                f"Error al procesar reserva: {error}"
            )

            raise

        except Exception as error:

            registrar_error(
                f"Error inesperado al procesar reserva: {error}"
            )

            raise ReservaError(
                "No fue posible procesar la reserva."
            ) from error

    # ========================================
    # DESCRIBIR RESERVA
    # ========================================

    def describir(self):

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Fecha: {self.fecha} | "
            f"Hora: {self.hora} | "
            f"Duracion: {self.duracion} | "
            f"Estado: {self.estado}"
        )

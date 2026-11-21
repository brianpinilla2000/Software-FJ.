
# ============================================
# CLASE SISTEMA DE GESTION
# PROYECTO SOFTWARE FJ - UNAD
# ============================================

from datetime import datetime, timedelta

from cliente import Cliente
from servicio import Servicio
from reserva import Reserva

from logs import (
    DatosInvalidosError,
    ReservaError,
    registrar_evento,
    registrar_error
)


class SistemaGestion:
    """
    Administra los clientes, servicios y reservas
    mediante listas internas.
    """

    def __init__(self):

        self._clientes = []
        self._servicios = []
        self._reservas = []

        registrar_evento(
            "Sistema de gestion creado correctamente."
        )

    # ========================================
    # PROPIEDADES DE CONSULTA
    # ========================================

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    # ========================================
    # REGISTRO DE CLIENTES
    # ========================================

    def registrar_cliente(self, cliente):

        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError(
                    "El objeto debe ser un cliente valido."
                )

            for existente in self._clientes:
                if existente.identificador == cliente.identificador:
                    raise DatosInvalidosError(
                        "Ya existe un cliente con ese identificador."
                    )

            self._clientes.append(cliente)

            registrar_evento(
                f"Cliente agregado al sistema: "
                f"{cliente.identificador}"
            )

            return "Cliente registrado correctamente."

        except Exception as error:
            registrar_error(
                f"Error al registrar cliente: {error}"
            )
            raise

    # ========================================
    # REGISTRO DE SERVICIOS
    # ========================================

    def registrar_servicio(self, servicio):

        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError(
                    "El objeto debe ser un servicio valido."
                )

            for existente in self._servicios:
                if existente.identificador == servicio.identificador:
                    raise DatosInvalidosError(
                        "Ya existe un servicio con ese identificador."
                    )

            self._servicios.append(servicio)

            registrar_evento(
                f"Servicio agregado al sistema: "
                f"{servicio.identificador}"
            )

            return "Servicio registrado correctamente."

        except Exception as error:
            registrar_error(
                f"Error al registrar servicio: {error}"
            )
            raise

    # ========================================
    # REGISTRO DE RESERVAS
    # ========================================

    def registrar_reserva(self, reserva):

        try:
            # Validar que sea una reserva.
            if not isinstance(reserva, Reserva):
                raise ReservaError(
                    "El objeto debe ser una reserva valida."
                )

            # Verificar que el cliente este registrado.
            if self.buscar_cliente(
                reserva.cliente.identificador
            ) is None:
                raise ReservaError(
                    "El cliente no esta registrado en el sistema."
                )

            # Verificar que el servicio este registrado.
            if self.buscar_servicio(
                reserva.servicio.identificador
            ) is None:
                raise ReservaError(
                    "El servicio no esta registrado en el sistema."
                )

            # Evitar identificadores duplicados.
            for existente in self._reservas:

                if existente.identificador == reserva.identificador:
                    raise ReservaError(
                        "Ya existe una reserva con ese identificador."
                    )

            # Calcular el horario de la nueva reserva.
            nuevo_inicio = datetime.strptime(
                f"{reserva.fecha} {reserva.hora}",
                "%Y-%m-%d %H:%M"
            )

            nuevo_final = nuevo_inicio + timedelta(
                hours=reserva.duracion
            )

            # Comprobar disponibilidad del servicio.
            for existente in self._reservas:

                # Las reservas canceladas no ocupan horario.
                if existente.estado == "Cancelada":
                    continue

                # Comparar reservas del mismo servicio.
                if (
                    existente.servicio.identificador
                    == reserva.servicio.identificador
                ):

                    existente_inicio = datetime.strptime(
                        f"{existente.fecha} {existente.hora}",
                        "%Y-%m-%d %H:%M"
                    )

                    existente_final = existente_inicio + timedelta(
                        hours=existente.duracion
                    )

                    # Detectar cruce de horarios.
                    if (
                        nuevo_inicio < existente_final
                        and existente_inicio < nuevo_final
                    ):
                        raise ReservaError(
                            "El servicio ya tiene una reserva "
                            "en ese horario."
                        )

            # Registrar la reserva cuando todo sea valido.
            self._reservas.append(reserva)

            registrar_evento(
                f"Reserva agregada al sistema: "
                f"{reserva.identificador}"
            )

            return "Reserva registrada correctamente."

        except Exception as error:

            registrar_error(
                f"Error al registrar reserva: {error}"
            )

            raise

    # ========================================
    # BUSQUEDA DE CLIENTES
    # ========================================

    def buscar_cliente(self, identificador):

        for cliente in self._clientes:
            if cliente.identificador == identificador:
                return cliente

        return None

    # ========================================
    # BUSQUEDA DE SERVICIOS
    # ========================================

    def buscar_servicio(self, identificador):

        for servicio in self._servicios:
            if servicio.identificador == identificador:
                return servicio

        return None

    # ========================================
    # BUSQUEDA DE RESERVAS
    # ========================================

    def buscar_reserva(self, identificador):

        for reserva in self._reservas:
            if reserva.identificador == identificador:
                return reserva

        return None

    # ========================================
    # CONSULTA GENERAL
    # ========================================

    def mostrar_resumen(self):

        print("\n========================================")
        print(" RESUMEN GENERAL DEL SISTEMA")
        print("========================================")

        print(f"Total de clientes: {len(self._clientes)}")
        print(f"Total de servicios: {len(self._servicios)}")
        print(f"Total de reservas: {len(self._reservas)}")

        print("\nCLIENTES:")
        for cliente in self._clientes:
            print(cliente.describir())

        print("\nSERVICIOS:")
        for servicio in self._servicios:
            print(servicio.describir())

        print("\nRESERVAS:")
        for reserva in self._reservas:
            print(reserva.describir())

        print("========================================")

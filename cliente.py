
# ============================================
# CLASE CLIENTE
# PROYECTO SOFTWARE FJ - UNAD
# ============================================

# Importamos la clase abstracta Entidad.
from entidades import Entidad

# Importamos la excepción personalizada y las funciones de registro.
from logs import DatosInvalidosError, registrar_evento, registrar_error


class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):

        try:
            # Inicializamos los atributos heredados de Entidad.
            super().__init__(identificador)

            # Validamos que el nombre sea correcto.
            if not isinstance(nombre, str) or not nombre.strip():
                raise DatosInvalidosError(
                    "El nombre del cliente es obligatorio."
                )

            # Validamos el correo electrónico.
            if (
                not isinstance(correo, str)
                or "@" not in correo
                or "." not in correo
            ):
                raise DatosInvalidosError(
                    "El correo electronico no es valido."
                )

            # Validamos el teléfono.
            if (
                not isinstance(telefono, str)
                or not telefono.isdigit()
            ):
                raise DatosInvalidosError(
                    "El telefono debe contener solamente numeros."
                )

            # Encapsulamos los datos personales.
            self._nombre = nombre.strip()
            self._correo = correo.strip()
            self._telefono = telefono.strip()

            # Registramos el evento exitoso.
            registrar_evento(
                f"Cliente registrado correctamente: {self._nombre}"
            )

        except DatosInvalidosError as error:

            # Registramos el error de validación.
            registrar_error(
                f"Error al registrar cliente: {error}"
            )

            # Propagamos la excepción personalizada.
            raise

        except Exception as error:

            # Registramos cualquier otro error inesperado.
            registrar_error(
                f"Error inesperado al crear cliente: {error}"
            )

            # Encadenamos la excepción original.
            raise DatosInvalidosError(
                "No fue posible registrar el cliente."
            ) from error

    # Propiedad para consultar el nombre.
    @property
    def nombre(self):
        return self._nombre

    # Propiedad para consultar el correo.
    @property
    def correo(self):
        return self._correo

    # Propiedad para consultar el teléfono.
    @property
    def telefono(self):
        return self._telefono

    # Método para describir el cliente.
    def describir(self):

        return (
            f"Cliente: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )

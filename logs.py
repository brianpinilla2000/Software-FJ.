
# Importamos el módulo logging para registrar eventos y errores.
import logging


# Configuramos el archivo donde se guardarán los registros.
logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# Excepción general del sistema Software FJ.
class ErrorSistema(Exception):
    pass


# Excepción para datos incorrectos.
class DatosInvalidosError(ErrorSistema):
    pass


# Excepción para servicios no disponibles.
class ServicioNoDisponibleError(ErrorSistema):
    pass


# Excepción para errores en las reservas.
class ReservaError(ErrorSistema):
    pass


# Excepción para operaciones no permitidas.
class OperacionNoPermitidaError(ErrorSistema):
    pass


# Función para registrar eventos importantes.
def registrar_evento(mensaje):
    logging.info(mensaje)


# Función para registrar errores.
def registrar_error(mensaje):
    logging.error(mensaje)


# Prueba del módulo de registros.
if __name__ == "__main__":

    registrar_evento("Sistema Software FJ iniciado correctamente.")

    registrar_error("Prueba del registro de errores.")

    print("Modulo de registros funcionando correctamente.")
    print("Archivo sistema.log actualizado.")

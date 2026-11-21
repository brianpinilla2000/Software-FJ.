
# ============================================
# PROYECTO SOFTWARE FJ
# CURSO: PROGRAMACION 213023
# UNAD - FASE 4
# ============================================

# Importacion de clases
from cliente import Cliente
from servicio import Sala, Equipo, Asesoria
from reserva import Reserva
from sistema import SistemaGestion

# Importacion de funciones de registro
from logs import (
    registrar_evento,
    registrar_error
)


def mostrar_presentacion():
    print("=" * 65)
    print(" SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print(" UNAD - PROGRAMACION 213023 - FASE 4")
    print("=" * 65)


def ejecutar_operacion(nombre, funcion):
    print("\n" + "-" * 65)
    print(nombre)
    print("-" * 65)

    try:
        resultado = funcion()

        if resultado is not None:
            print("Resultado:", resultado)

        print("Operacion ejecutada correctamente.")
        return resultado

    except Exception as error:
        print("Operacion controlada:", error)
        registrar_error(
            f"Operacion '{nombre}' controlada: {error}"
        )
        return None

    finally:
        print("Fin de la operacion.")


def ejecutar():

    mostrar_presentacion()

    sistema = SistemaGestion()

    # ========================================
    # 1. REGISTRO DE CLIENTE
    # ========================================

    cliente1 = ejecutar_operacion(
        "REGISTRO DE CLIENTE",
        lambda: Cliente(
            "C001",
            "Brayan Pinilla",
            "brayanpinilla2000@gmail.com",
            "3217568808"
        )
    )

    if cliente1 is not None:
        ejecutar_operacion(
            "INCORPORACION DEL CLIENTE AL SISTEMA",
            lambda: sistema.registrar_cliente(cliente1)
        )

    # ========================================
    # 2. REGISTRO DE SERVICIOS
    # ========================================

    sala1 = ejecutar_operacion(
        "CREACION DEL SERVICIO SALA",
        lambda: Sala(
            "S001",
            "Sala de reuniones",
            80000
        )
    )

    equipo1 = ejecutar_operacion(
        "CREACION DEL SERVICIO EQUIPO",
        lambda: Equipo(
            "E001",
            "Video Beam",
            50000
        )
    )

    asesoria1 = ejecutar_operacion(
        "CREACION DEL SERVICIO ASESORIA",
        lambda: Asesoria(
            "A001",
            "Asesoria tecnica",
            60000
        )
    )

    for servicio in (sala1, equipo1, asesoria1):
        if servicio is not None:
            ejecutar_operacion(
                f"REGISTRO DEL SERVICIO {servicio.identificador}",
                lambda servicio=servicio:
                    sistema.registrar_servicio(servicio)
            )

    # ========================================
    # 3. PRUEBA DE CLIENTE INVALIDO
    # ========================================

    ejecutar_operacion(
        "PRUEBA DE REGISTRO DE CLIENTE INVALIDO",
        lambda: Cliente(
            "C002",
            "",
            "correo_invalido",
            "123"
        )
    )

    # ========================================
    # 4. PRUEBA DE SERVICIO CON TARIFA INVALIDA
    # ========================================

    ejecutar_operacion(
        "PRUEBA DE SERVICIO CON TARIFA INVALIDA",
        lambda: Sala(
            "S002",
            "Sala de prueba",
            -50000
        )
    )

    # ========================================
    # 5. CREACION Y REGISTRO DE RESERVA
    # ========================================

    reserva1 = None

    if cliente1 is not None and sala1 is not None:

        reserva1 = ejecutar_operacion(
            "CREACION DE RESERVA R001",
            lambda: Reserva(
                "R001",
                cliente1,
                sala1,
                "2026-11-20",
                "09:00",
                1
            )
        )

        if reserva1 is not None:
            ejecutar_operacion(
                "REGISTRO DE RESERVA R001",
                lambda: sistema.registrar_reserva(reserva1)
            )

    # ========================================
    # 6. PRUEBA DE RESERVA CON HORARIO CRUZADO
    # ========================================

    if cliente1 is not None and sala1 is not None:

        reserva_cruzada = ejecutar_operacion(
            "CREACION DE RESERVA CON HORARIO CRUZADO",
            lambda: Reserva(
                "R004",
                cliente1,
                sala1,
                "2026-11-20",
                "09:30",
                1
            )
        )

        if reserva_cruzada is not None:
            ejecutar_operacion(
                "PRUEBA DE CONTROL DE DISPONIBILIDAD",
                lambda: sistema.registrar_reserva(
                    reserva_cruzada
                )
            )

    # ========================================
    # 7. PRUEBA DE RESERVA INVALIDA
    # ========================================

    ejecutar_operacion(
        "PRUEBA DE CREACION DE RESERVA INVALIDA",
        lambda: Reserva(
            "R002",
            cliente1,
            sala1,
            "fecha_incorrecta",
            "hora_incorrecta",
            0
        )
    )

    # ========================================
    # 8. CONFIRMACION DE RESERVA
    # ========================================

    if reserva1 is not None:
        ejecutar_operacion(
            "CONFIRMACION DE RESERVA R001",
            lambda: reserva1.confirmar()
        )

    # ========================================
    # 9. PROCESAMIENTO DE RESERVA
    # ========================================

    if reserva1 is not None:
        ejecutar_operacion(
            "PROCESAMIENTO DE RESERVA R001",
            lambda: reserva1.procesar()
        )

    # ========================================
    # 10. CALCULO DE COSTO CON IMPUESTO
    # Y DESCUENTO
    # ========================================

    if sala1 is not None:
        ejecutar_operacion(
            "CALCULO DE COSTO CON IMPUESTO Y DESCUENTO",
            lambda: sala1.calcular_costo(
                cantidad=2,
                impuesto=19,
                descuento=10
            )
        )

    # ========================================
    # 11. CREACION DE RESERVA PARA EQUIPO
    # ========================================

    reserva3 = None

    if cliente1 is not None and equipo1 is not None:

        reserva3 = ejecutar_operacion(
            "CREACION DE RESERVA R003",
            lambda: Reserva(
                "R003",
                cliente1,
                equipo1,
                "2026-11-21",
                "10:00",
                1
            )
        )

        if reserva3 is not None:
            ejecutar_operacion(
                "REGISTRO DE RESERVA R003",
                lambda: sistema.registrar_reserva(reserva3)
            )

    # ========================================
    # 12. CANCELACION DE RESERVA
    # ========================================

    if reserva3 is not None:
        ejecutar_operacion(
            "CANCELACION DE RESERVA R003",
            lambda: reserva3.cancelar()
        )

    # ========================================
    # 13. INTENTO DE PROCESAR RESERVA CANCELADA
    # ========================================

    if reserva3 is not None:
        ejecutar_operacion(
            "PRUEBA DE PROCESAMIENTO DE RESERVA CANCELADA",
            lambda: reserva3.procesar()
        )

    # ========================================
    # 14. BUSQUEDA DE CLIENTE
    # ========================================

    ejecutar_operacion(
        "BUSQUEDA DE CLIENTE C001",
        lambda: sistema.buscar_cliente("C001")
    )

    # ========================================
    # 15. BUSQUEDA DE SERVICIO
    # ========================================

    ejecutar_operacion(
        "BUSQUEDA DE SERVICIO S001",
        lambda: sistema.buscar_servicio("S001")
    )

    # ========================================
    # 16. BUSQUEDA DE RESERVA
    # ========================================

    ejecutar_operacion(
        "BUSQUEDA DE RESERVA R001",
        lambda: sistema.buscar_reserva("R001")
    )

    # ========================================
    # 17. PRUEBA DE CLIENTE DUPLICADO
    # ========================================

    if cliente1 is not None:
        cliente_duplicado = ejecutar_operacion(
            "CREACION DE CLIENTE DUPLICADO",
            lambda: Cliente(
                "C001",
                "Cliente duplicado",
                "duplicado@correo.com",
                "3001234567"
            )
        )

        if cliente_duplicado is not None:
            ejecutar_operacion(
                "PRUEBA DE REGISTRO DE CLIENTE DUPLICADO",
                lambda: sistema.registrar_cliente(
                    cliente_duplicado
                )
            )

    # ========================================
    # 18. RESUMEN GENERAL DEL SISTEMA
    # ========================================

    ejecutar_operacion(
        "RESUMEN GENERAL DEL SISTEMA",
        lambda: sistema.mostrar_resumen()
    )

    registrar_evento(
        "Ejecucion del sistema Software FJ finalizada."
    )

    print("\n" + "=" * 65)
    print(" FIN DE LAS OPERACIONES DE PRUEBA")
    print(" SISTEMA SOFTWARE FJ")
    print("=" * 65)


if __name__ == "__main__":

    try:
        ejecutar()

    except Exception as error:
        print("Error general del sistema:", error)
        registrar_error(
            f"Error general durante la ejecucion: {error}"
        )

    finally:
        print("\nPrograma finalizado.")

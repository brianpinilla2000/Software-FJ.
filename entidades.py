
# ============================================
# CLASE ABSTRACTA ENTIDAD
# PROYECTO SOFTWARE FJ - UNAD
# ============================================

from abc import ABC, abstractmethod


class Entidad(ABC):

    def __init__(self, identificador):

        if not identificador:
            raise ValueError(
                "El identificador es obligatorio."
            )

        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        pass

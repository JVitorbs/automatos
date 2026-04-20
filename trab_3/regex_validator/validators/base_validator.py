from abc import ABC, abstractmethod
from typing import Dict


class BaseValidator(ABC):
    """Classe base para padronizar o retorno dos validadores."""

    @abstractmethod
    def validate(self, value: str) -> Dict[str, object]:
        """Valida o valor e retorna um payload estruturado."""
        raise NotImplementedError

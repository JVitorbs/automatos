import re
from typing import Dict

from utils.regex_patterns import SENHA_FORTE_PATTERN
from validators.base_validator import BaseValidator


class SenhaValidator(BaseValidator):
    def validate(self, value: str) -> Dict[str, object]:
        if not isinstance(value, str):
            return {
                "valid": False,
                "message": "Senha deve ser texto.",
                "value": value,
            }

        senha = value.strip()
        if not senha:
            return {
                "valid": False,
                "message": "Senha nao pode ser vazia.",
                "value": value,
            }

        if re.fullmatch(SENHA_FORTE_PATTERN, senha):
            return {
                "valid": True,
                "message": "Senha forte valida.",
                "value": value,
            }

        return {
            "valid": False,
            "message": (
                "Senha invalida. Requisitos: minimo 8 caracteres, "
                "1 letra maiuscula, 1 minuscula, 1 numero e 1 simbolo."
            ),
            "value": value,
        }

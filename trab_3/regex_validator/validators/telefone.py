import re
from typing import Dict

from utils.regex_patterns import TELEFONE_PATTERN
from validators.base_validator import BaseValidator


class TelefoneValidator(BaseValidator):
    def validate(self, value: str) -> Dict[str, object]:
        if not isinstance(value, str):
            return {
                "valid": False,
                "message": "Telefone deve ser texto.",
                "value": value,
            }

        telefone = value.strip()
        if not telefone:
            return {
                "valid": False,
                "message": "Telefone nao pode ser vazio.",
                "value": value,
            }

        if not re.fullmatch(TELEFONE_PATTERN, telefone):
            return {
                "valid": False,
                "message": "Telefone invalido. Use (DD) 99999-9999 ou (DD) 9999-9999.",
                "value": value,
            }

        ddd = telefone[1:3]
        if ddd.startswith("0"):
            return {
                "valid": False,
                "message": "Telefone invalido. DDD nao pode iniciar com 0.",
                "value": value,
            }

        return {
            "valid": True,
            "message": "Telefone valido.",
            "value": value,
            "normalized": telefone,
        }

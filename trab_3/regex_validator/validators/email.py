import re
from typing import Dict

from utils.regex_patterns import EMAIL_PATTERN
from validators.base_validator import BaseValidator


class EmailValidator(BaseValidator):
    def validate(self, value: str) -> Dict[str, object]:
        if not isinstance(value, str):
            return {
                "valid": False,
                "message": "Email deve ser texto.",
                "value": value,
            }

        email = value.strip()
        if not email:
            return {
                "valid": False,
                "message": "Email nao pode ser vazio.",
                "value": value,
            }

        if re.fullmatch(EMAIL_PATTERN, email):
            return {
                "valid": True,
                "message": "Email valido.",
                "value": value,
                "normalized": email,
            }

        return {
            "valid": False,
            "message": "Email invalido. Use o formato usuario@dominio.tld.",
            "value": value,
        }

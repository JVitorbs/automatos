import re
from typing import Dict

from utils.regex_patterns import CPF_PATTERN_DIGITS, CPF_PATTERN_MASKED
from validators.base_validator import BaseValidator


class CPFValidator(BaseValidator):
    def validate(self, value: str) -> Dict[str, object]:
        if not isinstance(value, str):
            return {
                "valid": False,
                "message": "CPF deve ser texto.",
                "value": value,
            }

        raw = value.strip()
        if not raw:
            return {
                "valid": False,
                "message": "CPF nao pode ser vazio.",
                "value": value,
            }

        if not re.fullmatch(CPF_PATTERN_MASKED, raw) and not re.fullmatch(CPF_PATTERN_DIGITS, raw):
            return {
                "valid": False,
                "message": "CPF invalido. Use 000.000.000-00 ou 00000000000.",
                "value": value,
            }

        digits = self._only_digits(raw)

        if len(set(digits)) == 1:
            return {
                "valid": False,
                "message": "CPF invalido. Sequencia repetida nao e permitida.",
                "value": value,
                "normalized": digits,
            }

        if self._is_valid_cpf_digits(digits):
            return {
                "valid": True,
                "message": "CPF valido.",
                "value": value,
                "normalized": digits,
            }

        return {
            "valid": False,
            "message": "CPF invalido. Digitos verificadores nao conferem.",
            "value": value,
            "normalized": digits,
        }

    @staticmethod
    def _only_digits(value: str) -> str:
        return re.sub(r"\D", "", value)

    @staticmethod
    def _is_valid_cpf_digits(cpf_digits: str) -> bool:
        if len(cpf_digits) != 11:
            return False

        first_check = CPFValidator._calc_check_digit(cpf_digits[:9], start_weight=10)
        second_check = CPFValidator._calc_check_digit(cpf_digits[:10], start_weight=11)
        return cpf_digits[-2:] == f"{first_check}{second_check}"

    @staticmethod
    def _calc_check_digit(base: str, start_weight: int) -> int:
        total = 0
        weight = start_weight
        for digit_char in base:
            total += int(digit_char) * weight
            weight -= 1

        mod = total % 11
        return 0 if mod < 2 else 11 - mod

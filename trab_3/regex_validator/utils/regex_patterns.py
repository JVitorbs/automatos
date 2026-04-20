"""Padroes de expressoes regulares usados pelos validadores."""

# Email basico: usuario@dominio.tld
EMAIL_PATTERN = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"

# CPF com mascara 000.000.000-00 ou somente numeros 00000000000
CPF_PATTERN_MASKED = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
CPF_PATTERN_DIGITS = r"^\d{11}$"

# Telefone BR: (DD) 99999-9999 ou (DD) 9999-9999
TELEFONE_PATTERN = r"^\(\d{2}\)\s\d{4,5}-\d{4}$"

# Senha forte: 8+ chars, 1 maiuscula, 1 minuscula, 1 digito, 1 simbolo
SENHA_FORTE_PATTERN = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{8,}$"

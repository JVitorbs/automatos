from pathlib import Path

from services.validator_service import ValidatorService
from validators import CPFValidator, EmailValidator, SenhaValidator, TelefoneValidator


def test_email_valido() -> None:
    result = EmailValidator().validate("teste.email+ok@ufrn.br")
    assert result["valid"] is True


def test_email_invalido() -> None:
    result = EmailValidator().validate("teste.email@")
    assert result["valid"] is False


def test_cpf_valido_com_mascara() -> None:
    result = CPFValidator().validate("529.982.247-25")
    assert result["valid"] is True


def test_cpf_valido_sem_mascara() -> None:
    result = CPFValidator().validate("52998224725")
    assert result["valid"] is True


def test_cpf_invalido_digitos_verificadores() -> None:
    result = CPFValidator().validate("529.982.247-26")
    assert result["valid"] is False
    assert "Digitos verificadores" in result["message"]


def test_cpf_invalido_sequencia_repetida() -> None:
    result = CPFValidator().validate("111.111.111-11")
    assert result["valid"] is False


def test_telefone_valido_com_9_digitos() -> None:
    result = TelefoneValidator().validate("(84) 99999-9999")
    assert result["valid"] is True


def test_telefone_valido_com_8_digitos() -> None:
    result = TelefoneValidator().validate("(84) 3333-2222")
    assert result["valid"] is True


def test_telefone_invalido_ddd_zero() -> None:
    result = TelefoneValidator().validate("(04) 99999-9999")
    assert result["valid"] is False


def test_senha_forte_valida() -> None:
    result = SenhaValidator().validate("Senha@123")
    assert result["valid"] is True


def test_senha_forte_invalida() -> None:
    result = SenhaValidator().validate("senha123")
    assert result["valid"] is False


def test_service_tipo_invalido_persistido(tmp_path: Path) -> None:
    service = ValidatorService(storage_dir=tmp_path, log_file=tmp_path / "validation.log")
    result = service.validate("cnpj", "123", persist=True)

    assert result["valid"] is False
    history = service.load_history()
    assert len(history) == 1
    assert history[0]["type"] == "cnpj"


def test_service_registra_historico_e_log(tmp_path: Path) -> None:
    log_file = tmp_path / "validation.log"
    service = ValidatorService(storage_dir=tmp_path, log_file=log_file)

    result = service.validate("email", "aluno@ufrn.br", persist=True)
    history = service.load_history()

    assert result["valid"] is True
    assert len(history) == 1
    assert log_file.exists()
    assert "Validacao tipo=email" in log_file.read_text(encoding="utf-8")


def test_exportacao_json(tmp_path: Path) -> None:
    service = ValidatorService(storage_dir=tmp_path, log_file=tmp_path / "validation.log")
    results = [
        service.validate("email", "dev@ufrn.br", persist=False),
        service.validate("senha", "Senha@123", persist=False),
    ]

    output_path = tmp_path / "saida" / "resultado.json"
    created = service.export_results(results, output_path)

    assert created == output_path
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "dev@ufrn.br" in content
    assert "Senha@123" in content

from pathlib import Path

from services.validator_service import ValidatorService


MENU_MAP = {
    "1": "email",
    "2": "cpf",
    "3": "telefone",
    "4": "senha",
}


def run_cli() -> None:
    service = ValidatorService()
    session_results = []

    print("\n=== Validador de Dados com RegEx ===")

    while True:
        print("\nEscolha uma opcao:")
        print("1 - Validar Email")
        print("2 - Validar CPF")
        print("3 - Validar Telefone")
        print("4 - Validar Senha Forte")
        print("5 - Ver historico recente")
        print("6 - Exportar resultados da sessao (JSON)")
        print("0 - Sair")

        choice = input("Opcao: ").strip()

        if choice == "0":
            print("Encerrando aplicacao.")
            break

        if choice in MENU_MAP:
            data_type = MENU_MAP[choice]
            value = input(f"Digite o valor para {data_type}: ")
            result = service.validate(data_type, value, persist=True)
            session_results.append(result)
            _print_result(result)
            continue

        if choice == "5":
            _show_recent_history(service)
            continue

        if choice == "6":
            _export_session_results(service, session_results)
            continue

        print("Opcao invalida. Tente novamente.")


def _print_result(result: dict) -> None:
    status = "VALIDO" if result.get("valid") else "INVALIDO"

    print("\n--- Resultado ---")
    print(f"Tipo: {result.get('type')}")
    print(f"Status: {status}")
    print(f"Mensagem: {result.get('message')}")
    print(f"Valor informado: {result.get('value')}")

    if "normalized" in result:
        print(f"Valor normalizado: {result.get('normalized')}")

    print(f"Data/hora: {result.get('timestamp')}")


def _show_recent_history(service: ValidatorService, limit: int = 5) -> None:
    history = service.load_history(limit=limit)
    if not history:
        print("Nenhum registro no historico.")
        return

    print(f"\n--- Ultimos {len(history)} registros ---")
    for item in history:
        print(
            f"[{item.get('timestamp')}] tipo={item.get('type')} "
            f"valid={item.get('valid')} valor={item.get('value')}"
        )


def _export_session_results(service: ValidatorService, session_results: list[dict]) -> None:
    if not session_results:
        print("Nenhum resultado na sessao para exportar.")
        return

    default_path = Path("exports") / "session_results.json"
    raw_path = input(
        f"Caminho do arquivo JSON (enter para '{default_path.as_posix()}'): "
    ).strip()

    output_path = Path(raw_path) if raw_path else default_path
    created = service.export_results(session_results, output_path)
    print(f"Exportacao concluida: {created}")

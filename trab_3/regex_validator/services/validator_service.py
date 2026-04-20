import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from validators import CPFValidator, EmailValidator, SenhaValidator, TelefoneValidator


class ValidatorService:
    """Orquestra validacoes, logs, historico e exportacao."""

    def __init__(self, storage_dir: str | Path | None = None, log_file: str | Path | None = None):
        self.validators = {
            "email": EmailValidator(),
            "cpf": CPFValidator(),
            "telefone": TelefoneValidator(),
            "senha": SenhaValidator(),
        }

        base_dir = Path(__file__).resolve().parents[1]
        self.storage_dir = Path(storage_dir) if storage_dir else base_dir / "data"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.history_file = self.storage_dir / "validation_history.jsonl"

        log_path = Path(log_file) if log_file else self.storage_dir / "validation.log"
        self.logger = self._build_logger(log_path)

    def validate(self, tipo: str, valor: str, persist: bool = True) -> Dict[str, object]:
        tipo_normalizado = (tipo or "").strip().lower()

        if tipo_normalizado not in self.validators:
            result = {
                "valid": False,
                "message": f"Tipo invalido: {tipo}",
                "value": valor,
                "type": tipo,
                "timestamp": self._now_iso(),
            }
            if persist:
                self._record(result)
            return result

        result = self.validators[tipo_normalizado].validate(valor)
        enriched = {
            **result,
            "type": tipo_normalizado,
            "timestamp": self._now_iso(),
        }

        if persist:
            self._record(enriched)

        return enriched

    def export_results(self, results: List[Dict[str, object]], output_path: str | Path) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=2)

        self.logger.info("Exportacao JSON criada em %s com %d registros.", output, len(results))
        return output

    def load_history(self, limit: int | None = None) -> List[Dict[str, object]]:
        if not self.history_file.exists():
            return []

        with self.history_file.open("r", encoding="utf-8") as file:
            entries = [json.loads(line) for line in file if line.strip()]

        if limit is None:
            return entries
        return entries[-limit:]

    def _record(self, payload: Dict[str, object]) -> None:
        self._append_history(payload)

        level = logging.INFO if payload.get("valid") else logging.WARNING
        self.logger.log(
            level,
            "Validacao tipo=%s valid=%s valor=%s mensagem=%s",
            payload.get("type"),
            payload.get("valid"),
            payload.get("value"),
            payload.get("message"),
        )

    def _append_history(self, payload: Dict[str, object]) -> None:
        with self.history_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")

    @staticmethod
    def _build_logger(log_path: Path) -> logging.Logger:
        logger_name = f"regex_validator.{log_path.resolve()}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if logger.handlers:
            return logger

        handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def _now_iso() -> str:
        return datetime.now().isoformat(timespec="seconds")

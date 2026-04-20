from datetime import datetime
from pathlib import Path

from django.shortcuts import render

from services.validator_service import ValidatorService


def _service() -> ValidatorService:
    return ValidatorService()


def index(request):
    result = None
    selected_type = "email"
    input_value = ""

    if request.method == "POST":
        selected_type = request.POST.get("data_type", "email")
        input_value = request.POST.get("value", "")
        result = _service().validate(selected_type, input_value, persist=True)

    recent_history = _service().load_history(limit=5)
    context = {
        "result": result,
        "recent_history": list(reversed(recent_history)),
        "selected_type": selected_type,
        "input_value": input_value,
    }
    return render(request, "frontend/index.html", context)


def dashboard(request):
    entries = _service().load_history()
    total = len(entries)
    valid_count = sum(1 for item in entries if item.get("valid") is True)
    invalid_count = total - valid_count
    success_rate = round((valid_count / total) * 100, 2) if total else 0.0

    type_totals = {
        "email": 0,
        "cpf": 0,
        "telefone": 0,
        "senha": 0,
    }

    for item in entries:
        data_type = item.get("type")
        if data_type in type_totals:
            type_totals[data_type] += 1

    context = {
        "total": total,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "success_rate": success_rate,
        "type_totals": type_totals,
    }
    return render(request, "frontend/dashboard.html", context)


def history_view(request):
    entries = _service().load_history()
    filter_type = request.GET.get("type", "all")
    filter_status = request.GET.get("status", "all")

    filtered = []
    for item in reversed(entries):
        data_type = item.get("type", "")
        is_valid = item.get("valid") is True

        if filter_type != "all" and data_type != filter_type:
            continue

        if filter_status == "valid" and not is_valid:
            continue
        if filter_status == "invalid" and is_valid:
            continue

        filtered.append(item)

    context = {
        "entries": filtered,
        "filter_type": filter_type,
        "filter_status": filter_status,
    }
    return render(request, "frontend/history.html", context)


def export_view(request):
    export_path = None
    error = None
    limit = 20

    if request.method == "POST":
        raw_limit = request.POST.get("limit", "20").strip()

        try:
            limit = max(1, min(int(raw_limit), 1000))
        except ValueError:
            limit = 20

        data = _service().load_history(limit=limit)

        if not data:
            error = "Nao ha dados no historico para exportar."
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = Path(__file__).resolve().parents[1] / "exports" / f"validacoes_{timestamp}.json"
            created = _service().export_results(data, output)
            export_path = created

    context = {
        "export_path": export_path,
        "error": error,
        "limit": limit,
    }
    return render(request, "frontend/export.html", context)

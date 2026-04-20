# Validador de Dados com RegEx em Python

Aplicacao em Python para validacao de dados usando expressoes regulares, com arquitetura modular, testes automatizados e separacao clara entre logica de negocio e interface.

Agora o projeto possui duas interfaces:

- CLI (terminal)
- Web com Django (frontend Glassmorphism responsivo)

## Objetivo

Validar os seguintes tipos de dado:

- Email
- CPF
- Telefone brasileiro
- Senha forte

Cada validacao retorna um resultado estruturado no formato:

```python
{
    "valid": True or False,
    "message": "explicacao da validacao",
    "value": "valor_original",
    "type": "tipo_validado",
    "timestamp": "YYYY-MM-DDTHH:MM:SS"
}
```

Alguns validadores tambem retornam `normalized` para facilitar auditoria.

## Estrutura do Projeto

```text
regex_validator/
├── manage.py
├── run_web.py
├── webui/
│   ├── settings.py
│   └── urls.py
├── frontend/
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── templates/
│   ├── base.html
│   └── frontend/
│       ├── index.html
│       ├── dashboard.html
│       ├── history.html
│       └── export.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── main.py
├── validators/
│   ├── __init__.py
│   ├── base_validator.py
│   ├── email.py
│   ├── cpf.py
│   ├── telefone.py
│   └── senha.py
├── services/
│   ├── __init__.py
│   └── validator_service.py
├── utils/
│   ├── __init__.py
│   └── regex_patterns.py
├── interface/
│   ├── __init__.py
│   └── cli.py
├── tests/
│   └── test_validators.py
├── data/
│   ├── validation.log
│   └── validation_history.jsonl
└── README.md
```

## Explicacao das RegEx

### Email

Padrao:

```regex
^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$
```

Interpretacao:

- `^` inicio da string
- `[\w.+-]+` parte local do email (usuario)
- `@` separador obrigatorio
- `[\w-]+` dominio principal
- `(?:\.[\w-]+)+` ao menos um sufixo de dominio (`.br`, `.com`, `.edu.br`)
- `$` fim da string

### CPF

Padroes de formato:

```regex
^\d{3}\.\d{3}\.\d{3}-\d{2}$
^\d{11}$
```

Interpretacao:

- Aceita CPF com mascara (`000.000.000-00`) ou somente digitos (`00000000000`)
- Depois do match de formato, a aplicacao executa o algoritmo real dos digitos verificadores

### Telefone Brasileiro

Padrao:

```regex
^\(\d{2}\)\s\d{4,5}-\d{4}$
```

Interpretacao:

- `\(\d{2}\)` DDD com 2 digitos entre parenteses
- `\s` espaco obrigatorio
- `\d{4,5}` prefixo de 4 ou 5 digitos
- `-\d{4}` sufixo de 4 digitos

### Senha Forte

Padrao:

```regex
^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{8,}$
```

Interpretacao:

- `(?=.*[A-Z])` ao menos uma maiuscula
- `(?=.*[a-z])` ao menos uma minuscula
- `(?=.*\d)` ao menos um digito
- `(?=.*[^\w\s])` ao menos um simbolo
- `.{8,}` no minimo 8 caracteres

## Diferenciais Implementados

- Validacao real de CPF (digitos verificadores)
- Logs de validacao em arquivo
- Historico persistente em JSON Lines
- Exportacao dos resultados da sessao em JSON

## Como Executar

No diretorio `trab_3/regex_validator`:

CLI:

```bash
python main.py
```

Web Django:

```bash
python run_web.py
```

Depois, acesse `http://127.0.0.1:8000`.

## Como Executar Testes

No diretorio `trab_3/regex_validator`:

```bash
pytest -v
```

Para testes das rotas web Django:

```bash
python manage.py test frontend -v 2
```

## Frontend Web

Telas implementadas:

- Validacao unificada (Email, CPF, Telefone, Senha)
- Dashboard com metricas (total, validos, invalidos e taxa de sucesso)
- Historico com filtros por tipo e status
- Exportacao JSON a partir do historico persistido

Observacao: o frontend web reutiliza o mesmo `ValidatorService`, mantendo consistencia de regras entre CLI e Web.

## Exemplo de Uso (CLI)

```text
1 - Validar Email
2 - Validar CPF
3 - Validar Telefone
4 - Validar Senha Forte
5 - Ver historico recente
6 - Exportar resultados da sessao (JSON)
0 - Sair
```

## Conexao com Automatos

As expressoes regulares descrevem linguagens regulares. Toda linguagem regular reconhecida por uma RegEx pode ser reconhecida por um automato finito deterministico (AFD). Portanto:

- cada padrao define um conjunto de cadeias validas
- o processo de validacao equivale a decidir aceitacao/rejeicao da cadeia
- a ferramenta conecta teoria de linguagens formais com aplicacao pratica de validacao de dados

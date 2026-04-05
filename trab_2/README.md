# Conversor de Número para Extenso (FSM - Mealy)

Este projeto implementa um conversor de números inteiros (0 a 999.999) para texto por extenso, utilizando o conceito de **Máquina de Estados Finitos (Mealy)**.

Suporta:
- 🇧🇷 Português
- 🇺🇸 Inglês

---

## 🧠 Modelagem como Máquina de Estados (Mealy)

A solução foi modelada como uma **Máquina de Mealy**, onde:

- Cada estado representa uma etapa do processamento do número
- A saída é gerada durante as transições (dependendo do estado + entrada)

---

## 🔄 Diagrama de Estados

```mermaid
stateDiagram-v2
    [*] --> INICIO

    INICIO --> VALIDACAO : entrada
    VALIDACAO --> ERRO : inválido
    VALIDACAO --> SEPARACAO : válido

    SEPARACAO --> MILHAR : n >= 1000
    SEPARACAO --> CENTENA : n < 1000

    MILHAR --> CENTENA : processa milhar

    CENTENA --> DEZENA : resto >= 100
    DEZENA --> UNIDADE : resto >= 10
    UNIDADE --> FINAL

    CENTENA --> FINAL : resto == 0
    DEZENA --> FINAL : resto < 10

    FINAL --> [*]

    ERRO --> [*]
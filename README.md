# Gestor de Academia

Programa em Python (terminal) para administrar alunos, planos, presenças e alertas de vencimento de matrícula de uma academia.

📄 **Relatório completo:** [docs/relatorio.md](docs/relatorio.md)
📊 **Diagrama de classes:** [docs/Diagrama.png](docs/Diagrama.png)

![Diagrama de classes](docs/Diagrama.png)

## Como executar

1. Instale o Python 3 (python.org).
2. Baixe o repositório (**Code → Download ZIP**) e extraia.
3. No terminal, dentro da pasta do projeto:

```
python src/main.py
```

(No Mac/Linux pode ser `python3 src/main.py`.)

## Estrutura

```
├── docs/        # relatório, diagrama e evidências
└── src/
    ├── main.py          # menu
    ├── models/          # Plano, PlanoMensal, PlanoAnual, Aluno, Alerta
    └── services/        # Gerenciador (regras + CSV)
```

**Integrantes:** _Nome 1, Nome 2, Nome 3_

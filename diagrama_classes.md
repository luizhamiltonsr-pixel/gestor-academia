# Diagrama de Classes: Gestor de Academia

O GitHub desenha o diagrama abaixo automaticamente.

```mermaid
classDiagram
    class Plano {
        +String nome
        +float valor
    }
    class Aluno {
        +String nome
        +String email
        +String plano
        +String data_matricula
        +List presencas
        +registrar_presenca() bool
        +total_presencas() int
    }
    class Academia {
        +List alunos
        +carregar()
        +salvar()
        +buscar_aluno(email) Aluno
        +cadastrar_aluno(nome, email, plano) bool
        +remover_aluno(email) bool
        +registrar_presenca(email) String
    }

    Academia "1" o-- "*" Aluno : possui
    Plano "1" <-- "*" Aluno : escolhe
```

## Explicação

| Classe | O que faz |
|---|---|
| `Plano` | Guarda o nome e o valor de um plano (Mensal, Trimestral, Anual). |
| `Aluno` | Guarda os dados de um aluno e as datas em que ele treinou. |
| `Academia` | Guarda a lista de alunos e salva/carrega os dados no arquivo CSV. |

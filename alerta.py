class Alerta:
    """Aviso sobre um aluno com a matrícula vencida ou perto de vencer."""

    def __init__(self, aluno, mensagem):
        self.aluno = aluno
        self.mensagem = mensagem

    def __str__(self):
        return f"{self.aluno.nome} ({self.aluno.email}): {self.mensagem}"

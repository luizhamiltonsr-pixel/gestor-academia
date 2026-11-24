class Plano:
    """Classe base: um plano da academia.

    PlanoMensal e PlanoAnual herdam desta classe.
    """

    def __init__(self, nome, valor_mensal, duracao_meses):
        self.nome = nome
        self.valor_mensal = valor_mensal
        self.duracao_meses = duracao_meses

    def valor_total(self):
        """Quanto o aluno paga no plano inteiro."""
        return self.valor_mensal * self.duracao_meses

    def __str__(self):
        return f"{self.nome} - R$ {self.valor_total():.2f} ({self.duracao_meses} mês(es))"

from datetime import date, timedelta


class Aluno:
    """Um aluno da academia."""

    def __init__(self, nome, email, plano, data_matricula=None, presencas=None):
        self.nome = nome
        self.email = email
        self.plano = plano                                   # objeto Plano
        self.data_matricula = data_matricula or date.today()  # tipo date
        self.presencas = presencas or []                     # lista de datas (texto)

    def registrar_presenca(self):
        """Marca presença de hoje. Retorna False se já marcou hoje."""
        hoje = str(date.today())
        if hoje in self.presencas:
            return False
        self.presencas.append(hoje)
        return True

    def total_presencas(self):
        return len(self.presencas)

    def data_vencimento(self):
        """Matrícula + duração do plano (considerando 30 dias por mês)."""
        return self.data_matricula + timedelta(days=30 * self.plano.duracao_meses)

    def dias_para_vencer(self):
        """Dias que faltam para vencer. Negativo = já venceu."""
        return (self.data_vencimento() - date.today()).days

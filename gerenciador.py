import csv
import os
from datetime import date

from models.aluno import Aluno
from models.alerta import Alerta
from models.plano_mensal import PlanoMensal
from models.plano_anual import PlanoAnual

# Pasta e arquivo onde os dados ficam guardados (na raiz do projeto)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTA = os.path.join(RAIZ, "dados")
ARQUIVO = os.path.join(PASTA, "alunos.csv")


class Gerenciador:
    """Guarda a lista de alunos, aplica as regras e salva tudo no CSV."""

    def __init__(self):
        self.planos = {"Mensal": PlanoMensal(), "Anual": PlanoAnual()}
        self.alunos = []
        self.carregar()

    # ---------- arquivo CSV ----------
    def carregar(self):
        """Lê os alunos do arquivo CSV (se ele existir)."""
        if not os.path.exists(ARQUIVO):
            return
        with open(ARQUIVO, newline="", encoding="utf-8") as arquivo:
            for linha in csv.DictReader(arquivo):
                plano = self.planos[linha["plano"]]
                if linha["presencas"]:
                    presencas = linha["presencas"].split(";")
                else:
                    presencas = []
                data = date.fromisoformat(linha["data_matricula"])
                self.alunos.append(Aluno(linha["nome"], linha["email"], plano, data, presencas))

    def salvar(self):
        """Grava todos os alunos no arquivo CSV."""
        os.makedirs(PASTA, exist_ok=True)
        with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["nome", "email", "plano", "data_matricula", "presencas"])
            for a in self.alunos:
                escritor.writerow([a.nome, a.email, a.plano.nome,
                                   a.data_matricula.isoformat(), ";".join(a.presencas)])

    # ---------- regras do sistema ----------
    def buscar_aluno(self, email):
        """Procura um aluno pelo e-mail. Retorna None se não achar."""
        for aluno in self.alunos:
            if aluno.email.lower() == email.lower():
                return aluno
        return None

    def cadastrar_aluno(self, nome, email, nome_plano):
        if self.buscar_aluno(email) is not None:
            return False                                  # e-mail já cadastrado
        self.alunos.append(Aluno(nome, email, self.planos[nome_plano]))
        self.salvar()
        return True

    def remover_aluno(self, email):
        aluno = self.buscar_aluno(email)
        if aluno is None:
            return False
        self.alunos.remove(aluno)
        self.salvar()
        return True

    def registrar_presenca(self, email):
        """Retorna: 'ok', 'repetida' ou 'nao_encontrado'."""
        aluno = self.buscar_aluno(email)
        if aluno is None:
            return "nao_encontrado"
        if aluno.registrar_presenca():
            self.salvar()
            return "ok"
        return "repetida"

    def gerar_alertas(self, dias_limite=7):
        """Cria alertas para matrículas vencidas ou que vencem em poucos dias."""
        alertas = []
        for aluno in self.alunos:
            dias = aluno.dias_para_vencer()
            if dias < 0:
                alertas.append(Alerta(aluno, f"matrícula vencida há {-dias} dia(s)"))
            elif dias <= dias_limite:
                alertas.append(Alerta(aluno, f"matrícula vence em {dias} dia(s)"))
        return alertas

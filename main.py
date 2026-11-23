"""
GESTOR DE ACADEMIA (versão simples)

Como rodar:
    python main.py

O programa guarda os dados no arquivo dados/alunos.csv
(esse arquivo é criado sozinho na primeira vez que você cadastrar um aluno).
"""

import csv                      # biblioteca para ler e escrever planilhas CSV
import os                       # biblioteca para mexer com pastas e arquivos
from datetime import date       # biblioteca para pegar a data de hoje

# Pasta e arquivo onde os dados ficam guardados
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
ARQUIVO = os.path.join(PASTA, "alunos.csv")


# ---------------------------------------------------------------
# CLASSE 1: Plano
# Representa um tipo de plano da academia (nome e valor).
# ---------------------------------------------------------------
class Plano:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor


# Lista com os planos que a academia oferece
PLANOS = [
    Plano("Mensal", 99.90),
    Plano("Trimestral", 270.00),
    Plano("Anual", 960.00),
]


# ---------------------------------------------------------------
# CLASSE 2: Aluno
# Representa um aluno da academia.
# ---------------------------------------------------------------
class Aluno:
    def __init__(self, nome, email, plano, data_matricula=None, presencas=None):
        self.nome = nome
        self.email = email
        self.plano = plano                                  # nome do plano (texto)
        self.data_matricula = data_matricula or str(date.today())
        self.presencas = presencas or []                    # lista de datas

    def registrar_presenca(self):
        """Marca presença de hoje. Retorna False se já marcou hoje."""
        hoje = str(date.today())
        if hoje in self.presencas:
            return False
        self.presencas.append(hoje)
        return True

    def total_presencas(self):
        return len(self.presencas)


# ---------------------------------------------------------------
# CLASSE 3: Academia
# Guarda a lista de alunos e sabe salvar/carregar no arquivo CSV.
# ---------------------------------------------------------------
class Academia:
    def __init__(self):
        self.alunos = []
        self.carregar()

    def carregar(self):
        """Lê os alunos do arquivo CSV (se ele existir)."""
        if not os.path.exists(ARQUIVO):
            return
        with open(ARQUIVO, newline="", encoding="utf-8") as arquivo:
            for linha in csv.DictReader(arquivo):
                if linha["presencas"]:
                    presencas = linha["presencas"].split(";")
                else:
                    presencas = []
                aluno = Aluno(linha["nome"], linha["email"], linha["plano"],
                              linha["data_matricula"], presencas)
                self.alunos.append(aluno)

    def salvar(self):
        """Grava todos os alunos no arquivo CSV."""
        os.makedirs(PASTA, exist_ok=True)
        with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["nome", "email", "plano", "data_matricula", "presencas"])
            for a in self.alunos:
                escritor.writerow([a.nome, a.email, a.plano, a.data_matricula,
                                   ";".join(a.presencas)])

    def buscar_aluno(self, email):
        """Procura um aluno pelo e-mail. Retorna None se não achar."""
        for aluno in self.alunos:
            if aluno.email.lower() == email.lower():
                return aluno
        return None

    def cadastrar_aluno(self, nome, email, plano):
        if self.buscar_aluno(email) is not None:
            return False                                    # e-mail já cadastrado
        self.alunos.append(Aluno(nome, email, plano))
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


# ---------------------------------------------------------------
# MENU (parte que conversa com o usuário)
# ---------------------------------------------------------------
def escolher_plano():
    print("Planos disponíveis:")
    for i, plano in enumerate(PLANOS, start=1):
        print(f"  {i} - {plano.nome} (R$ {plano.valor:.2f})")
    while True:
        escolha = input("Escolha o número do plano: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(PLANOS):
            return PLANOS[int(escolha) - 1].nome
        print("Opção inválida, tente de novo.")


def main():
    academia = Academia()

    while True:
        print("\n===== GESTOR DE ACADEMIA =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Registrar presença de hoje")
        print("4 - Ver presenças de um aluno")
        print("5 - Remover aluno")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            if nome == "" or "@" not in email:
                print("Nome vazio ou e-mail inválido.")
                continue
            plano = escolher_plano()
            if academia.cadastrar_aluno(nome, email, plano):
                print("Aluno cadastrado com sucesso!")
            else:
                print("Já existe um aluno com esse e-mail.")

        elif opcao == "2":
            if not academia.alunos:
                print("Nenhum aluno cadastrado.")
            for a in academia.alunos:
                print(f"- {a.nome} | {a.email} | plano {a.plano} | "
                      f"{a.total_presencas()} presenças")

        elif opcao == "3":
            email = input("E-mail do aluno: ").strip()
            resultado = academia.registrar_presenca(email)
            if resultado == "ok":
                print("Presença registrada!")
            elif resultado == "repetida":
                print("Esse aluno já marcou presença hoje.")
            else:
                print("Aluno não encontrado.")

        elif opcao == "4":
            aluno = academia.buscar_aluno(input("E-mail do aluno: ").strip())
            if aluno is None:
                print("Aluno não encontrado.")
            else:
                print(f"{aluno.nome} - {aluno.total_presencas()} presenças")
                for dia in aluno.presencas:
                    print("  *", dia)

        elif opcao == "5":
            if academia.remover_aluno(input("E-mail do aluno: ").strip()):
                print("Aluno removido.")
            else:
                print("Aluno não encontrado.")

        elif opcao == "0":
            print("Até logo!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

"""
GESTOR DE ACADEMIA

Como rodar (na pasta do projeto):
    python src/main.py

Os dados ficam em dados/alunos.csv (criado sozinho no primeiro cadastro).
"""

from services.gerenciador import Gerenciador


def escolher_plano(gerenciador):
    """Mostra os planos e devolve o nome do plano escolhido."""
    nomes = list(gerenciador.planos.keys())
    print("Planos disponíveis:")
    for i, nome in enumerate(nomes, start=1):
        print(f"  {i} - {gerenciador.planos[nome]}")
    while True:
        escolha = input("Escolha o número do plano: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
            return nomes[int(escolha) - 1]
        print("Opção inválida, tente de novo.")


def main():
    gerenciador = Gerenciador()

    while True:
        print("\n===== GESTOR DE ACADEMIA =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Registrar presença de hoje")
        print("4 - Ver presenças de um aluno")
        print("5 - Ver alertas de vencimento")
        print("6 - Remover aluno")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            if nome == "" or "@" not in email:
                print("Nome vazio ou e-mail inválido.")
                continue
            plano = escolher_plano(gerenciador)
            if gerenciador.cadastrar_aluno(nome, email, plano):
                print("Aluno cadastrado com sucesso!")
            else:
                print("Já existe um aluno com esse e-mail.")

        elif opcao == "2":
            if not gerenciador.alunos:
                print("Nenhum aluno cadastrado.")
            for a in gerenciador.alunos:
                print(f"- {a.nome} | {a.email} | plano {a.plano.nome} | "
                      f"vence em {a.data_vencimento().strftime('%d/%m/%Y')} | "
                      f"{a.total_presencas()} presenças")

        elif opcao == "3":
            resultado = gerenciador.registrar_presenca(input("E-mail do aluno: ").strip())
            if resultado == "ok":
                print("Presença registrada!")
            elif resultado == "repetida":
                print("Esse aluno já marcou presença hoje.")
            else:
                print("Aluno não encontrado.")

        elif opcao == "4":
            aluno = gerenciador.buscar_aluno(input("E-mail do aluno: ").strip())
            if aluno is None:
                print("Aluno não encontrado.")
            else:
                print(f"{aluno.nome} - {aluno.total_presencas()} presenças")
                for dia in aluno.presencas:
                    print("  *", dia)

        elif opcao == "5":
            alertas = gerenciador.gerar_alertas()
            if not alertas:
                print("Nenhum alerta. Todas as matrículas estão em dia!")
            for alerta in alertas:
                print("!", alerta)

        elif opcao == "6":
            if gerenciador.remover_aluno(input("E-mail do aluno: ").strip()):
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

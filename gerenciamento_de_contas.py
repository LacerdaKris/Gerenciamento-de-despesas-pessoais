import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random


# classe p/ cada transação
class Transacao:
    def __init__(self, data, tipo, categoria, descricao, valor):
        self.data = data
        self.tipo = tipo
        self.categoria = categoria
        self.descricao = descricao
        self.valor = valor


# classe p/ cada conta
class Conta:
    # construtor da conta e inicializa com saldo zero
    def __init__(self, banco, agencia, numero):
        self.banco = banco
        self.agencia = agencia
        self.numero = numero
        self.saldo = 0
        self.transacoes = []

    # atualiza saldo conforme a transação
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
        if transacao.tipo == "Receita":
            self.saldo += transacao.valor
        else:
            self.saldo -= transacao.valor


# classe do sistema gerencial
class Sistema:
    # construtor
    def __init__(self):
        # atributo p/ armazenar contas
        self.contas = []
        self.criar_dados_exemplo()

    def criar_dados_exemplo(self):
        # contas de exemplo
        conta1 = Conta("Itau", "321", "12345")
        conta2 = Conta("Nubank", "001", "22222")
        self.contas.append(conta1)
        self.contas.append(conta2)
        # transações de exemplo para cada conta
        for conta in self.contas:
            # itera os últimos 6 meses
            meses = ["01", "02", "03", "04", "05", "06"]
            for mes in meses:
                # faz os dois lançamentos líquidos de receita do mês (fixo e variável)
                for i in range(2):
                    data_string = f"05/{mes}/2023"
                    data = datetime.strptime(data_string, "%d/%m/%Y")
                    tipo = "Receita"
                    categorias = ["Salário", "Comissões"]
                    categoria = categorias[i]
                    descricao = f"Descrição da transação de {categoria}"
                    if categoria == "Salário":
                        valor = 2000
                    else:
                        valor = random.randint(1200, 1800)
                    transacao = Transacao(data, tipo, categoria, descricao, valor)
                    conta.adicionar_transacao(transacao)
                # faz 7 lançamentos de despesa com tipo e valor aleatorios
                for lancar_despesas in range(7):
                    # datas aleatórias de cada mês (30 dias)
                    dia = random.randint(10, 28)
                    data_string = f"{dia}/{mes}/2023"
                    data = datetime.strptime(data_string, "%d/%m/%Y")
                    tipo = "Despesa"
                    categoria = random.choice(
                        [
                            "Lazer",
                            "Vestuário",
                            "Farmácia",
                            "Transporte",
                            "Educação",
                            "Alimentação",
                        ]
                    )
                    valor = random.randint(60, 400)
                    descricao = f"Descrição da transação de {categoria}"
                    transacao = Transacao(data, tipo, categoria, descricao, valor)
                    conta.adicionar_transacao(transacao)
                # um lançamento de contas fixas mensal
                data_string = f"10/{mes}/2023"
                data = datetime.strptime(data_string, "%d/%m/%Y")
                tipo = "Despesa"
                categoria = "Contas fixas da casa"
                descricao = "Condomínio, água, luz, gás e internet"
                valor = 1500
                transacao = Transacao(data, tipo, categoria, descricao, valor)
                conta.adicionar_transacao(transacao)

    ### MENU GERAL/PRINCIPAL ###
    def menu(self):
        print("_____________________________________")
        print("SISTEMA DE GERENCIAMENTO DE DESPESAS")
        print("1- Gerenciar contas")
        print("2- Gerenciar transações")
        print("3- Painel geral")
        print("4- Finalizar programa")

    ### SUB MENU GERENCIAR CONTAS ###
    def menu_gerenciar_contas(self):
        print("_____________________________________")
        print("GERENCIAR CONTAS")
        print("1- Cadastrar conta")
        print("2- Remover conta")
        print("3- Mesclar contas")
        print("4- Voltar ao menu anterior")

    def cadastrar_conta(self):
        banco = input("Nome do banco: ")
        agencia = input("Número da agência: ")
        numero = input("Número da conta: ")
        conta = Conta(banco, agencia, numero)
        self.contas.append(conta)
        print(f"A conta {conta.numero} foi cadastrada!")

    def remover_conta(self):
        numero_conta = input("Digite o número da conta a remover: ")
        for conta in self.contas:
            if conta.numero == numero_conta:
                confirmacao = input(
                    f"Todos os dados da CC {conta.numero} serão excluídos, confirma? (S/N): "
                )
                if confirmacao.upper() == "S":
                    self.contas.remove(conta)
                    print(f"A conta {conta.numero} foi removida!")
                else:
                    print("A exclusão da conta foi cancelada.")
                return
        print("Conta não encontrada!")

    def mesclar_contas(self):
        numero_conta1 = input("Digite o número da primeira conta: ")
        numero_conta2 = input("Digite o número da segunda conta: ")
        conta1 = None
        conta2 = None
        for conta in self.contas:
            if conta.numero == numero_conta1:
                conta1 = conta
            elif conta.numero == numero_conta2:
                conta2 = conta
        if conta1 is None or conta2 is None:
            print("Conta(s) não encontrada(s).")
            return
        conta_destino = conta1
        conta_origem = conta2
        confirmacao_exclusao = input(
            f"Essa operação exclui a conta {conta_origem.numero}. Confirma? (S/N): "
        )
        if confirmacao_exclusao.upper() == "S":
            conta_destino.transacoes.extend(conta_origem.transacoes)
            self.contas.remove(conta_origem)
            print(f"As transações foram mescladas na conta {conta_destino.numero}.")
        else:
            print("Mesclagem cancelada.")

    ### SUB MENU GERENCIAR TRANSAÇÕES ###
    def menu_gerenciar_transacoes(self, conta):
        print("_____________________________________")
        print(f"GERENCIAR TRANSAÇÕES DA CONTA {conta.numero}")
        print("1- Extrato da conta")
        print("2- Incluir transação")
        print("3- Editar a última transação")
        print("4- Transferir fundos")
        print("5- Voltar ao menu anterior")

    def extrato_conta(self, transacoes):
        # ordena por data
        transacoes.sort(key=lambda transacao: transacao.data)
        saldo = 0
        # imprime os dados de cada transação e o saldo da conta
        for transacao in transacoes:
            if transacao.tipo == "Receita":
                saldo += transacao.valor
            else:
                saldo -= transacao.valor
            print(
                f"Data: {transacao.data}\n"
                f"Tipo: {transacao.tipo}\n"
                f"Categoria: {transacao.categoria}\n"
                f"Descrição: {transacao.descricao}\n"
                f"Valor: {transacao.valor}\n"
                f"Saldo: {saldo}\n"
            )

    def incluir_transacao(self, conta):
        # garante que o usuário digitou data no formato correto
        while True:
            data_string = input("Data (DD/MM/AAAA): ")
            try:
                data = datetime.strptime(data_string, "%d/%m/%Y")
                break
            except ValueError:
                print("Formato de data inválido! Digite novamente.")
        # garante que o input será lido com a primeira letra maiuscula
        tipo = input("Tipo (Receita/Despesa): ").capitalize()
        if tipo not in ["Receita", "Despesa"]:
            tipo = input("Digitar 'Receita' ou 'Despesa': ").capitalize()
        categoria = input("Categoria: ")
        descricao = input("Descrição: ")
        # garante que o valor seja um número
        while True:
            valor = input("Valor: ")
            try:
                valor = float(valor)
                break
            except ValueError:
                print("Valor inválido! Digite um número.")
        transacao = Transacao(data, tipo, categoria, descricao, valor)
        conta.adicionar_transacao(transacao)

    def editar_ultima_transacao(self, conta):
        if len(conta.transacoes) > 0:
            # seleciona a última transação inserida
            ultima_transacao = conta.transacoes[-1]
            print("EDITAR DADOS")
            # pra cada informação da transação pergunta ao usuário se quer alterar
            opcao = input(f"Deseja alterar a data ({ultima_transacao.data})? (S/N): ")
            if opcao.upper() == "S":
                # garante que a data nova está no formato válido
                while True:
                    data_string = input("Nova data (DD/MM/AAAA): ")
                    try:
                        ultima_transacao.data = datetime.strptime(
                            data_string, "%d/%m/%Y"
                        )
                        break
                    except ValueError:
                        print("Formato de data inválido! Digite novamente.")
            opcao = input(f"Deseja alterar o tipo ({ultima_transacao.tipo})? (S/N): ")
            if opcao.upper() == "S":
                # garantir input de tipo correto
                novo_tipo = input("Novo tipo (Receita/Despesa): ").capitalize()
                if novo_tipo not in ["Receita", "Despesa"]:
                    novo_tipo = input("Digitar 'Receita' ou 'Despesa': ").capitalize()
                ultima_transacao.tipo = novo_tipo
            opcao = input(
                f"Deseja alterar a categoria ({ultima_transacao.categoria})? (S/N): "
            )
            if opcao.upper() == "S":
                ultima_transacao.categoria = input("Nova categoria: ")
            opcao = input(
                f"Deseja alterar a descrição ({ultima_transacao.descricao})? (S/N): "
            )
            if opcao.upper() == "S":
                ultima_transacao.descricao = input("Nova descrição: ")
            opcao = input(f"Deseja alterar o valor ({ultima_transacao.valor})? (S/N): ")
            if opcao.upper() == "S":
                # garante que o valor seja um número
                while True:
                    valor = input("Valor: ")
                    try:
                        ultima_transacao.valor = float(valor)
                        break
                    except ValueError:
                        print("Valor inválido! Digite um número.")
            print("Transação atualizada com sucesso.")
        # caso não tenham transações cadastradas para alterar
        else:
            print("Ainda não possuem transações cadastradas para editar.")

    def transferir_fundos(self, conta):
        numero_conta_destino = input("Digite o número da conta de destino: ")
        conta_destino = obter_conta(numero_conta_destino)
        if not conta_destino:
            print("Conta não encontrada.")
            return
        valor_transferencia = float(input("Valor a ser transferido: "))
        if conta.saldo < valor_transferencia:
            print("O saldo não é suficiente.")
            return
        data = datetime.now()
        # saque na conta atual
        tipo = "Despesa"
        categoria = "Transferência"
        descricao = f"Transferência para CC {numero_conta_destino}"
        transacao_saque = Transacao(
            data, tipo, categoria, descricao, valor_transferencia
        )
        conta.adicionar_transacao(transacao_saque)
        # crédito na conta de destino
        tipo = "Receita"
        descricao = f"Transferência da CC {conta.numero}"
        transacao_deposito = Transacao(
            data, tipo, categoria, descricao, valor_transferencia
        )
        conta_destino.adicionar_transacao(transacao_deposito)
        print("Transferência realizada com sucesso.")

    ### SUB MENU PAINEL GERAL ###
    def menu_painel_geral(self):
        print("_____________________________________")
        print("PAINEL GERAL")
        print("1- Resumo das contas")
        print("2- Resumo de receitas e despesas do mês")
        print("3- Saldo geral dos últimos 6 meses")
        print("4- Gráfico de receitas e despesas")
        print("5- Voltar ao menu anterior")

    def resumo_contas(self):
        saldo_total = 0
        # itera em todas as contas mostrando seu saldo atual e somando ao total
        for conta in self.contas:
            print(f"Conta: {conta.banco} {conta.agencia} {conta.numero}")
            print(f"Saldo: {conta.saldo}")
            print("*  *  *  *  *  *  *  *  *  *  *  *")
            saldo_total += conta.saldo
        print(f"Saldo Total: {saldo_total}")

    def resumo_receitas_despesas(self):
        mes_atual = datetime.now().month
        total_receitas = 0
        total_despesas = 0
        # itera em cada conta e transação, somando suas receitas e despesas nas variáveis
        for conta in self.contas:
            for transacao in conta.transacoes:
                data_transacao = transacao.data
                if data_transacao.month == mes_atual:
                    if transacao.tipo == "Receita":
                        total_receitas += transacao.valor
                    else:
                        total_despesas += transacao.valor
        print(f"Total em receitas do Mês: {total_receitas}")
        print(f"Total em despesas do Mês: {total_despesas}")

    def saldo_geral(self):
        saldo_meses = []
        mes_atual = datetime.now().month
        # itera 6x pra cada conta p/ armazenar saldo dos meses
        for mes in range(6):
            mes_referencia = mes_atual - mes
            saldo_mes = 0
            for conta in self.contas:
                for transacao in conta.transacoes:
                    transacao_data = transacao.data
                    if transacao_data.month == mes_referencia:
                        if transacao.tipo == "Receita":
                            saldo_mes += transacao.valor
                        else:
                            saldo_mes -= transacao.valor
            saldo_meses.append(saldo_mes)
        # itera lista de saldos e meses
        for saldos in range(6):
            mes_referencia = mes_atual - saldos
            print(f"Saldo do mês {mes_referencia}: {saldo_meses[saldos]}")

    def gerar_grafico(self):
        # armazenar os dados p/ o gráfico
        meses = []
        receitas = []
        despesas = []
        mes_atual = datetime.now().month
        # total de receitas e despesas para cada mês do último semestre
        for mes in range(6):
            mes_referencia = mes_atual - mes
            receita = 0
            despesa = 0
            for conta in self.contas:
                for transacao in conta.transacoes:
                    transacao_data = transacao.data
                    if transacao_data.month == mes_referencia:
                        if transacao.tipo == "Receita":
                            receita += transacao.valor
                        else:
                            despesa += transacao.valor
            # adiciona mês e totais nos arrays
            meses.append(mes_referencia)
            receitas.append(receita)
            despesas.append(despesa)
        # cria gráfico de linha p/ receita e despesas no eixo Y, e meses no eixo X
        plt.plot(meses, receitas, label="Receitas")
        plt.plot(meses, despesas, label="Despesas")
        # rótulo dos eixos e legenda das linhas
        plt.xlabel("Meses")
        plt.ylabel("Valor")
        plt.legend()
        # título e exibição
        plt.title("Receitas e despesas ao mês")
        plt.show()


# instanciação da classe sistema para acesso dos menus
sistema = Sistema()


### SUB MENU GERENCIAR CONTAS ###
def gerenciar_contas():
    while True:
        sistema.menu_gerenciar_contas()
        opcao_gerenciar_contas = input("Digite a opção desejada: ")
        if opcao_gerenciar_contas == "1":
            sistema.cadastrar_conta()
        elif opcao_gerenciar_contas == "2":
            sistema.remover_conta()
        elif opcao_gerenciar_contas == "3":
            sistema.mesclar_contas()
        elif opcao_gerenciar_contas == "4":
            break
        else:
            print("Opção inválida.")


### SUB MENU GERENCIAR TRANSAÇÕES ###
def gerenciar_transacoes():
    numero_conta = input("Digite o número da conta: ")
    conta = obter_conta(numero_conta)
    if not conta:
        print("Conta não encontrada.")
        return
    while True:
        sistema.menu_gerenciar_transacoes(conta)
        opcao_gerenciar_transacoes = input("Digite a opção desejada: ")
        if opcao_gerenciar_transacoes == "1":
            sistema.extrato_conta(conta.transacoes)
        elif opcao_gerenciar_transacoes == "2":
            sistema.incluir_transacao(conta)
        elif opcao_gerenciar_transacoes == "3":
            sistema.editar_ultima_transacao(conta)
        elif opcao_gerenciar_transacoes == "4":
            sistema.transferir_fundos(conta)
        elif opcao_gerenciar_transacoes == "5":
            break
        else:
            print("Opção inválida.")


def obter_conta(numero_conta):
    for conta in sistema.contas:
        if conta.numero == numero_conta:
            return conta
    return None


### SUB MENU PAINEL GERAL ###
def painel_geral():
    while True:
        sistema.menu_painel_geral()
        opcao_gerenciar_contas = input("Digite a opção desejada: ")
        if opcao_gerenciar_contas == "1":
            sistema.resumo_contas()
        elif opcao_gerenciar_contas == "2":
            sistema.resumo_receitas_despesas()
        elif opcao_gerenciar_contas == "3":
            sistema.saldo_geral()
        elif opcao_gerenciar_contas == "4":
            sistema.gerar_grafico()
            break
        elif opcao_gerenciar_contas == "5":
            break
        else:
            print("Opção inválida.")


### EXECUÇÃO DO MENU GERAL/PRINCIPAL ###
continua_pedindo_opcao = True
while continua_pedindo_opcao:
    sistema.menu()
    opcao_geral = input("Digite o número da opção desejada: ")
    if opcao_geral == "1":
        gerenciar_contas()
    elif opcao_geral == "2":
        gerenciar_transacoes()
    elif opcao_geral == "3":
        painel_geral()
    elif opcao_geral == "4":
        print("Programa encerrado.")
        continua_pedindo_opcao = False
        break
    else:
        print("Opção inválida - Tente novamente com um número de 1 a 4.")

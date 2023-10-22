import textwrap
from time import sleep


def linha(tam=42):
    return '-' * tam


def menu():
    print(linha())
    print('MENU'.center(42))
    print(linha())
    menu = ('''
        \033[34m[1]\tDEPÓSITO
        [2]\tSAQUE
        [3]\tEXTRATO
        [4]\tNOVACONTA
        [5]\tLISTAR CONTAS
        [6]\tNOVO USUÁRIO
        [0]\tFINALIZAR OPERAÇÃO \033[m
    
        Escolha uma opção: ''')


    return input(textwrap.dedent(menu))


def deposito(saldo, valor, extrato, numero_depositos): #ver segunda 02/10
    if valor > 0:
        saldo += valor
        numero_depositos += 1
        extrato += f'Depósito realizado:\t R${valor}'
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
        sleep(1)
    else:
        print('Valor incorreto, não é possivel executar esta operação!')

    return saldo, valor, extrato, numero_depositos


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saque = numero_saques >= limite_saques
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    if excedeu_saldo:
        print('Saldo insuficiente!')
    elif excedeu_saque:
        print('Operação negada! Número maximo de saques realizados!')
    elif excedeu_limite:
        print('Operação negada! O seu limite de saque é de R$ 500,00 por operação!')
    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque realizado:\t R${valor:.2f}\n"
        print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
        sleep(1)
    else:
        print('Operação negada, valor incorreto!')
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato, numero_saques, numero_depositos):
    print('CARREGANDO EXTRATO...')
    sleep(2)
    print('{:=^40}'.format(' EXTRATO '))
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'Depositos realizados: {numero_depositos}')
    print(f'Saques realizados: {numero_saques}')
    print(f'Seu Saldo: {saldo:.2f}')
   # print(extrato)
    print('=' * 40)
    return saldo, extrato, numero_saques, numero_depositos


def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente numero): ')
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('\n Já existe usuario com este CPF')
    nome = input('Digite o nome completo: ')
    data_nascimento = input('Digite a data de nascimento (dd-mm-aaaa)')
    endereco = input('Digite o seu endereço: ')
    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    print('Usuario criado com sucesso!')
    sleep(1)


def filtrar_usuario(cpf, usuarios):
    filtro = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return filtro[0] if filtro else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usário: ')
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('\nConta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    print('Usuário não encontrado, fluxo encerrado!')


def listar_contas(contas):
    for c in contas:
        linha = f'''
                Agência:\t{c['agencia']}
                C/C:\t\t{c['numero_conta']}
                Titular:\t{c['usuario']['nome']}
        '''
        print('=-' * 50)
        print(textwrap.dedent(linha))





saldo = 0
AGENCIA = '00001'
LIMITE_SAQUE = 3
limite = 500
extrato = ""
numero_saques = 0
numero_depositos = 0
usuarios = list()
contas = list()

while True:
    opcao = menu()
    if opcao == "1": #depósito
        valor = float(input('Informe o valor a ser depositado: '.strip()))
        saldo += valor
        numero_depositos += 1

        deposito(saldo, valor, extrato, numero_depositos)

    elif opcao == '2': #sacar
        valor_saque = float(input('Informe o valor de Saque: '))
        valor = valor_saque
        saldo, extrato, numero_saques = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUE
            )

    elif opcao == '3':  # extrato
        exibir_extrato(saldo, extrato=extrato, numero_saques=numero_saques, numero_depositos=numero_depositos)

    elif opcao == '4':
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas.append(conta)

    elif opcao == '5':
        listar_contas(contas)

    elif opcao == '6':
        criar_usuario(usuarios)

    elif opcao == '0':
        print('Operação finalizada, até mais!')
        break
    else:
        print('Opção inválida, tente novamente!')





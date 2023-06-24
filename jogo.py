import sqlite3
from classesecomandos import Pessoa
import classesecomandos as fazer

jogador = 'Jogador'
adm = 'Administrador'
perguntas = 'Perguntas'
diego = Pessoa('diego', None, 'diego.mendesgarcia@gmail.com', None)
try:
    fazer.criartabela(jogador)
    fazer.criartabela(adm)
    fazer.criartabela(perguntas)
except sqlite3.OperationalError:
    pass
try:
    fazer.adicionaradm(diego)
except sqlite3.IntegrityError:
    pass
fazer.limpartela()
while True:
    print(('-------------- Menu Principal --------------\n'
           '1 – Jogar\n'
           '2 – Cadastrar Novo Jogador\n'
           '3 – Recuperar Senha\n'
           '4 – Entrar como Administrador\n'
           '5 – Sair'))
    try:
        o = int(input('Digite sua opção: '))
        fazer.limpartela()
        if o == 1:
            fazer.iniciarjogo()
        elif o == 2:
            email = str(input('email: '))
            j = Pessoa(input('nome: '), input('cpf: '), email=email, senha=str(input('senha: ')))
            fazer.adicionarjogador(j)
        elif o == 3:
            fazer.mandaremail(str(input('email:')))
            fazer.limpartela()
        elif o == 4:
            fazer.entrarcomoadmin(str(input('login:')), str(input('senha:')))
        elif o == 5:
            fazer.limpartela()
            break
        else:
            fazer.limpartela()
            print('Opção invalida,digite uma das opcões:')
    except ValueError:
        fazer.limpartela()
        print('Opção invalida, digite uma das opções: ')

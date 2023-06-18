import sqlite3
import smtplib
import random
import string
from email.message import EmailMessage
from classesecomandos import Pessoa, Perguntas
import classesecomandos as fazer
import ssl

enderecodeemail = 'jogoprojeto40@gmail.com'
senhadeemail = 'pqmkopgytmicxiea'
smtpgmail = 'smtp.gmail.com'
smtp_port = 465
banco = sqlite3.connect('jogo_forca.db')
cursor = banco.cursor()
adm = 'Administrador'
jogador = 'Jogador'
perguntas = 'Perguntas'

'''def criartabela(tipo):
    if tipo == adm:
        cursor.execute('CREATE TABLE Administrador(nome text, email text unique, login text, senha text)')
    elif tipo == jogador:
        cursor.execute('CREATE TABLE Jogador (cpf text unique, nome text, email text, senha text) ')
    elif tipo == perguntas:
        cursor.execute('CREATE TABLE Perguntas (codigo text unique, dica text, palavra text , qmaxima integer )')
    banco.commit()


def alterarpergunta(codigo):
    cursor.execute(f'UPDATE INTO {perguntas} palavra = 
    banco.commit()


def alterarpergunta(codigo):
    cursor.execute(f'update {perguntas} set palavra = "{input("palavra: ")}" where codigo = "{codigo}"')
    cursor.execute(f'update {perguntas} set dica = "{input("dica: ")}" where codigo = "{codigo}"')
    cursor.execute(
        f'update {perguntas} set qmaxima = "{input("quantidade maxima de tentativas: ")}" where codigo = "{codigo}"')
    banco.commit()


def adicionarpergunta(pergunta):
    cursor.execute(
        f'INSERT INTO {perguntas} VALUES("{pergunta.codigo}", "{pergunta.dica}", "{pergunta.palavra}", {pergunta.qmaxima})')
    banco.commit()
    print('adcionado com sucesso')


def adicionarjogador(pessoa):
    cursor.execute(
        f"INSERT INTO Jogador VALUES(\"{pessoa.cpf}\",\"{pessoa.nome}\",\"{pessoa.email}\",\"{pessoa.login}\",\"{pessoa.senha}\")")
    banco.commit()
    print('jogador adicionado com sucesso')


def adicionaradm(pessoa):
    cursor.execute(f'INSERT INTO {adm} VALUES ("{pessoa.nome}"," {pessoa.email}","{pessoa.login}", "{pessoa.senha}")')
    banco.commit()


def deletardobanco(tipo, cpf):
    try:
        cursor.execute(f'DELETE from {tipo} WHERE cpf = {cpf}')
        banco.commit()
        print('Excluido com sucesso')
    except sqlite3.Error as erro:
        print(f'Erro ao exluir: {erro}')


def verbanco(tipo):
    cursor.execute(f'SELECT * FROM {tipo}')
    print(cursor.fetchall())


def gerarsenha(email):
    texto = ''
    letras = string.ascii_letters + string.digits + '!@#$'
    for c in range(5):
        texto += random.choice(letras)
    cursor.execute(f'UPDATE {jogador} SET senha="{texto}" WHERE email = "{email}"')
    banco.commit()
    return texto'''
while True:
    fazer.verbanco(jogador)
    print(('-------------- Menu Principal --------------\n'
           '1 – Jogar\n'
           '2 – Cadastrar Novo Jogador\n'
           '3 – Recuperar Senha\n'
           '4 – Entrar como Administrador\n'
           '5 – Sair'))
    try:
        o = int(input('Digite sua opção: '))
        if o == 1:
            fazer.iniciarjogo()
        elif o == 2:
            email = str(input('email: '))
            j = Pessoa(input('nome: '), input('cpf: '), email=email, senha=str(input('senha: ')))
            fazer.adicionarjogador(j)
        elif o == 3:
            fazer.mandaremail(str(input('email:')))
        elif o == 4:
            fazer.verbanco(adm)
            fazer.entrarcomoadmin(str(input('login:')), str(input('senha:')))
        elif o == 5:
            print('saindo....')
            break
        else:
            print('Opção invalida,digite uma das opcões:')
    except ValueError:
        print('Opção invalida, digite uma das opções: ')

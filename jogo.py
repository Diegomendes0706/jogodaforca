import sqlite3
from classes import Pessoa
banco = sqlite3.connect('jogo_forca.db')
cursor = banco.cursor()
adm = 'Administrador'
jogador = 'Jogador'
p = 'Perguntas'

def criartabela(tipo):
    if tipo == adm:
        cursor.execute('CREATE TABLE Administrador(nome text, email text, login text, senha text)')
    elif tipo == jogador :
        cursor.execute('CREATE TABLE Jogador (cpf text, nome text, email text, login text, senha text) ')
    elif tipo == p:
        cursor.execute('CREATE TABLE Perguntas (pergunta text)')
def adcionaraobanco(tipo,cpf,nome, email,login,senha):
    if tipo == adm:
        login = senha = 'admin'
        cursor.execute(f"INSERT INTO {tipo} VALUES('{input('nome: ')}', {input('email: ')}', '{input('login: ')}', '{input('senha: ')}')")
    elif tipo == jogador:
        cursor.execute(f'INSERT INTO {tipo} VALUES("{cpf}","{nome}","{email}","{login}","{senha}")')
    banco.commit()
    print('adcionado com sucesso')

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


verbanco('Administrador')
while True:
    print(('-------------- Menu Principal --------------\n'
           '1 – Jogar\n'
           '2 – Cadastrar Novo Jogador\n'
           '3 – Recuperar Senha\n'
           '4 – Entrar como Administrador\n'
           '5 – Sair'))
    try:
        o = int(input('Digite sua opção: '))
        if o == 1:
            cpf = str(input('CPF: '))
            senha = input('Senha: ')
        elif o == 2:
            pass
        elif o == 3:
            pass
        elif o == 4:
            pass
        elif o == 5:
            print('saindo....')
            break
        else:
            print('Opção invalida,digite uma das opcões:')
    except ValueError:
        print('Opção invalida, digite uma das opções: ')

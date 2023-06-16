import sqlite3
import smtplib
import random
import string
from email.message import EmailMessage
from classes import Pessoa
import ssl

enderecodeemail = 'diego.mendesgarcia@gmail.com'
senhadeemail = 'oeexoajydwjbokkk'
smtpgmail = 'smtp.gmail.com'
smtp_port = 465
banco = sqlite3.connect('jogo_forca.db')
cursor = banco.cursor()
adm = 'Administrador'
jogador = 'Jogador'
perguntas = 'Perguntas'


def criartabela(tipo):
    if tipo == adm:
        cursor.execute('CREATE TABLE Administrador(nome text, email text, login text, senha text)')
    elif tipo == jogador:
        cursor.execute('CREATE TABLE Jogador (cpf text, nome text, email text, login text, senha text) ')
    elif tipo == perguntas:
        cursor.execute('CREATE TABLE Perguntas (pergunta text)')


def adcionarjogador(pessoa):
    cursor.execute(
        f'INSERT INTO Jogador VALUES("{pessoa.cpf}","{pessoa.nome}","{pessoa.email}","{pessoa.login}","{pessoa.senha}")')
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


def gerarsenha(email):
    texto = ''
    letras = string.ascii_letters + string.digits + '!@#$'
    for c in range(5):
        texto += random.choice(letras)
    cursor.execute(f'UPDATE {jogador} SET senha="{texto}" WHERE email = "{email}"')
    return texto


while True:
    verbanco(jogador)
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
            senha = str(input('Senha: '))
            cursor.execute(f'SELECT COUNT(*) FROM {jogador} WHERE cpf = ? AND senha = ?', (cpf, senha))
            c = cursor.fetchone()
            if c[0] == 0:
                print('login inválido ')
            else:
                cursor.execute(f'SELECT nome FROM {jogador} WHERE cpf = ? ', (cpf,))
                nome = cursor.fetchone()
                nome = nome[0]
                print(f'--------- Menu Jogo da Forca – {nome} --------\n\n'
                      f'     1 – Jogar\n'
                      f'     2 – Atualizar Dados\n'
                      f'     3 – Voltar Menu Principal')

        elif o == 2:
            email = str(input('email: '))
            j = Pessoa(input('nome: '), input('cpf: '), email, login=email, senha=input('senha: '))
            adcionarjogador(j)
        elif o == 3:
            email = str(input('email:'))
            cursor.execute(f'SELECT nome FROM {jogador} WHERE email = ?', (email,))
            nome = cursor.fetchone()
            if nome is None:
                print('O e-mail digitado não esteja cadastrado')
            else:
                print(nome[0])
                destinatario = email
                msg = EmailMessage()
                msg['From'] = enderecodeemail
                msg['To'] = email
                msg['Subject'] = 'Recuperação Senha'
                corpo = f'“Oi {nome[0]}, sua nova senha é {gerarsenha(email)}.'
                msg.set_content(corpo)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtpgmail, smtp_port, context=context) as smtp:
                    smtp.login(enderecodeemail, senhadeemail)
                    smtp.sendmail(enderecodeemail, destinatario, msg.as_string())
        elif o == 4:
            pass
        elif o == 5:
            print('saindo....')
            break
        else:
            print('Opção invalida,digite uma das opcões:')
    except ValueError:
        print('Opção invalida, digite uma das opções: ')

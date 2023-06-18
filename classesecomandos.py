import sqlite3
import smtplib
import random
import os
import string
from email.message import EmailMessage
from unidecode import unidecode
import ssl
import speech_recognition as sr

# variaveis
enderecodeemail = 'jogoprojeto40@gmail.com'
senhadeemail = 'pqmkopgytmicxiea'
smtpgmail = 'smtp.gmail.com'
smtp_port = 465
banco = sqlite3.connect('jogo_forca.db')
cursor = banco.cursor()
adm = 'Administrador'
jogador = 'Jogador'
perguntas = 'Perguntas'


def limpartela():
    os.system('cls')


def ouvirmic():
    microfone = sr.Recognizer()
    with sr.Microphone() as fonte:
        microfone.adjust_for_ambient_noise(fonte)
        audio = microfone.listen(fonte)
        try:
            palavra = microfone.recognize_google(audio, language='pt_BR')
            letra = palavra.replace('letra ', '')
            letra = unidecode(letra)
            print(f'você disse: {palavra}')
        except sr.UnknownValueError:
            print('não entendi')
        return letra


def gerarsenha(email):
    texto = ''
    letras = string.ascii_letters + string.digits + '!@#$'
    for c in range(5):
        texto += random.choice(letras)
    cursor.execute(f'UPDATE {jogador} SET senha="{texto}" WHERE email = "{email}"')
    banco.commit()
    return texto


def mandaremail(email):
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


def entrarcomoadmin(login, senha):
    cursor.execute(f'SELECT COUNT (*) FROM {adm} WHERE login = ? and senha = ?', (login, senha))
    c = cursor.fetchone()
    if c[0] == 0:
        print('Administrador não encontrado')
    else:
        while True:
            print('-------------- Menu Administrador --------------\n'
                  '1 – Cadastrar Nova Pergunta\n'
                  '2 – Atualizar Pergunta\n'
                  '3 – Remover Pergunta\n'
                  '4 – Listar Perguntas\n'
                  '5 – Voltar Menu Principal\n')
            opa = int(input('Digite sua opção: '))
            limpartela()
            if opa == 1:
                codigo = input('codigo: ')
                dica = input('dica: ')
                palavra = str(input('palavra: '))
                qmax = input('quantidade maxima de tentativas: ')
                pergunta = Perguntas(codigo, dica, palavra, qmax)
                adicionarpergunta(pergunta)
                limpartela()
            elif opa == 2:
                verbanco(perguntas)
                codigo = str(input('codigo: '))
                cursor.execute(f'select count(*) from "{perguntas}" where codigo = "{codigo}"')
                c = cursor.fetchone()
                if c[0] == 0:
                    print('pergunta não encontrada')
                    limpartela()
                else:
                    alterarpergunta(codigo)
                    limpartela()
            elif opa == 3:
                codigo = str(input('codigo: '))
                cursor.execute(f'delete from "{perguntas}" where codigo = "{codigo}"')
                limpartela()
            elif opa == 4:
                verbanco(perguntas)
            elif opa == 5:
                break
            else:
                print('opção invalida')


def adicionarpergunta(pergunta):
    cursor.execute(f'INSERT INTO {perguntas} VALUES("{pergunta.codigo}", "{pergunta.dica}", "{pergunta.palavra}",'
                   f' {pergunta.qmaxima})')
    banco.commit()
    print('adcionado com sucesso')


def excluirtabela(tipo):
    cursor.execute(f"DROP TABLE '{tipo}'")
    banco.commit()


def criartabela(tipo):
    if tipo == adm:
        cursor.execute(
            'CREATE TABLE Administrador(nome text, email text unique, login text unique, senha text)')
    elif tipo == jogador:
        cursor.execute(
            'CREATE TABLE Jogador (cpf text unique, nome text, email text not null, senha text not null) ')
    elif tipo == perguntas:
        cursor.execute(
            'CREATE TABLE Perguntas (codigo text unique, dica text, palavra text , qmaxima integer )')
        banco.commit()


def sortearpergunta():
    cursor.execute(f'select dica, palavra, qmaxima from "{perguntas}"')
    registros = cursor.fetchall()
    return random.choice(registros)


def jogar():
    sorteada = sortearpergunta()
    contador = 0
    palavra = str(sorteada[1])
    iconepalavra = '_' * len(sorteada[1])
    while contador < sorteada[2]:
        print(f'------------------ Jogo da Forca -----------------\n'
              f'Dica: {sorteada[0]}\n'
              f'Palavra: {iconepalavra}\n'
              f'Tentativas: {sorteada[2]}\n'
              f'{sorteada[2] - contador}/ {sorteada[2]}\n'
              f'Fale uma letra: (aviso fale: LETRA + (LETRA DE VOCE QUER COLOCAR)')
        letra = ouvirmic()
        while len(letra) != 1:
            print('Fale apenas uma letra')
            letra = ouvirmic()
        indices = []
        for i in range(len(palavra)):
            if palavra[i] == letra:
                indices.append(i)
        if letra in palavra:
            lista = list(iconepalavra)
            for k in indices:
                lista[k] = letra
            iconepalavra = ''.join(lista)
        else:
            contador += 1
        limpartela()
        if '_' not in iconepalavra:
            print('parabens você ganhou')
            break
        if contador == sorteada[2]:
            print('você perdeu')


def mudarjogador(player, atributo, novo):
    cursor.execute(f'update "{jogador}" set "{atributo}" = "{novo}" where cpf = "{player.cpf}"')
    banco.commit()


def verificarjogador(nome, cpf, email, senha):
    cursor.execute(
        f'SELECT COUNT(*) FROM "{jogador}" WHERE cpf = ? AND senha = ? and nome =  ? and email = ?',
        (cpf, senha, nome, email))
    c = cursor.fetchone()
    if c[0] == 0:
        return 'jogador invalido'
    else:
        return Pessoa(nome, cpf, email, senha)


def iniciarjogo():
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
        while True:
            try:
                p = int(input(f'--------- Menu Jogo da Forca – {nome} --------\n\n'
                              f'     1 – Jogar\n'
                              f'     2 – Atualizar Dados\n'
                              f'     3 – Voltar Menu Principal\n\n'
                              f'     Digite sua opção: '))
                if p == 1:
                    jogar()
                elif p == 2:
                    cpf = str(input('cpf: '))
                    nome = str(input('nome: '))
                    email = str(input('email: '))
                    senha = str(input('senha: '))
                    j = verificarjogador(nome, cpf, email, senha)
                    if j != 'jogador invalido':
                        novonome = str(input('novo nome: '))
                        if novonome != ' ':
                            mudarjogador(j, 'nome', novonome)
                            nome = novonome
                        novoemail = str(input('novo email: '))
                        if novoemail != ' ':
                            mudarjogador(j, 'email', novoemail)
                        novasenha = str(input('nova senha: '))
                        if novasenha != ' ':
                            mudarjogador(j, 'senha', novasenha)
                        novocpf = str(input('novo cpf: '))
                        if novocpf != ' ':
                            mudarjogador(j, 'cpf', novocpf)
                            j.cpf = novocpf
                    else:
                        print(j)
                elif p == 3:
                    break
                else:
                    print('opção invalida')
            except ValueError:
                print('opção invalida')


def adicionarjogador(player):
    cursor.execute(
        f"INSERT INTO Jogador VALUES(\"{player.cpf}\",\"{player.nome}\",\"{player.email}\",\"{player.senha}\")")
    banco.commit()
    print('jogador adicionado com sucesso')


def adicionaradm(pessoa):
    cursor.execute(
        f'INSERT INTO {adm} VALUES ("{pessoa.nome}"," {pessoa.email}",admin , admin")')
    banco.commit()


def verbanco(tipo):
    cursor.execute(f'SELECT * FROM {tipo}')
    print(cursor.fetchall())


def alterarpergunta(codigo):
    palavra = input("Nova palavra: ")
    dica = input("Nova dica: ")
    qmaxima = input("Nova quantidade máxima de tentativas: ")
    cursor.execute(
        f'UPDATE perguntas SET palavra = "{palavra}", dica = "{dica}", qmaxima = "{qmaxima}" WHERE codigo = "{codigo}"')
    banco.commit()


def deletardobanco(tipo, cpf):
    try:
        cursor.execute(f'DELETE from {tipo} WHERE cpf = {cpf}')
        banco.commit()
        print('Excluido com sucesso')
    except sqlite3.Error as erro:
        print(f'Erro ao exluir: {erro}')


class Perguntas:
    def __init__(self, codigo, dica, palavra, qmaxima):
        self.codigo = codigo
        self.dica = dica
        self.palavra = palavra
        self.qmaxima = qmaxima


class Pessoa:
    def __init__(self, nome, cpf, email, senha):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha

class Pessoa:
    def __init__(self, nome, cpf, email, login, senha):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.login = login
        self.senha = senha


class Perguntas:
    def __init__(self, codigo, dica, palavra, qmaxima):
        self.codigo = codigo
        self.dica = dica
        self.palavra = palavra
        self.qmaxima = qmaxima

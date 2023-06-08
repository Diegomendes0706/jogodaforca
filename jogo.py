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


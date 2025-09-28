def getJogada():
    letras_para_numeros = {'a': 0, 's': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'j': 6}
    
    while True:
        posicao = input("Qual posição deseja jogar?").strip().lower()

        if posicao in letras_para_numeros:
            posicao = letras_para_numeros[posicao]
        else:
            try:
                posicao = int(posicao) - 1
            except ValueError:
                print("Entrada inválida, tente novamente.")
                continue

        if 0 <= posicao <= 6:
            return posicao
        else:
            print("Posição inválida, Tenta de novo ...")

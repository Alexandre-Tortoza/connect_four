from colors import bcolors

def showTabuleiro(tabuleiro):
    """
    Exibe o tabuleiro atual do jogo no terminal, com cores e símbolos para cada jogador.

    Args:
        tabuleiro (list[list[int]]): Matriz representando o estado atual do tabuleiro.
            - 0: posição vazia
            - 1: peça do jogador humano (vermelho)
            - 2: peça da IA (amarelo)

    Exemplo:
        showTabuleiro([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 0, 0, 0],
            ...
        ])
    """
    print("\n" * 2)
    linhas = len(tabuleiro)
    colunas = len(tabuleiro[0])
    print(f"{bcolors.BLUE}==========================={bcolors.ENDC}")
    print(f"{bcolors.CYAN}[a] [s] [d] [f] [g] [h] [j]{bcolors.ENDC}")
    print(f"{bcolors.BLUE}==========================={bcolors.ENDC}\n")

    for i in range(linhas):
        linha_str = ""
        for j in range(colunas):
            if tabuleiro[i][j] == 0:
                linha_str += "[ ] "
            elif tabuleiro[i][j] == 1:
                linha_str += f"[{bcolors.RED}{bcolors.BOLD}⬤{bcolors.ENDC}] "
            elif tabuleiro[i][j] == 2:
                linha_str += f"[{bcolors.YELLOW}{bcolors.BOLD}⬤{bcolors.ENDC}] "
        print(linha_str)

    print(f"{bcolors.BLUE}==========================={bcolors.ENDC}")


def getJogada():
    """
    Solicita e valida a jogada do jogador humano via entrada no terminal.

    O jogador pode digitar:
        - Uma letra entre 'a' e 'j' (mapeada para colunas 0 a 6)
        - Um número de 1 a 7 (convertido internamente para 0 a 6)

    Returns:
        int: índice da coluna escolhida (entre 0 e 6)

    Exemplo:
        Entrada: 'd' -> Retorna 2
        Entrada: '4' -> Retorna 3
    """
    letras_para_numeros = {'a': 0, 's': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'j': 6}
    while True:
        posicao = input("Qual posição deseja jogar? ").strip().lower()
        if posicao in letras_para_numeros:
            posicao = letras_para_numeros[posicao]
        else:
            try:
                posicao = int(posicao) - 1
            except ValueError:
                print("Entrada inválida...")
                continue
        if 0 <= posicao <= 6:
            return posicao
        print("Posição inválida...")


def escolherDificuldade():
    """
    Exibe o menu de seleção de dificuldade e retorna a escolha do jogador.

    Opções disponíveis:
        1 - Iniciante
        2 - Intermediário
        3 - Profissional

    Returns:
        int: nível de dificuldade escolhido (1, 2 ou 3)

    Exemplo:
        Entrada: 2 -> Retorna 2
    """
    print(f"{bcolors.GREEN}Escolha a dificuldade:{bcolors.ENDC}")
    print("1 - Iniciante")
    print("2 - Intermediário")
    print("3 - Profissional")
    while True:
        try:
            escolha = int(input("Digite sua escolha (1, 2 ou 3): "))
            if escolha in [1, 2, 3]:
                return escolha
            print("Escolha inválida. Digite 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

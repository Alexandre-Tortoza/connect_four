from colors import bcolors

def showTabuleiro(tabuleiro):
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
    letras_para_numeros = {'a': 0, 's': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'j': 6}
    while True:
        posicao = input("Qual posição deseja jogar? ").strip().lower()
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
        print("Posição inválida, tente de novo...")

def escolherDificuldade():
    print(f"{bcolors.GREEN}Escolha o nível de dificuldade:{bcolors.ENDC}")
    print("1 - Iniciante (Minimax básico, profundidade 3)")
    print("2 - Intermediário (Minimax com poda alfa-beta, profundidade 5)")
    print("3 - Profissional (Minimax adaptativo, 3s limite)")
    while True:
        try:
            escolha = int(input("Digite sua escolha (1, 2 ou 3): "))
            if escolha in [1, 2, 3]:
                return escolha
            print("Escolha inválida. Digite 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

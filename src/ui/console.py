
class bcolors:
    RED = '\033[91m'      # vermelho
    YELLOW = '\033[93m'   # amarelo
    BLUE = '\033[94m'     # azul para bordas
    CYAN = '\033[96m'     # azul claro para letras
    BOLD = '\033[1m'
    ENDC = '\033[0m'      # reset de cor

def showTabuleiro(tabuleiro):
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
                # jogador 1 vermelho
                linha_str += f"[{bcolors.RED}{bcolors.BOLD}⬤{bcolors.ENDC}] "
            elif tabuleiro[i][j] == 2:
                # jogador 2 amarelo
                linha_str += f"[{bcolors.YELLOW}{bcolors.BOLD}⬤{bcolors.ENDC}] "
        print(linha_str)
    
    print(f"{bcolors.BLUE}==========================={bcolors.ENDC}")


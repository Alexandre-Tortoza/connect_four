
class bcolors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def showTabuleiro(tabuleiro):
    print("\n" * 130) # por agora vamos fazer dessa forma


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


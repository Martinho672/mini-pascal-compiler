from sys import argv
from sintatico import Sintatico
from tabela import TabelaSimbolos

if __name__ == '__main__':
    ##  Para imprimir a tabela de simbolos digite -t antes de digitar o exemplo nos argumentos
    nome = argv[1]
    nome_saida = 'log_saida.txt'
    tab = None
    tabelaSimbolo = TabelaSimbolos()

    sintatico = Sintatico()
    ok = sintatico.interprete(nome)
    tab = sintatico.importTabela()

    if '-t' in argv:
        indice = argv.index('-t')
        if indice + 1 < len(argv):
            nome_saida = argv[indice + 1]
        if sintatico.interprete(nome):
            print("Arquivo sintaticamente correto")
            tab.escreveTabelaArquivo(nome_saida)
            print(f'Arquivo saida salvo "{nome_saida}"')
    
    if sintatico.interprete(nome):
        tab.escreveTabelaArquivo("log_saida.txt")
        print('Arquivo sintaticamente correto.')

from lexico import Lexico
from lexico import TipoToken as tt
from semantico import Semantico
from tabela import TabelaSimbolos

class Sintatico:
    def __init__ (self):
        self.lex = None
        self.tokenAtual = None
        self.erro = False

    def interprete(self, nomeArquivo):
    
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.tabSimb = TabelaSimbolos()
            self.semantico = Semantico()

            self.PROG()

            # self.consome(tt.FIMARQ)
            self.lex.fechaArquivo()

            return not self.erro

    def atualIgual(self, token):
        (const, _) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual(token):
            (_, msg) = token
            ultimoToken = self.tokenAtual.lexema
            self.tokenAtual = self.lex.getToken()
            return ultimoToken
        
        else:
            self.deuErro = True
            (_, msg) = token
            print(f'ERRO DE SINTAXE [linha {self.tokenAtual.linha}]: era esperado "{msg}" mas veio "{self.tokenAtual.lexema}"')
            quit()
        

#    def verificaExpressaoLogica(self, expressao, linha):
#       if not expressao == tt.LOGICO:
#            msg = "A expressão não retorna um valor lógico."
#            self.semantico.erro(msg, linha)

    def salvaLexama(self):
        return self.tokenAtual.lexema
    
    def salvaLinha(self):
        return self.tokenAtual.linha

    def testaVarNaoDeclarada(self, var, linha):
        if self.deuErro:
            return
        if not self.tabSimb.existeIdent(var):
            self.deuErro = True
            msg = "Variavel " + var + " nao declarada."
            self.semantico.erro(msg, linha)
            quit()

    def importTabela(self):
        return self.tabSimb
        
    def PROG(self):
        self.consome(tt.PROGRAMA)
        self.consome(tt.IDENT)
        self.consome(tt.PVIRG)
        self.DECLS()
        self.C_COMP()

    def DECLS(self):
        if self.atualIgual(tt.VARIAVEIS):
            self.consome(tt.VARIAVEIS)
            self.LIST_DECLS()
        else:
            pass

    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()
    
    def D(self):
        if self.atualIgual(tt.IDENT):
            self.LIST_DECLS()
        else:
            pass
    
    def DECL_TIPO(self):
        ident = self.LIST_ID()
        self.consome(tt.DPONTOS)
        tipo = self.TIPO()
        self.consome(tt.PVIRG)

        if type(ident) == list:
            for i in ident:
                if i in self.tabSimb.tabela:
                    print('Essa variavel ja foi declarada.')
                    quit()
                
                self.tabSimb.declaraIdent(i, tipo)

        else:
            if ident in self.tabSimb.tabela:
                print('Essa variavel ja foi declarada.')
                quit()

            self.tabSimb.declaraIdent(ident, tipo)

    def LIST_ID(self):
        ident = self.consome(tt.IDENT)
        aux = self.E()
        
        if aux != None:
            listAux = []
            listAux.append(ident)
            listAux.extend(aux)

            return listAux

        return ident

    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            return self.LIST_ID()
        else:
            pass

    def TIPO(self):
        if self.atualIgual(tt.INTEIRO):
            return self.consome(tt.INTEIRO)
        elif self.atualIgual(tt.REAL):
            return self.consome(tt.REAL)
        elif self.atualIgual(tt.LOGICO):
            return self.consome(tt.LOGICO)
        elif self.atualIgual(tt.CARACTER):
            return self.consome(tt.CARACTER)

    def C_COMP(self):
        self.consome(tt.ABRECH)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH)

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()
    
    def G(self):
        if self.atualIgual(tt.SE) or self.atualIgual(tt.ENQUANTO) or self.atualIgual(tt.LEIA) or self.atualIgual(tt.ESCREVA) or self.atualIgual(tt.IDENT):
            self.LISTA_COMANDOS()
        else:
            pass

    def COMANDOS(self):
        if self.atualIgual(tt.SE):
            self.IF()
        elif self.atualIgual(tt.ENQUANTO):
            self.WHILE()
        elif self.atualIgual(tt.LEIA):
            self.READ()
        elif self.atualIgual(tt.ESCREVA):
            self.WRITE()
        elif self.atualIgual(tt.IDENT):
            self.ATRIB()

    def IF(self):
        self.consome(tt.SE)
        self.consome(tt.ABREPAR)
        self.EXPR()
        #self.verificaExpressaoLogica(expressao, self.tokenAtual.linha)
        self.consome(tt.FECHAPAR)
        self.C_COMP()
        self.H()

    def H(self):
        if self.atualIgual(tt.SENAO):
            self.consome(tt.SENAO)
            self.C_COMP()
        else:
            pass

    def WHILE(self):
        self.consome(tt.ENQUANTO)
        self.consome(tt.ABREPAR)
        self.EXPR()
        #self.verificaExpressaoLogica(expressao, self.tokenAtual.linha)
        self.consome(tt.FECHAPAR)
        self.C_COMP()

    def READ(self):
        self.consome(tt.LEIA)
        self.consome(tt.ABREPAR)
        aux = self.LIST_ID()
        if (not self.tabSimb.existeIdent(aux)):
            self.semantico.erro(f'Variável {aux} não declarada', self.tokenAtual.linha)
            quit()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    def ATRIB(self):
        lexAux = self.consome(tt.IDENT)
        if (not self.tabSimb.existeIdent(lexAux)):
            self.semantico.erro(f'Variável {lexAux} não declarada', self.tokenAtual.linha)
            quit()
        self.consome(tt.ATRIB)
        self.EXPR()
        self.consome(tt.PVIRG)

    def WRITE(self):
        self.consome(tt.ESCREVA)
        self.consome(tt.ABREPAR)
        self.LIST_W()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_W()
        else:
            pass

    def ELEM_W(self):
        if self.atualIgual(tt.IDENT):
            self.EXPR()
        elif self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
    
    def EXPR(self):
        self.SIMPLES()
        self.P()

    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL)
            self.SIMPLES()
        else:
            pass

    def SIMPLES(self):
        self.TERMO()
        self.R()

    def R(self):
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD)
            self.SIMPLES()
        else:
            pass

    def TERMO(self):
        self.FAT()
        self.S()

    def S(self):
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass

    def FAT(self):
        if self.atualIgual(tt.IDENT):
            lexAux = self.consome(tt.IDENT)
            if (not self.tabSimb.existeIdent(lexAux)):
                self.semantico.erro(f'Variável {lexAux} não declarada', self.tokenAtual.linha)
                quit()
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE)
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR)
            self.EXPR()
            self.consome(tt.FECHAPAR)
        elif self.atualIgual(tt.VERDADEIRO):
            self.consome(tt.VERDADEIRO)
        elif self.atualIgual(tt.FALSO):
            self.consome(tt.FALSO)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.FAT()

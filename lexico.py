# Nome Discente: Fernando Martinho Nascimento   
# Matrícula: 0040886
# Data: 20/05/2023


# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias.


from os import path
from sys import argv

class TipoToken:
    IDENT = (1, 'ID')
    CTE = (2, 'NUM')
    CADEIA = (3, 'CADEIA')
    ATRIB = (4, ':=')
    READ = (5, 'read')
    PVIRG = (6, ';')
    DPONTOS = (7, ':')
    VIRG = (8, ',')
    PRINT = (9, 'print')
    OPAD = (10, 'OPAD')
    OPMUL = (11, 'OPMUL')
    OPREL = (12, 'OPREL')
    OPENEG = (13, '!')
    ABREPAR = (14, '(')
    FECHAPAR = (15, ')')
    ABRECH = (16, '{')
    FECHACH = (17, '}')

    # PALAVARAS RESERVADAS

    ERROR = (18, 'ERRO')
    FIMARQ = (19, 'EOF')
    PROGRAMA = (20, 'PROGRAMA')
    VARIAVEIS = (21, 'VARIAVEIS')
    INTEIRO = (22, 'INTEIRO')
    REAL = (23, 'REAL')  
    LOGICO = (24, 'LOGICO')
    CARACTER = (25, 'CARACTER')
    SE = (26, 'SE')
    SENAO = (27, 'SENAO')
    ENQUANTO = (28, 'ENQUANTO')
    LEIA = (29, 'LEIA')
    ESCREVA = (30, 'ESCREVA')
    FALSO = (31, 'FALSO')
    VERDADEIRO = (32, 'VERDADEIRO')
 

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha

class Lexico:
    # dicionario de palavras reservadas
    reservadas = {
         'PROGRAMA': TipoToken.PROGRAMA,
         'VARIAVEIS': TipoToken.VARIAVEIS,
         'INTEIRO' : TipoToken.INTEIRO,
         'REAL' : TipoToken.REAL,
         'LOGICO' : TipoToken.LOGICO,
         'CARACTER' : TipoToken.CARACTER,
         'SE' : TipoToken.SE,
         'SENAO': TipoToken.SENAO,
         'ENQUANTO' : TipoToken.ENQUANTO,
         'LEIA' : TipoToken.LEIA,
         'ESCREVA' : TipoToken.ESCREVA,
         'FALSO': TipoToken.FALSO,
         'VERDADEIRO': TipoToken.VERDADEIRO,
         }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # fila de caracteres 'deslidos' pelo ungetChar
        self.buffer = ''

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            self.buffer =  ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def verifica_pontos(self,string):
        # verifica se um lexema de um numero real possui mais de 2 pontos
        # retorna um valor True no caso da existência de mais de 1 ponto
        numero_pontos = string.count('.')
        if numero_pontos > 1: 
           return True
        else :
            False 

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c.lower()
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c


    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha += 1
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    
                    estado = 3
                elif car in {'+', '-', '*', '(', ')','{', '}','<', '>', ';', '=', ':', '!', ',', '/'}:
                    if (car == ';'):
                        self.linha += 1
                    estado = 4
                elif car == '"':
                    estado = 6
                else:
                    
                    return Token(TipoToken.ERROR, '*' + car + '*', self.linha)
                
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isalnum()):
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema.upper() in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema.upper()], lexema, self.linha)
                    if not lexema.isascii(): # Verificação se o lexema encontrado não contém caracteres indevidos
                        return Token(TipoToken.ERROR, '*' + lexema + '*', self.linha)
                    else:
                        return Token(TipoToken.IDENT, lexema.upper(), self.linha)
            elif estado == 3:         
                # estado que trata numeros inteiros
                # consumindo numero real 
                lexema = car
                while(str(lexema)[-1] != ' ') and (car.isdigit() or car == '.'):
                    car = self.getChar()
                    lexema += car
                if car is None or (not car.isdigit()):
                    # terminou o numero
                    if self.verifica_pontos(lexema) :
                        return Token(TipoToken.ERROR, lexema, self.linha)
                    self.ungetChar(car)
                    
                    return Token(TipoToken.CTE, lexema, self.linha)
              

                return Token(TipoToken.ERROR, '*' + car + '*', self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                # TODO: tratar '>=' '<=' '<>' ':='
                lexema = lexema + car
                if lexema == ':=':
                    return Token(TipoToken.ATRIB, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PVIRG, lexema,self.linha)
                elif car == ':':
                    car = self.getChar() # ':='
                    lexema += car
                    if lexema == ':=':
                        return Token(TipoToken.ATRIB,lexema, self.linha)
                    else:
                        self.ungetChar(car)
                    return Token(TipoToken.DPONTOS, lexema, self.linha)

                elif car == '=':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '+':
                    return Token(TipoToken.OPAD, lexema,self.linha)
                elif car == '-':
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.OPMUL, lexema,self.linha)
                elif car == '/':
                    lexema = car
                    lexema += self.getChar()
                    if (lexema == '//' or lexema == '/*'):
                        estado = 5
                    else : 
                        self.ungetChar(lexema)
                        lexema = ''
                        return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.ABREPAR, lexema ,self.linha)
                elif car == ')':
                    return Token(TipoToken.FECHAPAR, lexema ,self.linha)
                elif car == '{':
                    return Token(TipoToken.ABRECH, lexema ,self.linha)
                elif car == '}':
                    return Token(TipoToken.FECHACH, lexema ,self.linha)
                elif car == '>':
                    car = self.getChar() # '>='
                    lexema += car
                    if lexema == '>=':
                        return Token(TipoToken.OPREL,lexema, self.linha)
                    else:
                        self.ungetChar(car)
                    return Token(TipoToken.OPREL, lexema ,self.linha)
                elif car == '<' :
                    car = self.getChar() # '<='
                    lexema += car
                    if lexema == '<=':
                        return Token(TipoToken.OPREL,lexema, self.linha)
                    elif lexema == '<>':
                        return Token(TipoToken.OPREL, lexema, self.linha)
                    else:
                        self.ungetChar(car)
                    return Token(TipoToken.OPREL, lexema ,self.linha)
                elif car == '!':
                    return Token(TipoToken.OPENEG, lexema, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, lexema, self.linha)

            
            elif estado == 5:
                # consumindo comentario
                if(lexema == '//'):
                    car = self.getChar() 
                    while (car != '\n'):
                        lexema += car   
                        car = self.getChar()
                    self.ungetChar(car)
                    lexema = ''
                    estado = 1
                  
                elif lexema == '/*':
                    car = self.getChar()
                    while (car != '*'):
                        lexema += car
                        car = self.getChar()
                        if (car == '*'):
                            lexema += car
                            car = self.getChar()
                            if (car == '/'):
                                lexema += car
                                break
                            else:
                                return Token(TipoToken.ERROR, lexema, self.linha)
                    lexema = ''
                    estado = 1

            elif estado == 6:
                car = self.getChar()
                while (car != '"'):
                    lexema += car
                    car = self.getChar()
                return Token(TipoToken.CADEIA, lexema, self.linha)


if __name__== "__main__":

   nome = argv[1]
   lex = Lexico(nome)
   lex.abreArquivo()

   print('Processando...')
   while(True):
       
       token = lex.getToken()
       print("token= %s  lexema= (%s)" % (token.msg, token.lexema))
       if token.const == TipoToken.ERROR[0]:
           print('Erros foram encontrados')
           break
       if token.const == TipoToken.FIMARQ[0]:
           print('SUCESSO!')
           break
   lex.fechaArquivo()

from random import choice

class Palavra:
    def __init__(self, arquivo):
        self.arquivo = open(arquivo, 'r')
        self.palavras = self.palavrasDoArquivo(self.arquivo) 
        self.palavra_secreta = self.sortear(self.palavras)
        self.palavras_sorteadas = [self.palavra_secreta]
        self.arquivo.close()

    def sortear_nova(self):
        nova_palavra = self.sortear(self.palavras)
        while nova_palavra in self.palavras_sorteadas:
            nova_palavra = self.sortear(self.palavras) 
        self.palavra_secreta = nova_palavra

    def palavrasDoArquivo(self, arquivo):
        palavras = []
        for linha in self.arquivo:
            palavras.append(linha.strip().upper())
        return palavras
    
    def sortear(self, palavras):
        return choice(palavras)
    
    def tem(self, letra):
        return letra.upper() in self.palavra_secreta
    
    def esconder(self):
        self.palavra_escondida = []
        for letra in self.palavra_secreta:
            self.palavra_escondida.append('__')
    
    def revelar(self, letra):
        for posicao, letraDaPalavra in enumerate(self.palavra_secreta):
            if letra.upper() == letraDaPalavra:
                self.palavra_escondida[posicao] = letra

    def estaCompleta(self):
        return '__' not in self.palavra_escondida

class Jogo:
    def __init__(self, arquivo):
        self.palavra_secreta = Palavra(arquivo)
        self.novoJogo()

    def novoJogo(self):
        self.chutes = 0
        self.chances= 6
        self.palavra_secreta.sortear_nova()
        self.palavra_secreta.esconder()
        self.historico_chutes = []

    def chutar(self, letra):
        self.chutes += 1
        letra = letra.upper()
        if letra not in self.historico_chutes:
            self.historico_chutes.append(letra)
            if self.palavra_secreta.tem(letra):
                self.palavra_secreta.revelar(letra)
                return True
            else:
                self.chances -= 1
        return False

    def ganhou(self):
        return True if self.palavra_secreta.estaCompleta() else False
    
    def perdeu(self):
        return True if self.chances <= 0 else False
        

if(__name__ == "__main__"):
    jogo = Jogo("palavras.txt") 
    while True:
        while not jogo.ganhou() and not jogo.perdeu():
            print(jogo.palavra_secreta.palavra_escondida)
            letra = input()
            jogo.chutar(letra)
        if jogo.ganhou():
            print("Você sobreviveu, desta vez...")
        else:
            print("Chegou a sua hora!")
        if input("Deseja jogar de novo?") == 'sim':
            jogo.novoJogo()


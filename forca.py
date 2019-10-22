class Palavra:
    def __init__(self, arquivo):
        self.arquivo = open(arquivo, 'r', encoding='utf-8')
        self.palavras = self.palavrasDoArquivo(self.arquivo) 
        self.palavras_sorteadas = []
        self.palavra_secreta = self.sortear(self.palavras)
        self.palavras_sorteadas.append(self.palavra_secreta)
        self.esconder()
        self.arquivo.close()

    def palavrasDoArquivo(self, arquivo):
        palavras = []
        for linha in self.arquivo:
            palavras.append(linha.strip().upper())
        return palavras
    
    def sortear(self, palavras):
        from random import choice
        palavras_nao_sorteadas = list(set(self.palavras) - set(self.palavras_sorteadas))
        nova_palavra = choice(palavras_nao_sorteadas)
        return nova_palavra
    
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
        self.arquivo = arquivo
        self.novoJogo()

    def novoJogo(self):
        self.chutes = 0
        self.chances= 6
        self.palavra_secreta = Palavra(self.arquivo)
        self.historico_chutes = []

    def chutar(self, letra):
        self.chutes += 1
        letra = letra.upper()
        if self.eh_valido(letra):
            if letra not in self.historico_chutes:
                self.historico_chutes.append(letra)
                if self.palavra_secreta.tem(letra):
                    self.palavra_secreta.revelar(letra)
                    return True
                else:
                    self.chances -= 1
        return False
    def eh_valido(self, letra):
        if len(letra) == 1 and letra.isalpha():
            return True
        return False
    def ganhou(self):
        return True if self.palavra_secreta.estaCompleta() else False
    
    def perdeu(self):
        return True if self.chances <= 0 else False
        

if(__name__ == "__main__"):
    jogo = Jogo("palavras.txt") 
    while True:
        while not jogo.ganhou() and not jogo.perdeu():
            print("--------------------------")
            print(f'Vidas: {jogo.chances}')
            print(jogo.palavra_secreta.palavra_escondida)
            print(f'Chutes: {jogo.historico_chutes}')
            print("--------------------------")
            letra = input()
            jogo.chutar(letra)
        if jogo.ganhou():
            print("Você sobreviveu, desta vez...")
        else:
            print("Chegou a sua hora!")
        if input("Deseja jogar de novo?") == 'sim':
            jogo.novoJogo()



from flask import Flask, render_template, url_for, request
from forca import Jogo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'morte'
jogo = Jogo('palavras.txt')
errors = {
    'chute_invalido' : 'Chute inválido, você está tentando enganar a morte?',
    'ganhou': 'Mas que proeza, esse é o primeiro ser que escapa da morte',
    'perdeu': 'Sua hora chegou!',
    'errou': 'Continue assim, que você morrerá logo logo',
    'acertou': 'Essa foi por pouco mas na próxima você morre!'
}
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/jogar', methods=['GET', 'POST'])
def jogar():
    mensagem_feedback = ''
    if request.method == 'POST':
        letra = request.form['letra']
        if validar_chute(letra):
            acertou = jogo.chutar(letra)
            if acertou:
                mensagem_feedback = errors['acertou']                    
            else:
                mensagem_feedback = errors['errou']                    
        else:
            mensagem_feedback = errors['chute_invalido']
        if jogo.ganhou():
            mensagem_feedback = errors['ganhou']
        elif jogo.perdeu():
            mensagem_feedback = errors['perdeu']
    else:
        jogo.novoJogo()
    return render_template('game.html', jogo = jogo, mensagem_feedback = mensagem_feedback)

@app.route('/jogar', methods=['GET'])
def novo_jogo():
    jogo.novoJogo()
    return render_template('game.html', jogo = jogo)

def validar_chute(chute):
    if len(chute) == 1 and chute.isalpha():
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
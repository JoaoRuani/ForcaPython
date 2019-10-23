import os
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
        if jogo.eh_valido(letra):
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
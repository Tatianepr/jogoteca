from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time

@app.route('/')
def index():
    # query que retorna todos os jogos em ordem pelo campo jogos
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # monta a url incluindo novamente a querystring da próxima página
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    # verifica se nome do jogo já está cadastrado.
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    # instancia Jogos passando todas as informações preenchidas
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    # adiciona o novo jogo no banco de dados
    db.session.add(novo_jogo)
    #commita o insert
    db.session.commit()

    arquivo = request.files['arquivo']
    # pega a variável universal que tem o caminho da pasta upload e grava o arquivo com nome do ID do jogo
    upload_def = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_def}/capa{novo_jogo.id}-{timestamp}.jpg')

    # a função url_for redireciona para a função do route. é uma boa prática
    return redirect(url_for('index'))

# passa o id do registro selecionado na lista - <int:id>
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # monta a url incluindo novamente a querystring da próxima página
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    # busca no banco dados do jogo pelo ID informado
    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)
    # passa como parâmetro da pagina de retorno o título e os dados do jogo
    # return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo, form=form)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_def = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_def}/capa{jogo.id}-{timestamp}.jpg')

    return redirect( url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # monta a url incluindo novamente a querystring da próxima página
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))



@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


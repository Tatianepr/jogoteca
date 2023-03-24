from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    #recupera informação passada na querystring
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    # executa uma query que filtra pelo nickname recebido do forme.
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    # passa a senha criptografada para validar no banco
    senha = check_password_hash(usuario.senha, form.senha.data)

    # verifica se o usuario enviado no form está no retorno da query
    if usuario and senha:
        # guarda o usuário logado nos cookies do navegador
        session['usuario_logado'] = usuario.nickname
        # envia uma menssagem padrão de sucesso
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        # retorna para a página próxima
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))
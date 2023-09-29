from flask import render_template, redirect, url_for, flash, request
from vagasdeestacionamento import app, database, bcrypt
from vagasdeestacionamento.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormVaga
from vagasdeestacionamento.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

#link da página
@app.route('/', methods=['GET', 'POST'])

# O que aparece na página
def home():
    form_vaga = FormVaga()
    if form_vaga.validate_on_submit():
       #  current_user.email = form_vaga.email.data
       #  current_user.username = form_vaga.username.data
       # current_user.placa = form_vaga.placa.data
       # current_user.vagas = atualizar_vagas(form_vaga)
        database.session.commit()
        flash(f'A VAGA ESTÁ DISPONÍVEL!', 'alert-success')
        return redirect(url_for('home'))
    #elif request.method == 'GET':
       #form_vaga.email.data = current_user.email
       #form_vaga.username.data = current_user.username
       #form_vaga.placa.data = current_user.placa
   # for vaga in current_user.vagas.split(";"):
    #    for campo in form_vaga:
     #       if vaga in campo.label.text:
      #          campo.data = True

    return render_template('home.html', form_vaga=form_vaga)

@app.route('/local')
def local():
    return render_template('local.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
            return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos.', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_vagas(form):
   lista_vagas = []
   for campo in form:
       if 'vaga_' in campo.name:
           if campo.data:
              lista_vagas.append(campo.label.text)
   return ';'.join(lista_vagas)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.placa = form.placa.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.vagas = atualizar_vagas(form)
        database.session.commit()
        flash(f'Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.placa.data = current_user.placa
        for vaga in current_user.vagas.split(";"):
            for campo in form:
                if vaga in campo.label.text:
                    campo.data = True


    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)
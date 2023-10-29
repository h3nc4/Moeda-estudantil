#  Copyright 2023 Henrique Almeida, Gabriel Dolabela, João Pauletti
# 
# This file is part of Moeda estudantil.
# 
# Moeda estudantil is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# 
# Moeda estudantil is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
# 
# You should have received a copy of the GNU Affero
# General Public License along with Moeda estudantil. If not, see
# <https://www.gnu.org/licenses/>.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as unlog, login as log_user
from django.contrib.auth.hashers import make_password
from django.db.models import F
from django.http import HttpResponseNotAllowed
import base64
from .models import *

# Página inicial
def index(request):
    return render(request, 'index.html', {'turmas': Turma.objects.all().count(), 'semestre': Enum.objects.first().semestre})

# Faz o login de um usuário e o redireciona para a página inicial
def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('nome'), password=request.POST.get('senha'))
        if user:
            log_user(request, user)
            return redirect('/')
        return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos.'})
    return render(request, 'login.html')

# Faz o logout de um usuário e o redireciona para a página inicial
def logout(request):
    unlog(request)
    return redirect('/')

# Página de cadastro de professor, apenas envia o template e o tipo de usuário para a função de cadastro
def cadastro_professor(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return err403(request)
    return cadastro(request, template_name='cadastro_professor.html', user_type='professor')

# Página de cadastro de empresa, apenas envia o template e o tipo de usuário para a função de cadastro
def cadastro_empresa(request):
    return cadastro(request, template_name='cadastro_empresa.html', user_type='empresa')

# Página de cadastro, por padrão realiza o cadastro de um aluno, mas pode ser usado para outros tipos de usuário
def cadastro(request, template_name='cadastro.html', user_type='aluno'):
    if request.method == 'POST':
        # Pega os dados em comum entre os todos os tipos de usuário
        nome = request.POST.get('nome')
        senha_crua = request.POST.get('senha')
        email = request.POST.get('email')
        if not (nome and senha_crua):
            return render(request, template_name, {'erro': 'Preencha todos os campos.'})
        # Verifica se o usuário já existe
        if Usuario.objects.filter(username=nome):
            return render(request, template_name, {'erro': 'Usuário já cadastrado.'})

        # Usado para enviar o objeto criado para o usuário
        tipo_e_objeto = {}

        # Se o usuário for um aluno, cria um endereço e um aluno
        if user_type == 'aluno':
            cpf = request.POST.get('cpf')
            rg = request.POST.get('rg')
            estado = request.POST.get('estado')
            cidade = request.POST.get('cidade')
            bairro = request.POST.get('bairro')
            rua = request.POST.get('rua')
            numero = request.POST.get('numero')
            complemento = request.POST.get('complemento')
            if not (email and cpf and rg and estado and cidade and bairro and rua and numero):
                return render(request, template_name, {'erro': 'Preencha os campos obrigatórios.'})

            tipo_e_objeto['aluno'] = Aluno.objects.create(cpf=cpf, rg=rg, 
                # Cria o endereço ou pega um já existente com os mesmos dados
                endereco=Endereco.objects.get_or_create(
                    estado=estado, cidade=cidade, bairro=bairro, rua=rua, numero=numero, complemento=complemento
                )[0]
            )

        # Se o usuário for um professor, cria um professor
        elif user_type == 'professor':
            cpf = request.POST.get('cpf')
            if not cpf:
                return render(request, template_name, {'erro': 'Preencha todos os campos.'})
            tipo_e_objeto['professor'] = Professor.objects.create(cpf=cpf)

        # Se o usuário for uma empresa, cria uma empresa
        elif user_type == 'empresa':
            tipo_e_objeto['empresa'] = Empresa.objects.create()
        usuario = Usuario.objects.create(username=nome, password=make_password(senha_crua), email=email, **tipo_e_objeto)
        if user_type != 'professor':
            log_user(request, usuario)
        return redirect('/')
    return render(request, template_name)

# Página principal para empresas
def empresa(request):
    if not request.user.is_authenticated or not request.user.empresa:
        return err403(request)
    return render(request, 'empresa.html', {'vantagens': request.user.empresa.vantagem_set.all()})

# Página para adicionar uma nova vantagem
def nova_vantagem(request):
    if not request.user.is_authenticated or not request.user.empresa:
        return err403(request)
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        imagem = request.FILES.get('imagem')
        if not (valor and imagem):
            return render(request, 'nova_vantagem.html', {'erro': 'Preencha todos os campos.'})
        Vantagem.objects.create(descricao=descricao, valor=valor, empresa=request.user.empresa, imagem=base64.b64encode(imagem.read()).decode('utf-8'))
        return redirect('/empresa/')
    return render(request, 'nova_vantagem.html')

# Avança o semestre, adicionando moedas para os professores
def avanca_semestre(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return err403(request)
    Professor.objects.all().update(moedas=F('moedas') + 1000)
    sys_config = Enum.objects.first()
    sys_config.semestre += 1
    sys_config.save()
    return redirect('/')

# Página de turmas
def turmas(request):
    if not request.user.is_authenticated or (not request.user.professor and not request.user.aluno):
        return err403(request)
    if request.method == 'POST':
        turma = request.POST.get('turma')
        if not turma:
            return render(request, 'turmas.html', {'erro': 'Selecione uma turma.'})
        if request.user.aluno:
            request.user.aluno.turmas.add(Turma.objects.get(id=turma))
        elif request.user.professor:
            request.user.professor.turmas.add(Turma.objects.get(id=turma))
        return redirect('/')
    return render(request, 'turmas.html', {'suas_turmas': request.user.aluno.turmas.all() if request.user.aluno else request.user.professor.turmas.all(), 'turmas': Turma.objects.all()})

# Página de uma turma
def turma(request, id):
    if not request.user.is_authenticated or not request.user.professor:
        return err403(request)
    turma = Turma.objects.get(id=id)
    return render(request, 'turma.html', {'professor': turma.professor_set.first(), 'alunos': turma.aluno_set.all(), 'turma': turma})

# Página de cadastro de turmas, cria e insere uma turma no banco de dados
def cadastrar_turma(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return err403(request)
    Turma.objects.create()
    return redirect('/')

def enviar_moeda(request, id):
    if not request.user.is_authenticated or not request.user.professor:
        return err403(request)
    aluno = Usuario.objects.get(id=id).aluno
    professor = request.user.professor
    if request.method == 'POST':
        moedas = request.POST.get('quantidade_moedas')
        mensagem = request.POST.get('mensagem')
        if not moedas:
            return render(request, 'error.html', {'erro': 'Preencha todos os campos.'})
        try:
            moedas = int(moedas)
        except:
            return render(request, 'error.html', {'erro': 'São aceitos apenas números inteiros.'})
        if moedas < 0:
            return render(request, 'error.html', {'erro': 'Não é possível enviar moedas negativas.'})
        if moedas > request.user.professor.moedas:
            return render(request, 'error.html', {'erro': 'Você não tem moedas suficientes.'})
        professor.moedas -= moedas
        professor.save()
        aluno.moedas += moedas
        aluno.save()
        Transacao.objects.create(moedas=moedas, mensagem=mensagem, de=request.user, para=aluno.usuario)
        return redirect('/')
    return HttpResponseNotAllowed(['POST'])

# Página de vantagens
def vantagens(request):
    if not request.user.is_authenticated or not request.user.aluno:
        return err403(request)
    return render(request, 'vantagens.html', {
        'vantagens': Vantagem.objects.exclude(id__in=request.user.aluno.vantagens.values_list('id', flat=True)),
        'compradas': request.user.aluno.vantagens.all()
    })

# Compra de uma vantagem
def vantagem(request, id):
    if not request.user.is_authenticated or not request.user.aluno:
        return err403(request)
    vantagem = Vantagem.objects.get(id=id)
    aluno = request.user.aluno
    if request.method == 'POST':
        if aluno.moedas < vantagem.valor:
            return render(request, 'error.html', {'erro': 'Você não tem moedas suficientes.'})
        aluno.moedas -= vantagem.valor
        aluno.vantagens.add(vantagem)
        aluno.save()
        Transacao.objects.create(moedas=vantagem.valor, de=aluno.usuario, para=vantagem.empresa.usuario)
        return redirect('/')
    return HttpResponseNotAllowed(['POST'])

def historico(request):
    if not request.user.is_authenticated:
        return err403(request)
    enviadas = Transacao.objects.filter(de=request.user)
    recebidas = Transacao.objects.filter(para=request.user)
    total = 0
    for t in enviadas:
        total -= t.moedas
    for t in recebidas:
        total += t.moedas
    return render(request, 'historico.html', {
        'transacoes_enviadas': enviadas,
        'transacoes_recebidas': recebidas,
        'moedas': total
    })

# Página de erro 403, 'forbidden'
def err403(request):
    return render(request, '403.html', status=403)

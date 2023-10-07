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

from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import logout as _logout
from django.contrib.auth import login as _login

from .models import *

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(request, username=nome, password=senha)
        if user:
            _login(request, user)
            return HttpResponse(f'<script>window.location.href = "/"</script>')
        return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos.'})
    return render(request, 'login.html')

def logout(request):
    _logout(request)
    return HttpResponse(f'<script>window.location.href = "/"</script>')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        rg = request.POST.get('rg')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')
        if not (nome and senha and email and cpf and rg and estado and cidade and bairro and rua and numero):
            return render(request, 'cadastro.html', {'erro': 'Preencha os campos obrigatórios.'})
        if Usuario.objects.filter(username=nome):
            return render(request, 'cadastro.html', {'erro': 'Usuário já cadastrado.'})
        endereco = Endereco.objects.filter(estado=estado, cidade=cidade, bairro=bairro, rua=rua, numero=numero, complemento=complemento)
        if endereco:
            endereco = endereco[0]
        else:
            endereco = Endereco.objects.create(estado=estado, cidade=cidade, bairro=bairro, rua=rua, numero=numero, complemento=complemento)
            endereco.save()
        aluno = Aluno.objects.create(email=email, cpf=cpf, rg=rg, endereco=endereco)
        usuario_aluno = Usuario.objects.create(username=nome, password=senha, aluno=aluno)
        usuario_aluno.save()
        aluno.save()
        _login(request, usuario_aluno)
        return HttpResponse(f'<script>window.location.href = "/"</script>')
    return render(request, 'cadastro.html')

def cadastro_professor(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        if not (nome and senha and cpf):
            return render(request, 'cadastro_professor.html', {'erro': 'Preencha todos os campos.'})
        if Usuario.objects.filter(username=nome):
            return render(request, 'cadastro_professor.html', {'erro': 'Usuário já cadastrado.'})
        professor = Professor.objects.create(cpf=cpf)
        usuario_prof = Usuario.objects.create(username=nome, password=senha, professor=professor)
        usuario_prof.save()
        professor.save()
        _login(request, usuario_prof)
        return HttpResponse(f'<script>window.location.href = "/"</script>')
    return render(request, 'cadastro_professor.html')

def cadastro_empresa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        if not (nome and senha):
            return render(request, 'cadastro_empresa.html', {'erro': 'Preencha todos os campos.'})
        if Usuario.objects.filter(username=nome):
            return render(request, 'cadastro_empresa.html', {'erro': 'Usuario já cadastrada.'})
        empresa = Usuario.objects.create(username=nome, password=senha, e_empresa=True)
        empresa.save()
        _login(request, empresa)
        return HttpResponse(f'<script>window.location.href = "/"</script>')
    return render(request, 'cadastro_empresa.html')
    
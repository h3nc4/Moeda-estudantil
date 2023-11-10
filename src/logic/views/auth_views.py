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
from django.contrib.auth import authenticate, logout as logoff, login as logon
from django.contrib.auth.hashers import make_password
from ..models import Usuario, Aluno, Professor, Empresa, Endereco
from ..permissions import somente_super

# Faz o login de um usuário e o redireciona para a página inicial
def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    user = authenticate(request, username=request.POST.get('nome'), password=request.POST.get('senha'))
    if not user:
        return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos.'})
    logon(request, user)
    return redirect('/')

# Faz o logout de um usuário e o redireciona para a página inicial
def logout(request):
    logoff(request)
    return redirect('/')

# Página de cadastro de professor, apenas envia o template e o tipo de usuário para a função de cadastro
@somente_super
def cadastro_professor(request):
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
            logon(request, usuario)
        return redirect('/')
    return render(request, template_name)

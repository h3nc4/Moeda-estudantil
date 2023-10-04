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

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(request, username=nome, password=senha)
        if user:
            _login(request, user)
            alert_message = 'Usuário logado com sucesso'
            return HttpResponse(f'<script>alert("{alert_message}"); window.location.href = "/";</script>')
        alert_message = 'Usuário ou senha incorretos'
        return HttpResponse(f'<script>alert("{alert_message}"); window.location.href = "/login/";</script>')
    return render(request, 'login.html')

def logout(request):
    _logout(request)
    return HttpResponse(f'<script>alert("Usuário deslogado com sucesso"); window.location.href = "/";</script>')

def cadastro(request):
    #if request.method == 'POST':

        # Lógica de cadastro

        #usuario.save()
        #_login(request, usuario)
        #return HttpResponse(f'<script>alert("Usuário cadastrado com sucesso"); window.location.href = "/";</script>')
    return render(request, 'cadastro.html')

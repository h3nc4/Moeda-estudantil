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
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

from django.shortcuts import render
from django.http import HttpResponseNotAllowed

# Página de erro 403, 'forbidden'
def err403(request):
    return render(request, '403.html', status=403)

def somente_super(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return err403(request)
        return view_func(request, *args, **kwargs)
    return wrapper

def somente_empresa(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.empresa:
            return err403(request)
        return view_func(request, *args, **kwargs)
    return wrapper

def somente_aluno(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.aluno:
            return err403(request)
        return view_func(request, *args, **kwargs)
    return wrapper

def somente_professor(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.professor:
            return err403(request)
        return view_func(request, *args, **kwargs)
    return wrapper

def ou_professor_ou_aluno(view_func):
    def wrapper(request, *args, **kwargs):
        if not (request.user.aluno or request.user.professor):
            return err403(request)
        return view_func(request, *args, **kwargs)
    return wrapper

def somente_autenticado(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return err403(request)
        return view_func(request, *args, **kwargs)
    return wrapper

def somente_post(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        return view_func(request, *args, **kwargs)
    return wrapper

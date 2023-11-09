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
from django.http import HttpResponseNotAllowed
from .error_views import err403
from ..models import Usuario, Turma, Vantagem, Transacao

# Inscreve um usuário em uma turma, aceita apenas POST
def enturmar(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    turma = request.POST.get('turma')
    if not turma:
        return render(request, 'turmas.html', {'erro': 'Selecione uma turma.'})
    if request.user.aluno:
        request.user.aluno.turmas.add(Turma.objects.get(id=turma))
    elif request.user.professor:
        request.user.professor.turmas.add(Turma.objects.get(id=turma))
    return redirect('/turmas/')

# Envio de moedas, aceita apenas POST
def enviar_moeda(request, id):
    if not request.user.professor:
        return err403(request)
    aluno_usr = Usuario.objects.get(id=id).aluno.usuario
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    moedas = request.POST.get('quantidade_moedas')
    mensagem = request.POST.get('mensagem')
    if not moedas:
        return render(request, 'error.html', {'erro': 'Preencha todos os campos.'})
    try:
        moedas = int(moedas)
    except ValueError:
        return render(request, 'error.html', {'erro': 'São aceitos apenas números inteiros.'})
    if moedas < 0:
        return render(request, 'error.html', {'erro': 'Não é possível enviar moedas negativas.'})
    if moedas > request.user.moedas:
        return render(request, 'error.html', {'erro': 'Você não tem moedas suficientes.'})
    request.user.moedas -= moedas
    request.user.save() # Professor
    aluno_usr.moedas += moedas
    aluno_usr.save()
    Transacao.objects.create(moedas=moedas, mensagem=mensagem, de=request.user, para=aluno_usr)
    return redirect('/')

# Compra de uma vantagem, aceita apenas POST
def comprar(request, id):
    if not request.user.aluno:
        return err403(request)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    vantagem = Vantagem.objects.get(id=id)
    aluno_usr = request.user
    if aluno_usr.moedas < vantagem.valor:
        return render(request, 'error.html', {'erro': 'Você não tem moedas suficientes.'})
    aluno_usr.moedas -= vantagem.valor
    aluno_usr.save()
    aluno_usr.aluno.vantagens.add(vantagem)
    aluno_usr.aluno.save()
    Transacao.objects.create(moedas=vantagem.valor, de=aluno_usr, para=vantagem.empresa.usuario, vantagem_comprada=vantagem)
    return redirect('/vantagens/')

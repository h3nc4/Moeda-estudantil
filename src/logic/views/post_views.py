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

from django.shortcuts import render, redirect, get_object_or_404
from ..utils import mail
from ..models import Usuario, Turma, Vantagem, Transacao
from ..permissions import somente_professor, somente_aluno, somente_post, ou_professor_ou_aluno

# Inscreve um usuário em uma turma, aceita apenas POST
@somente_post
@ou_professor_ou_aluno
def enturmar(request):
    turma_id = request.POST.get('turma')
    if not turma_id:
        return render(request, 'turmas.html', {'erro': 'Selecione uma turma.'})
    aluno_prof = getattr(request.user, 'aluno', None) or getattr(request.user, 'professor', None)
    if aluno_prof:
        aluno_prof.turmas.add(get_object_or_404(Turma, id=turma_id))
    return redirect('/turmas/')

# Envio de moedas, aceita apenas POST
@somente_post
@somente_professor
def enviar_moeda(request, id):
    aluno_usr = get_object_or_404(Usuario, id=id).aluno.usuario
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
    mail("O professor " + request.user.username + " enviou moedas para você",
        "email/profmoedas.html", {
            'user': aluno_usr.username,
            'professor': request.user.username,
            'moedas': moedas,
            'mensagem': mensagem,
        }, aluno_usr.email)
    request.user.moedas -= moedas
    request.user.save() # Professor
    aluno_usr.moedas += moedas
    aluno_usr.save()
    Transacao.objects.create(moedas=moedas, mensagem=mensagem, de=request.user, para=aluno_usr)
    return redirect('/historico/')

# Compra de uma vantagem, aceita apenas POST
@somente_post
@somente_aluno
def comprar(request, id):
    vantagem = get_object_or_404(Vantagem, id=id)
    aluno_usr = request.user
    empresa_usr = vantagem.empresa.usuario
    if aluno_usr.moedas < vantagem.valor:
        return render(request, 'error.html', {'erro': 'Você não tem moedas suficientes.'})
    aluno_usr.moedas -= vantagem.valor
    aluno_usr.save()
    aluno_usr.aluno.vantagens.add(vantagem)
    aluno_usr.aluno.save()
    transacao = Transacao.objects.create(moedas=vantagem.valor, de=aluno_usr, para=vantagem.empresa.usuario, vantagem_comprada=vantagem)
    mail("O aluno " + aluno_usr.username + " comprou uma vantagem",
        "email/nota_fiscal.html", {
            'aluno': aluno_usr.username,
            'empresa': empresa_usr.username,
            'vantagem': vantagem.descricao,
            'cupom': transacao.codigo,
        }, empresa_usr.email)
    return redirect('/vantagens/')

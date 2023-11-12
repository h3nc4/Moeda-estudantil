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
from django.db.models import F
from ..models import Usuario, Turma, Vantagem, Transacao, Enum
from ..permissions import *

# Página inicial
def index(request):
    return render(request, 'index.html', {'turmas': Turma.objects.all().count(), 'semestre': Enum.objects.first().semestre})

# Página principal para empresas
@somente_empresa
def empresa(request):
    return render(request, 'empresa/empresa.html', {'vantagens': request.user.empresa.vantagem_set.all()})

# Página para adicionar uma nova vantagem
@somente_empresa
def nova_vantagem(request):
    if request.method != 'POST':
        return render(request, 'empresa/nova_vantagem.html')
    descricao = request.POST.get('descricao')
    valor = request.POST.get('valor')
    imagem = request.FILES.get('imagem')
    if not (valor and imagem):
        return render(request, 'empresa/nova_vantagem.html', {'erro': 'Preencha todos os campos.'})
    Vantagem.objects.create(descricao=descricao, valor=valor, empresa=request.user.empresa, imagem=imagem.read())
    return redirect('/empresa/')

# Avança o semestre, adicionando moedas para os professores
@somente_super
def avanca_semestre(request):
    Usuario.objects.filter(professor__isnull=False).update(moedas=F('moedas') + 1000)
    sys_config = Enum.objects.first()
    sys_config.semestre += 1
    sys_config.save()
    return redirect('/')

# Página de turmas
@ou_professor_ou_aluno
def turmas(request):
    return render(request, 'turmas.html', {'suas_turmas': request.user.aluno.turmas.all() if request.user.aluno else request.user.professor.turmas.all(), 'turmas': Turma.objects.all()})

# Página de uma turma
@somente_professor
def turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    return render(request, 'turma.html', {'professor': turma.professor_set.first(), 'alunos': turma.aluno_set.all(), 'turma': turma})

# Cadastro de turmas, cria e insere uma turma no banco de dados
@somente_super
def cadastrar_turma(request):
    Turma.objects.create()
    return redirect('/')

# Página de vantagens
@somente_aluno
def vantagens(request):
    vantagens_compradas = request.user.aluno.vantagens.all()
    compradas = {}
    for vantagem in vantagens_compradas:
        transacao = Transacao.objects.filter(de=request.user, vantagem_comprada=vantagem).first()
        if transacao:
            compradas[vantagem] = transacao.codigo
    return render(request, 'vantagens.html', {
        # Filtra as vantagens que o aluno não possui
        'vantagens': Vantagem.objects.exclude(id__in=request.user.aluno.vantagens.values_list('id', flat=True)),
        'compradas': compradas
    })

# Página de extrato de transações
@somente_autenticado
def historico(request):
    return render(request, 'historico.html', {
        'transacoes_enviadas': Transacao.objects.filter(de=request.user),
        'transacoes_recebidas': Transacao.objects.filter(para=request.user)
    })

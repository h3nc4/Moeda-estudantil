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

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    pass

class Endereco(models.Model):
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    rua = models.CharField(max_length=50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=50, blank=True, default='')

class Vantagem(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.IntegerField()

class Transacao(models.Model):
    moedas = models.IntegerField()
    mensagem = models.CharField(max_length=200, blank=True, default='Mensagem não especificada')
    para_quem = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='para_quem')

class Turma(models.Model):
    id = models.AutoField(primary_key=True)

class Membro(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=11, unique=True)
    turmas = models.ManyToManyField(Turma)
    moedas = models.IntegerField(default=0, blank=True)
    transacoes = models.ManyToManyField(Transacao, blank=True)
    class Meta:
        abstract = True

class Aluno(Membro):
    email = models.EmailField()
    rg = models.CharField(max_length=20)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)
    vantagens = models.ManyToManyField(Vantagem)

class Professor(Membro):
    pass

class Empresa(Usuario):
    pass

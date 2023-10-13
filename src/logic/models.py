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

class Sistema(models.Model):
    semestre = models.PositiveIntegerField(default=1)

class Endereco(models.Model):
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    rua = models.CharField(max_length=50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=10, blank=True, default=None)

class Empresa(models.Model):
    pass

class Vantagem(models.Model):
    descricao = models.TextField()
    imagem = models.TextField()
    valor = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Turma(models.Model):
    pass

class Usuario(AbstractUser):
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, blank=True, null=True)
    aluno = models.OneToOneField('Aluno', on_delete=models.CASCADE, blank=True, null=True)
    professor = models.OneToOneField('Professor', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Os campos abaixo são herdados de AbstractUser mas desnecessários para o Usuário padrão 
    first_name = None; last_name = None

class Transacao(models.Model):
    moedas = models.PositiveIntegerField()
    mensagem = models.CharField(max_length=200, blank=True, default='Mensagem não especificada')
    de = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='de_user')
    para = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='para_user')

class Membro(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    turmas = models.ManyToManyField(Turma)
    moedas = models.PositiveIntegerField(default=0, blank=True)
    class Meta:
        abstract = True

class Aluno(Membro):
    rg = models.CharField(max_length=10)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    vantagens = models.ManyToManyField(Vantagem)

class Professor(Membro):
    pass

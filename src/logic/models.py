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
import string
import random

class Enum(models.Model):
    semestre = models.PositiveIntegerField(default=1)

class Endereco(models.Model):
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    rua = models.CharField(max_length=50)
    numero = models.PositiveSmallIntegerField()
    complemento = models.CharField(max_length=10, blank=True, default=None)

class Usuario(AbstractUser):
    empresa = models.OneToOneField('Empresa', on_delete=models.CASCADE, blank=True, null=True)
    aluno = models.OneToOneField('Aluno', on_delete=models.CASCADE, blank=True, null=True)
    professor = models.OneToOneField('Professor', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    moedas = models.PositiveIntegerField(default=0, blank=True)

    # Os campos abaixo são herdados de AbstractUser mas desnecessários para o Usuário padrão 
    first_name = None; last_name = None

class Membro(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    turmas = models.ManyToManyField('Turma')
    class Meta:
        abstract = True

class Aluno(Membro):
    rg = models.CharField(max_length=10)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    vantagens = models.ManyToManyField('Vantagem')

class Professor(Membro):
    pass

class Turma(models.Model):
    pass

class Empresa(models.Model):
    pass

class Vantagem(models.Model):
    descricao = models.TextField()
    imagem = models.BinaryField()
    valor = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Transacao(models.Model):
    moedas = models.PositiveIntegerField()
    mensagem = models.CharField(max_length=200, blank=True, default='Mensagem não especificada')
    de = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='de_user')
    para = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='para_user')
    vantagem_comprada = models.ForeignKey('Vantagem', on_delete=models.CASCADE, blank=True, null=True)
    codigo = models.CharField(max_length=6, unique=True, blank=True, null=True, default=None)
    def gerar_codigo(self):
        if self.de.aluno and self.para.empresa:
            novo_codigo = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
            if Transacao.objects.filter(codigo=novo_codigo).exists():
                return self.gerar_codigo()
            return novo_codigo
        return None

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.gerar_codigo()
        super().save(*args, **kwargs)

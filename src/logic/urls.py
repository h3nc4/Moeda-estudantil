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

from django.urls import path, include
from .views import views, auth_views, post_views

url_empresa = [
    path('', views.empresa, name='empresa'),
    path('cadastro/', auth_views.cadastro_empresa, name='cadastro_empresa'),
    path('nova_vantagem/', views.nova_vantagem, name='nova_vantagem'),
]

url_admin = [
    path('cadastro_professor/', auth_views.cadastro_professor, name='cadastro_professor'),
    path('avanca_semestre/', views.avanca_semestre, name='avanca_semestre'),
    path('cadastrar_turma/', views.cadastrar_turma, name='cadastrar_turma'),
]

urlpatterns = [
    path('admin/', include(url_admin)),
    path('empresa/', include(url_empresa)),
    path('', views.index, name='index'),
    path('cadastro/', auth_views.cadastro, name='cadastro'),
    path('turmas/', views.turmas, name='turmas'),
    path('enturmar/', post_views.enturmar, name='enturmar'),
    path('turma/<int:id>', views.turma, name='turma'),
    path('enviar_moeda/<int:id>', post_views.enviar_moeda, name='enviar_moeda'),
    path('comprar/<int:id>', post_views.comprar, name='comprar'),
    path('vantagens/', views.vantagens, name='vantagens'),
    path('historico/', views.historico, name='historico'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
]

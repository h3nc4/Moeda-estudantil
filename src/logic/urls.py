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
from . import views

url_empresa = [
    path('', views.empresa, name='empresa'),
    path('cadastro/', views.cadastro_empresa, name='cadastro_empresa'),
    path('nova_vantagem/', views.nova_vantagem, name='nova_vantagem'),
]

urlpatterns = [
    path('empresa/', include(url_empresa)),
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro_professor/', views.cadastro_professor, name='cadastro_professor'),
    path('avanca_semestre/', views.avanca_semestre, name='avanca_semestre'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]

# Moeda Estudantil

## Estrutura

```bash
├── docs/ - Documentação do projeto e descrição do sistema
│   ├── casos_de_uso/ - Diagrama de casos de uso e histórias de usuário
│   ├── classes/ - Diagrama de classes
│   ├── db/ - Modelo ER, Definição da estratégia de acesso ao banco de dados e comandos SQL
│   ├── flow/ - Diagrama de Sequência
│   ├── pdf/ - Apresentações e relatórios
├── scripts/ - Scripts de desenvolvimento e implantação
├── src/ - Código fonte e instruções para instalação e execução do projeto
│   ├── app/ - Configuração do Django
│   ├── logic/ - Lógica da aplicação
│   │  ├── migrations/ - Migrações do banco de dados
│   │  ├── templates/ - Telas de interface
│   │  ├── views/ - Controladores
```

## Instalação

Veja [src/README.md](src/README.md) para instruções de instalação e execução do projeto.

## Descrição do sistema

O Moeda Estudantil é um sistema de gerenciamento de moedas virtuais para escolas. O sistema permite que os professores recebam moedas a cada semestre e as distribuam para os alunos de acordo com seu desempenho. Os alunos podem trocar as moedas por recompensas publicadas por empresas parceiras e trocar cupons por produtos e serviços.

## Licença

Moeda Estudantil is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Moeda Estudantil is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

See [LICENSE](LICENSE) for more information.

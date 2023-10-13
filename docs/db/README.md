# Definição e implementação da estratégia de acesso ao banco de dados

A estratégia de acesso ao banco de dados no Django é facilitada pelo ORM (Object-Relational Mapping). O ORM permite interação com o banco de dados usando orientação ao objeto em Python, em vez de escrever consultas SQL diretamente.

No modelo implementado, as classes de modelo são mapeadas diretamente para tabelas no banco de dados. A herança é usada para representar a relação entre os diferentes tipos de usuários e modelos comuns.

Ao criar uma instância de modelo, com `Aluno.objects.create(...)` e `.save()`, o Django monta uma instrução SQL para adicionar uma linha à tabela correspondente no banco de dados.

Da mesma forma, ao consultar dados usando o ORM, como `Aluno.objects.filter(...)`, o Django gera consultas SQL para buscar os dados do banco de dados e retorna objetos Python que correspondem a esses dados.

A estratégia de acesso ao banco de dados é eficiente e segura, pois o Django lida com muitos detalhes de baixo nível, permitindo a nós salvar e recuperar dados sem escrever SQL diretamente e sem se preocupar com a segurança.

**Na modelagem, relação terminada em bola significa que o lado é "n" da relação.**

**Já a relação terminada em ponta significa que o lado é "1" da relação.**

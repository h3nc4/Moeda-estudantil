# Código fonte

## Instalação

```bash
sudo apt install python3 python3-pip python3-venv -y
git clone https://github.com/h3nc4/Moeda-estudantil.git moeda-estudantil
cd moeda-estudantil
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
mkdir src/logic/migrations
touch src/logic/migrations/__init__.py
python src/manage.py makemigrations
python src/manage.py migrate
```

Use `deactivate` para sair do ambiente virtual.

Use `source .venv/bin/activate` antes de executar qualquer dos seguintes comandos.

## Execução

```bash
python src/manage.py runserver
```

## Criação do primeiro usuário

```bash
python src/manage.py createsuperuser
```

## Gerar modelo ER

```bash
python src/manage.py graph_models logic -o tmp.dot
dot -Tpng tmp.dot -o ./docs/db/Modelo_ER.png
rm tmp.dot
```

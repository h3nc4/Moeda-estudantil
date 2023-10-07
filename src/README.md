# Código fonte

## Instalação

```bash
sudo apt install python3 python3-pip python3-venv -y
git clone https://github.com/h3nc4/Moeda-estudantil.git
mv Moeda-estudantil moeda-estudantil
cd moeda-estudantil
python3 -m venv modules
source modules/bin/activate
pip install -r src/requirements.txt
mkdir src/logic/migrations
python src/manage.py makemigrations
python src/manage.py migrate
```

Use `deactivate` para sair do ambiente virtual.

Use `source modules/bin/activate` antes de executar qualquer dos seguintes comandos.

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

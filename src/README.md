# Código fonte

## Pré-requisitos

Crie um arquivo secrets.py em src/app com o seguinte conteúdo:

```python
KEY='chave do django'
DATABASE_PASSWORD='senha do banco de dados'
EMAIL_USER='usuário do email'
EMAIL_PASSWORD='senha do email'
```

Para gerar uma chave do django, use o seguinte comando:

```bash
python3 src/manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

Caso não deseje usar postgresql, altere o arquivo src/app/settings.py para usar sqlite3.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

## Instalação

```bash
sudo apt install python3 python3-pip python3-venv -y
git clone https://github.com/h3nc4/Moeda-estudantil.git moeda-estudantil
cd moeda-estudantil
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
python3 src/manage.py makemigrations
python3 src/manage.py migrate
```

Use `deactivate` para sair do ambiente virtual.

Use `source .venv/bin/activate` antes de executar qualquer dos seguintes comandos.

## Execução

```bash
python3 src/manage.py runserver
```

## Criação do primeiro usuário

```bash
python3 src/manage.py createsuperuser
```

## Gerar modelo ER

```bash
python3 src/manage.py graph_models logic -o tmp.dot
dot -Tpng tmp.dot -o ./docs/db/Modelo_ER.png
rm tmp.dot
```

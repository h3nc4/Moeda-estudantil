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

use `deactivate` para sair do ambiente virtual

## Execução

```bash
source modules/bin/activate
python src/manage.py runserver
```

## Criação do primeiro usuário

```bash
source modules/bin/activate
python src/manage.py createsuperuser
```

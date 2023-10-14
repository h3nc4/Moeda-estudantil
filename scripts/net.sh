# Diferente do script run.sh, este script permite conexão com em LAN, edite settings.py para permitir conexão com o IP da máquina
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py runserver 0.0.0.0:8000

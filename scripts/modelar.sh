python src/manage.py graph_models logic -o tmp.dot
dot -Tpng tmp.dot -o ./docs/db/Modelo_ER.png
rm tmp.dot

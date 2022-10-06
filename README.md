# Meus Dependentes


## Este projeto foi feito com:

* [Python 3.10.4](https://www.python.org/)
* [Django 4.0.6](https://www.djangoproject.com/)
* [Bootstrap 4.0](https://getbootstrap.com/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/klauvital/meus_dependentes.git
cd meus_dependentes
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
python manage.py cria_grupos
```


## Como resetar o banco

Se estiver usando docker, deve deletar o volume.

```
docker container exec -it sgwc psql

DROP DATABASE sgwc;
CREATE DATABASE sgwc;
```

## Deploy no Heroku

```
git add .
git commit -m 'mensagem'
git push

git push heroku main

heroku run python manage.py migrate
heroku run python manage.py cria_grupos  # caso precise

# Se der erro
heroku logs --tail
```



## Links

https://www.djangoproject.com/

https://ccbv.co.uk/

https://htmx.org/


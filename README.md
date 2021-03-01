# Mobilité 2 - Back-end
## Installation for local development
Requis : `python`, `virtualenv`
```shell
virtualenv venv
source venv/bin/activate
cp .env.local .env
pip install -r requirements.txt
python manage.py migrate
```

## Lancement de l'app
```shell
python manage.py runserver
```

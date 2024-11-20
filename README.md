## «Foodgram» — сайт, на котором пользователи публикуют свои рецепты
### Описание проекта
«Foodgram» — сайт, на котором пользователи публикуют свои рецепты, добавляют чужие рецепты в избранное и подписываются на публикации друг друга. 
Foodgram позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
Сайт доступен по адресу (https://fooooodgram.sytes.net/)
### Технологии
Python 3.9.13,
Django 3.2.3,
djangorestframework==3.12.4, 
PostgreSQL 13.10,
Docker,
Djoser,
Nginx 1.22.1

## Как запустить проект: 

Клонировать репозиторий и перейти в него в командной строке 
 
### Cоздать и активировать виртуальное окружение: 

Windows 

``` python -m venv venv ``` 
``` source venv/Scripts/activate ``` 

Linux/macOS

``` python3 -m venv venv ``` 
``` source venv/bin/activate ``` 

 
### Установить зависимости из файла requirements.txt: 
 
``` pip install -r requirements.txt ``` 
 

### Запустить проект с помощью Docker: 
Подключитесь к удаленному серверу

```ssh -i PATH_TO_SSH_KEY/SSH_KEY_NAME YOUR_USERNAME@SERVER_IP_ADDRESS ```

Установите Docker Compose на сервер:

    ```
    sudo apt update
    sudo apt install curl
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo apt install docker-compose
    ```

На сервере создать директорию foodgram и перейти в нее.

```mkdir foodgram/```
```cd foodgram```

Скопируйте файл docker-compose.production.yml из текущего репозитория в корневую папку проекта foodgram/
В корневой папке проекта foodgram/ создайте файл .env и заполните его согласно примеру:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db
DB_HOST=db
DB_PORT=5432
SECRET_KEY = *django_secret_key*
DEBUG = True
ALLOWED_HOSTS = ваш_домен,127.0.0.1,localhost,
```
Создайте администратора сайта
```sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser```

Запустите docker-compose
```sudo docker compose -f docker-compose.production.yml up -d```

## Автор проекта:

Denis Gurov @dgnsvh
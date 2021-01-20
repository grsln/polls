# Polls API

### Установка Polls API с помощью Docker

Открываем терминал на клиенте.

Вводим следующие команды:

+ _cd ~/.ssh_

+ _ssh-keygen -t rsa_

> на все запросы нажимаем клавишу Enter

+ _cat id_rsa.pub_ - выводим на экран публичный ключ, копируем в буфер Ctrl-C

Регистрируемся на сайте Vscale.io и создаем *Docker*-сервер. При создании сервера выбираем **Добавить ключ ssh**. В окне создания ключа вводим произвольное название и вставляем из буфера раннее скопированный ключ. Далее выбираем добавленный ключ и нажимаем **Создать сервер**.

В окне терминала клиента вводим:

+ _ssh root@xxx.xxx.xxx.xxx_ (где xxx.xxx.xxx.xxx— IP созданного сервера).

Скачиваем образы из Docker Hub.

+ _docker pull grsln/polls_api_web:latest_

+ _docker pull grsln/polls_api_nginx:latest_

Создаем docker-compose.yaml и вводим конфигурации

+ _nano docker-compose.yml_

```
version: '3.7'

services:
  web:
    image: grsln/polls_api_web:latest
    command: gunicorn polls.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/home/polls/web/static
      - media_volume:/home/polls/web/media
    expose:
      - 8000
    env_file:
      - ./.env
    depends_on:
      - db
  db:
    image: postgres:12.0-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env.db
  nginx:
    image: grsln/polls_api_nginx:latest
    volumes:
      - static_volume:/home/polls/web/static
      - media_volume:/home/polls/web/media
    ports:
      - 80:80
    depends_on:
      - web
volumes:
  postgres_data:
  static_volume:
  media_volume:
```

Создаем файл .env,  вводим домен (или IP-адрес) docker-сервера и secret key 
+ _nano .env_

```
DEBUG=0
SECRET_KEY=<secret key>
DJANGO_ALLOWED_HOSTS=*
DATABASE_URL=/home/up_site/web/db/db.sqlite3

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=<database name>
SQL_USER=<database user>
SQL_PASSWORD=<password>
SQL_HOST=db
SQL_PORT=<port>
DATABASE=postgres
```

Создаем файл .env,  вводим домен (или IP-адрес) docker-сервера и secret key 
+ _nano .env.db_

```
POSTGRES_USER=<database user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database name>
```
Выполняем запуск контейнеров
+ _docker-compose  up -d_

Выполняем команды

+ _docker-compose  exec web python manage.py migrate --noinput_

+ _docker-compose  exec web python manage.py collectstatic --noinput_

+ _docker-compose  exec web python manage.py createsuperuser_
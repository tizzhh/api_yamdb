### API yambd
API версии 1 для взаимодействия с сервисом yambd. Доступны следующие эндпоинты:
```
categories/
genres/
titles/
titles/<int:pk>/
titles/<int:pk>/reviews/
titles/<int:pk>/reviews/<int:pk>/
titles/<int:pk>/reviews/<int:pk>/comments/
titles/<int:pk>/reviews/<int:pk>/comments/<int:pk>/
users/
users/<slug:username>/
``` 

Для аутентификации используется PyJWT и djangorestframework-simplejwt. Для начала создается пользователь, после чего на указанную почту отправляется код с подтверждением. Далее с помощью этого кода и юзернейма можно получить токен.
```
auth/signup/
auth/token/
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:bpaverin/api_final_yatube.git
```


Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Предусмотрена возможность загрузить заранее подготовленные данные для таблиц:
```
cd static
python3.9 data_loader.py 
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов
Полная документация доступна по эндпоинту *redoc/*

- POST api/v1/auth/signup/

Тело:
```
{
  "email": "user@example.com",
  "username": "string"
}
```

Ответ:
```
{
  "email": "string",
  "username": "string"
}
```

- POST api/v1/auth/token/

Тело:
```
{
  "username": "string",
  "confirmation_code": "string"
}
```

Ответ:
```
{
  "token": "string"
}
```

- GET api/v1/genres/

Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
- GET api/v1/titles/

Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
- GET api/v1/titles/<int:pk>/reviews

Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
- GET api/v1/titles/<int:pk>/reviews/<int:pk>/comments/

Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

Используемые библиотеки:
- requests==2.26.0
- Django==3.2
- djangorestframework==3.12.4
- PyJWT==2.1.0
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- djangorestframework-simplejwt==4.7.2
- django-filter==23.5
- pandas==2.2.1

Версия Python:
Python 3.9.18

Авторы:

> tizzhh. Гит: https://github.com/tizzhh. Почта: darovadraste@gmail.com. Сайт: tizzhh.github.io

> bpaverin. Гит: https://github.com/bpaverin. Почта: bpaverin@gmail.com.

> diiishka. Гит: https://github.com/diiishka. Почта: dkuzhambetova@gmail.com
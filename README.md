# API "Друзья"

## Технологии
 - Python
 - FastApi
 - PostgreSQL

## API

1. POST /auth/users/

Регистрация нового пользователя.

#### Тело запроса
|Параметр|Тип|Описание|
|--------|---|--------|
|username|string|Имя пользователя|
|password|string|Пароль|


#### Пример запроса
```
POST /auth/users/
{
  "username": "ivan",
  "password": "useruser"
}'
```

#### Пример ответа
```json
{
  "username": "ivan",
  "id": 1
}
```

2. POST /auth/jwt/create/

Получение access и refresh токенов

#### Тело запроса
|Параметр|Тип|Описание|
|--------|---|--------|
|username|string|Имя пользователя|
|password|string|Пароль|


#### Пример запроса
```
POST /auth/jwt/create/
{
  "username": "ivan",
  "password": "useruser"
}'
```

#### Пример ответа
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzU3NTM3MCwiaWF0IjoxNjgzNDg4OTcwLCJqdGkiOiIyOWRiM2RmNzQ3YzY0ZWQ1YTI1NThhMDE4NzFjYzQ5NiIsInVzZXJfaWQiOjF9.aA_Srimj21xBWTEaubHjQ_aHH7x8FEJd_TNAh_EqG6c",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNDg5MjcwLCJpYXQiOjE2ODM0ODg5NzAsImp0aSI6IjdhNzRmZGY5NzFjZDRjYjNiN2JlY2ExNDlhNzJmMzBjIiwidXNlcl9pZCI6MX0.lozEHTlJDD3fDIKf7H1I9_V8Yd_3DZWlnaoEp_Bt3LA"
}
```

3. POST /auth/jwt/refresh/

Обновление access токена

#### Тело запроса
|Параметр|Тип|Описание|
|--------|---|--------|
|refresh|string|Токен|


#### Пример запроса
```
POST /auth/jwt/refresh/
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzU3NTM3MCwiaWF0IjoxNjgzNDg4OTcwLCJqdGkiOiIyOWRiM2RmNzQ3YzY0ZWQ1YTI1NThhMDE4NzFjYzQ5NiIsInVzZXJfaWQiOjF9.aA_Srimj21xBWTEaubHjQ_aHH7x8FEJd_TNAh_EqG6c"
}'
```

#### Пример ответа
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNDg5NDExLCJpYXQiOjE2ODM0ODg5NzAsImp0aSI6IjRjYjA4NjhmYTBlZTQ2Y2Y4MWYxYTY4OTk4NTg1ZjhjIiwidXNlcl9pZCI6MX0.7JZzuF6syfHUoXc4rtoq3OsGMA4tM6nNkHUM-bRyYHw"
}
```

4. POST /auth/jwt/verify/

Проверяет валидный ли токен

#### Тело запроса
|Название|Тип|Описание|
|--------|---|--------|
|token|string|Токен|


#### Пример запроса
```
POST /auth/jwt/verify/
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNDg5NjA2LCJpYXQiOjE2ODM0ODkzMDYsImp0aSI6IjYwMjE2NDEwZTdjNzQxYmViN2U4NDY1YjM1M2RkYTdjIiwidXNlcl9pZCI6MX0.WLqpDN1ll0n2xzzlrH-BRWSVyAflPSPJpo98zmS7-rY"
}
```

#### Пример ответа
```json
{}
```

5. POST /api/v1/friends/request/

Отправить заявку в друзья

#### Тело запроса
|Название|Тип|Описание|
|--------|---|--------|
|username|string|Имя пользователя|


#### Пример запроса
```
POST /api/v1/friends/request/
{
  "username": "semen"
}
```

#### Пример ответа
```json
{
  "status": "ok"
}
```

6. POST /api/v1/friends/request/accept/

Принять заявку в друзья

#### Тело запроса
|Название|Тип|Описание|
|--------|---|--------|
|username|string|Имя пользователя|


#### Пример запроса
```
POST /api/v1/friends/request/accept/
{
  "username": "ivan"
}
```

#### Пример ответа
```json
{
  "status": "ok"
}
```

7. POST /api/v1/friends/request/reject/

Отклонить заявку в друзья

#### Тело запроса
|Название|Тип|Описание|
|--------|---|--------|
|username|string|Имя пользователя|


#### Пример запроса
```
POST /api/v1/friends/request/reject/
{
  "username": "ivan"
}
```

#### Пример ответа
```json
{
  "status": "ok"
}
```

8. GET /api/v1/friends/request/incoming/

Получить входищие заявки в друзья.

#### Пример запроса
```
GET /api/v1/friends/request/incoming/
```

#### Пример ответа
```json
[
  {
    "id": 2,
    "from_user": {
      "id": 1,
      "username": "ivan"
    },
    "is_canceled": true
  }
]
```

9. GET /api/v1/friends/request/outgoing/

Получить исходящие заявки в друзья.

#### Пример запроса
```
GET /api/v1/friends/request/outgoing/
```

#### Пример ответа
```json
[
  {
    "id": 2,
    "to_user": {
      "id": 3,
      "username": "jack"
    },
    "is_canceled": false
  }
]
```

10. GET /api/v1/friends/

Получить список друзей

#### Пример запроса
```
GET /api/v1/friends/
```

#### Пример ответа
```json
[
  {
    "id": 5,
    "username": "kate"
  },
  {
    "id": 6,
    "username": "tom"
  }
]
```

11. GET /api/v1/friends/status/

Получить список друзей

#### Параметры запроса
|Название|Тип|Описание|
|--------|---|--------|
|username|string|Имя пользователя|

#### Пример запроса
```
GET /api/v1/friends/status/?username=ivan/
```

#### Пример ответа
```json
{
  "status": "Incoming request"
}
```

12. DELETE /api/v1/friends/

Удлить пользователя из друзей

#### Параметры запроса
|Название|Тип|Описание|
|--------|---|--------|
|username|string|Имя пользователя|


#### Пример запроса
```
DELETE /api/v1/friends/delete/?username=ivan/
```

## Запуск
**Перед запуском необходимо заполнить файл ```.env```**
```text
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

SECRET=
```

Для запуска ввести команду:
```shell
docker-compose up -d --build
```

Для запуска тестов ввести команду:
```shell
docker-compose exec api python manage.py test
```

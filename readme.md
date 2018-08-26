# Тестовое задание от ReTech Labs

[Техническое задание](tz.pdf)

## Руководство по установке

Установка:

```commandline
pip3 install -r requirements
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

Тестирование:
```commandline
python3 manage.py test
```

Запуск:
```commandline
python3 manage.py runserver
```

## Админ панель

Админ панель расположена по адресу [/admin](http://localhost:8000/admin)

Через админ панель создаются пользователи, работники (на основе пользователей) и организации.

## Django-Rest-Framework

Авторизация: [/api/signin](http://localhost:8000/api/signin)

POST-запрос
```json
{
    "email": "root@test.com", 
    "organiz":"TUSUR", 
    "passw":"123qwe123"
}
```

Выход из системы: [/api/signout](http://localhost:8000/api/signout)

Получить список доступных ToDo заданий: [/api/tasks](http://localhost:8000/api/tasks)

#### CRUD-операции

##### Создание записи: 

[/api/tasks](http://localhost:8000/api/tasks/)

POST-запрос
```json
{
    "name": "Проверить тестовое задание",
    "description": "Описание для тестового задания",
    "deadline": "2018-08-26T17:25:29Z",
    "status": 1,
    "priority": 1
}
```

##### Обновление записи: 

/api/tasks/(?P\<id\>\d+)/

PUT-запрос (Все параметры должны присутствовать)

```json
{
    "name": "Проверить тестовое задание",
    "description": "",
    "deadline": "",
    "status": 1,
    "priority": 1
}
```

##### Удаление записи:

/api/tasks/(?P\<id\>\d+)/

DELETE - запрос

## Стек использованных технологий

Python3

Django 1.10

Django-Rest-Framework

Sqlite

Git

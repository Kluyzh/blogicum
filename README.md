# Blogicum
### Описание
Блогикум — это дом для творческих людей. Это — сообщество людей, для которых нет грани между ведением блога и дружбой в социальных сетях.

Дружба и рассказы о новых, неизведанных впечатлениях — вот что вы найдете на нашем ресурсе. Миллионы блогов по различным темам. Путешествия, политика, развлечения, мода, литература, дизайн и все другие сферы человеческой деятельности.

Творчество, разнообразие и свобода взглядов и самовыражения — основные черты наших пользователей.

### Технологии
- Python 3.9.10
- Django 3.2.16

### Запуск проекта в dev-режиме
(Руководство для владельцев системы Windows)
- Установите и активируйте виртуальное окружение:
```
1. python -m venv venv
2. source venv/Scripts/activate
```
- Обновите pip:
```
python -m pip install --upgrade pip
```
- Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
- Выполните миграции:
```
python manage.py migrate
``` 
- Создайте суперпользователя:
```
python manage.py createsuperuser
``` 
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```
- При пустой базе данных загрузите фикстуры:
```
python manage.py loaddata db.json
```
### Авторы
Илья Клюжев

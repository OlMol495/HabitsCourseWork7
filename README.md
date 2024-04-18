Курсовой проект "Трекер полезных привычек"
Для работы с проектом необходимо выполнить следующие действия:
Клонировать репозиторий.
Активировать виртуальное окружение
Установить зависимости из файла pyproject.toml
Создать файл .env, заполнить его данными из файла .env.sample
Создать базу данных в PostreSQL CREATE DATABASE <yourdatabasename>
Создать python manage.py makemigrate и применить миграции python manage.py migrate
Создать пользователя командой python manage.py csu
Установить и запустить Redis локально (на Windows)
В терминале набрать команду celery -A config worker -l info -P eventlet
В терминале набрать команду celery -A config beat -l info -S django
Запустить проект python manage.py runserver
Откройте браузер и перейдите по адресу http://127.0.0.1:8000 для доступа к приложению.

Документация для API реализована с помощью drf-yasg и находится на следующих эндпоинтах:

http://127.0.0.1:8000/redoc/
http://127.0.0.1:8000/swagger/
Тестирование проекта
Для тестирования проекта запустить команду: python manage.py test
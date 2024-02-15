# PollTracker

Веб-приложение, разработанное для подсчета голосов на мероприятиях проводимых на конкурсной основе. В приложении реализована возможность создания участников, судей и структуры конкурса. Судьи могут выполнять голосование по критериям для каждого участника на различных этапах конкурса. В конце конкурса отображаются результаты голосования в порядке убывания.

[![Mixmaster](https://img.shields.io/badge/Developed%20by-mixmaster-blue?style=for-the-badge)](https://github.com/mixma5ter)

### Алгоритм работы с приложением
1. Запуск админ панели:
   - Создание участников, судей и структуры конкурса.
2. Регистрация конкурса:
   - Запуск команды создания оценок со значением по умолчанию.
3. Пользовательский интерфейс судьи:
   - Судьи получают ссылку на страницу авторизации.
   - Выбирают свое имя из выпадающего списка судей и переходят к конкурсу.
   - Выполняют голосование на каждом этапе, выбирая оценки из выпадающего списка по критериям для каждого участника.
   - Переходят к следующему этапу, когда голосование текущего этапа окончено.
4. Отображение результатов:
   - В конце конкурса, результаты голосования отображаются на странице в порядке убывания.

### Пользовательские роли
- Судья (`judge`): Может работать с интерфейсом приложения и влиять на результаты голосования путем выставления оценок участникам конкурса.
- Администратор (`admin`): Обладает полными правами на управление всем контентом проекта. Может создавать и удалять конкурсы, регистрировать участников и назначать роли пользователям.

### Стек технологий
* Python 3.7
* Django 3.2
* REST API
* HTML, CSS
* JavaScript
* PostgreSQL
* Nginx
* gunicorn

### Запуск проекта
1. Требования перед установкой:
   - Установите Python 3.7 на вашей системе.
   - Установите Django 3.2, используя следующую команду:
   
   `pip install Django==3.2`
   
   - Установите PostgreSQL и настройте его.

2. Установка и запуск серверной части:
   - Склонируйте репозиторий проекта.
   - Перейдите в папку проекта.
   - Установите все зависимости, выполнив следующую команду:
   
   `pip install -r requirements.txt`
   
   - Создайте базу данных PostgreSQL и настройте файл settings.py, указав параметры подключения к вашей базе данных.
   - Выполните миграции, используя команды:
   
   `python manage.py makemigrations`

   `python manage.py migrate`
   
   - Запустите серверную часть, выполнив следующую команду:
   
   `python manage.py runserver`

3. Откройте веб-браузер и перейдите по адресу http://localhost:8000, чтобы начать работу с приложением.

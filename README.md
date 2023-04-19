# PollTracker

Веб-приложение подсчета голосов для мероприятий на конкурсной основе.

[![Mixmaster](https://img.shields.io/badge/Developed%20by-mixmaster-blue?style=for-the-badge)](https://github.com/mixma5ter)

### Алгоритм работы с приложением
* В админ панели создаются участники, судьи и структура конкурса.
* После регистрации конкурса запускается команда создания оценок со значением по умолчанию.
* Пользователь (судья) получает ссылку на страницу авторизации. Выбирает свое имя в выпадающем списке судей и переходит к конкурсу.
После этого он попадает на страницу первого этапа голосования, где выбирает оценки из выпадающего списка по критериям для каждого участника.
* После окончания голосования первого этапа, переходит ко второму этапу и т.д.
* В конце конкурса, пользователю отображаются страница с результатами голосования в порядке убывания.

### Пользовательские роли
* **Судья** (`judge`) — работает с интерфейсом приложения, влияет на результаты голосования путем выставления оценок участникам конкурса.
* **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять конкурсы, регистрировать участников и назначать роли пользователям.

### Стек технологий
* Python 3.7
* Django 3.2
* REST API
* HTML, CSS
* JavaScript
* PostgreSQL
* Nginx
* gunicorn

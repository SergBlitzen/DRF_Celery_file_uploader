# DRF/Celery file uploader

API на DRF для загрузки и обработки файлов с помощью Celery.

Подробный стек:

* Python 3.9
* Django
* Django REST Framework
* Celery
* Flower
* Redis
* nginx
* PostgreSQL 

### Доступ к API

Реализованы два эндпоинта:

* `/api/v1/upload/` — для загрузки одного файла. Разрешён только метод POST. Пример payload запроса:
```
{
  'file': your_file_object.file
}
```
* `/api/v1/files/` — для доступа к списку загруженных файлов. Разрешён только метод GET. Пример получения данных по запросу:
```
{
  'id': 1,
  'file': your_file_object.file,
  'uploaded_at': "yyyy-mm-ddT17:hh:mm.ss+03:00",
  "processed": true/false
}
```

### Запуск в контейнерах

Деплой в контейнерах полностью настроен и автоматизирован.

<details>
<summary>Подробная инструкция:</summary>

* скопировать репозиторий
* настроить переменные окружения в .env файле в соответствии с .env.example;
* собрать образы в docker compose:
```
docker compose build
```
* запустить образы в docker compose:
```
docker compose up
```
</details>

### Выполнено

Загрузка и обработка файлов: файлы загружаются во временное хранилище, откуда обрабатываются уже задачей. Первоначально
View-функция принимает файл из запроса (перед этим проверяя, что загружен лишь один) и сохраняет во временное хранилище,
после чего создаёт объект модели файла и передаёт информацию о его primary key и пути к файлу в асинхронно выполняющуюся
задачу.

Задача находит нужный объект по ключу и обрабатывает файл, привязывая его к объекту, после чего удаляет временный файл.

<details>
<summary>Дополнительно:</summary>

* настроена администраторская панель;
* настроен nginx для выдачи статики админки и api root;
* настроен контейнер flower для визуального интерфейса к задачам воркера Celery, но полноценно доступен он только 
по порту 5555 локального хоста;
</details>

### Масштабирование

Так как Django по умолчанию не предназначен для хранения и обработки файлов большого объёма, для дальнейшего масштабирования 
потребуется определить, какие именно запросы и файлы будут исходить от пользователей: для большого объёма файлов необходимо
горизонтальное расширение, в чём можно воспользоваться распределёнными хранилищами — здесь нужно подключать ```django-storage```
и соответствующие бэкенды, например, S3. При большом параметре RPS потребуется расширить сеть воркеров.


### Проблемные места и возможные улучшения

Реализация разных механизмов обработки для разных расширений файлов требует уточнения: связано ли это с ожиданием конкретных
типов, или же требуется общий механизм сжатия. Сейчас обработка разных типов сделана максимально просто: основной тип
находится через `content-type` — такой вариант, правда, не идеален, поэтому можно реализовать более сложную систему, — и
по основному назначению идёт проброс данных непосредственно к задаче-обработчику (менеджер также можно улучшить). Сами
обработчики повторяют друг друга, так как нет вводных данных для точечной обработки конкретных типов.

Скорость отклика на запрос зависит от самого сервера: на данный момент это WSGI, который обрабатывает запросы синхронно, 
для обеспечения полной асинхронности потребуется перейти на ASGI. Сейчас, с WSGI, сервер всё ещё синхронно принимает запросы
и отвечает на них последовательно.

Дополнительно по функционалу приложения можно предложить некоторые quality-of-life улучшения: переход на вьюсеты для
большего контроля над объектами модели файлов (или отдельная реализация методов, например, `PATCH` и `DELETE`), расширение
информации в модели, к примеру, название и/или объём. Также view-функция возвращает ответ с данными объекта на момент
создания необработанными данными.
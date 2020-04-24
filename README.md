# api_final
api final

### Описание
Это API для социальной сети Yatube. 
### Установка
- настройте виртуальное окружение
- склонируйте проект с реппозитория GitHub
- установите необходимые библиотеки 
    ```
    pip install -r requirements.txt
    ```
- запустите проект
    ```
    python manage.py runserver
    ```
- зайдите на страницу http://localhost:8000/redoc/ 
и воспользуйтесь документацией к API :smile:
### Примеры запросов к API
- Получить список всех публикаций
```http://localhost:8000/api/v1/posts/```
```
GET /api/v1/posts/
```
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "author": "yadmin",
        "group": ёжики,
        "text": "новый текст для первого поста",
        "pub_date": "2020-04-22T17:57:31.888998Z"
    },
    ...
]
```
- Получить список всех комментариев для выбранной публикации
```http://localhost:8000/api/v1/posts/1/comments/```
```
GET /api/v1/posts/1/comments/
```
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "author": "yadmin",
        "text": "первый тестовый коммент для первого поста",
        "created": "2020-04-23T12:59:14.096584Z",
        "post": 1
    },
    ...
]
```
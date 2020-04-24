# api_final
api final

### Описание
Это API для социальной сети Yatube. 
### Установка
- настройте виртуальное окружение
- склонируйте проект с реппозитория GitHub
- установите необходимые библиотеки 
    `<pip install -r requirements.txt>`
- запустите проект
    ```
    python manage.py runserver
    ```
- зайдите на страницу http://localhost:8000/redoc/ и воспользуйтесь документацией к API
### Примеры запросов к API
- Получить список всех публикаций
    'http://localhost:8000/api/v1/posts/'
- Получить список всех комментариев публикации
    'http://localhost:8000/api/v1/posts/{post_id}/comments/'




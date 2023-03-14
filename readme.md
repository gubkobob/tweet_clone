**Аналог твиттера**

1. Разработка
    - запуск приложения
```docker-compose up --build```
    - создание БД

      - Создание БД происходит посредством инициализирующей миграции в контейнере web

        - alembic revision --message="Init migration" --autogenerate
        - alembic upgrade head
    - тестирование
        - тестирование происходит автоматически при pull в ветку master и при push в ветки master, main
     




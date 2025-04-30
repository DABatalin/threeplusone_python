# Платформа аналитики электронной коммерции

## Обзор проекта
Платформа электронной коммерции с аналитическими возможностями, построенная на FastAPI, PostgreSQL, Elasticsearch, Kafka и ClickHouse.

### Функциональность
- Аутентификация и авторизация пользователей
- Управление товарами с операциями CRUD
- Функционал корзины покупок
- Поиск товаров с использованием Elasticsearch
- Хранение изображений с использованием S3
- Аналитический конвейер с Kafka и ClickHouse
- Обработка данных с помощью Apache Spark

### Технологический стек
- **Бэкенд**: FastAPI
- **База данных**: PostgreSQL
- **Поиск**: Elasticsearch
- **Очередь сообщений**: Kafka
- **Аналитика**: ClickHouse
- **Хранилище**: S3
- **Обработка данных**: Apache Spark

## Инструкции по установке

1. Создайте и активируйте виртуальное окружение:
```bash
python3.11 -m venv venv
source venv/bin/activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервисы с помощью Docker:
```bash
docker-compose up -d
```
Возможно, для запуска придется включить впн, чтобы скачать образы

4. Удалите папку alembic и файл alembic.ini, но сохраните содержимое файла alembic/env.py и alembic.ini. После выполнения команды ниже:
```bash
alembic init alembic
```
Замените создавшиеся файлы env.py и alembic.ini на те, которые вы сохранили заранее.

5. Выполните миграции базы данных:
```bash
alembic revision --autogenerate -m "init migration"
alembic upgrade head
```

6. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

## Структура проекта
```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   │   
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │   
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │   
│   ├── models/
│   │   └── __init__.py
│   │   
│   ├── schemas/
│   │   └── __init__.py
│   │   
│   └── services/
│   │       └── __init__.py
│   ├── alembic/
│   ├── tests/
│   ├── .env
│   ├── .gitignore
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
```

## Команда
1. Климов Иван - тимлид, аналитик
2. Баталин Дмитрий - техлид, бекенд
3. Драновский Иван - S3 база данных, метрики
4. Елизавета Николаева - kafka, apache spark


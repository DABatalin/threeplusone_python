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

3. Настройте переменные окружения в файле `.env`:
```bash
# PostgreSQL
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ecommerce
POSTGRES_PORT=5432

# JWT
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET_NAME=your-bucket-name

# Elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

4. Запустите сервисы с помощью Docker:
```bash
docker-compose up -d
```

5. Выполните миграции базы данных:
```bash
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


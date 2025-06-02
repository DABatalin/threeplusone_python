# E-commerce Analytics Platform

Платформа электронной коммерции с аналитическими возможностями, построенная на FastAPI.

## Основные возможности

- Аутентификация и авторизация пользователей
- Управление товарами и продавцами
- Система корзины покупок
- Комментарии к товарам
- Хранение изображений товаров в MinIO
- Поиск по товарам, продавцам и комментариям через Elasticsearch
- Аналитика с использованием ClickHouse и Apache Kafka
- Мониторинг системы через Prometheus и Grafana
- Автоматические тесты для всех основных функций API

## Технологический стек

- **Backend**: FastAPI, Python 3.11
- **База данных**: PostgreSQL
- **Хранение изображений**: MinIO
- **Поиск**: Elasticsearch
- **Очереди сообщений**: Apache Kafka
- **Аналитика**: ClickHouse
- **Мониторинг**: Prometheus, Grafana
- **Тестирование**: Pytest
- **Контейнеризация**: Docker, Docker Compose

## Начало работы

### Предварительные требования

- Docker и Docker Compose
- Python 3.11 или выше
- Git

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd project_python
```

2. Создайте файл `.env` в корневой директории проекта со следующим содержимым:
```env
PROJECT_NAME=E-commerce Analytics Platform
API_V1_STR=/api/v1

POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ecommerce
POSTGRES_PORT=5432

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MinIO settings
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_HOST=minio
MINIO_PORT=9000
MINIO_BUCKET_NAME=product-images
MINIO_USE_SSL=false

ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200

KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

3. Запустите сервисы с помощью Docker Compose:
```bash
docker-compose up --build
```

4. После запуска будут доступны следующие сервисы:
- API: http://localhost:8000
- Swagger документация: http://localhost:8000/docs
- MinIO консоль: http://localhost:9001 (login: minioadmin, password: minioadmin)
- Grafana: http://localhost:3000 (login: admin, password: admin)
- Prometheus: http://localhost:9090

## Мониторинг

Система включает в себя комплексный мониторинг с использованием Prometheus и Grafana:

### Prometheus
- Собирает метрики приложения
- Доступен по адресу http://localhost:9090
- Настроен на сбор метрик FastAPI приложения

### Grafana
- Доступна по адресу http://localhost:3000
- Логин: admin
- Пароль: admin
- Предустановленные дашборды:
  - Application_info 
  - Request_info

Дашборды хранятся в формате JSON в директории `grafana/dashboards/json/` и автоматически загружаются при старте Grafana.

## Структура проекта

```

├── app/                    # Основной код приложения
│   ├── api/                # API endpoints
│   ├── core/               # Основные настройки и конфигурация
│   ├── crud/               # CRUD операции
│   ├── db/                 # Настройки базы данных
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic схемы
│   ├── services/           # Сервисные слои
│   ├── tests/              # Автоматические тесты
│   └── main.py             # Точка входа в приложение
```

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/signup` - Регистрация

### Товары
- `GET /api/v1/products` - Список товаров
- `POST /api/v1/products` - Создание товара
- `GET /api/v1/products/{id}` - Получение товара
- `PUT /api/v1/products/{id}` - Обновление товара
- `DELETE /api/v1/products/{id}` - Удаление товара
- `POST /api/v1/products/{id}/image` - Загрузка изображения товара

### Корзина
- `GET /api/v1/cart` - Просмотр корзины
- `POST /api/v1/cart` - Добавление товара в корзину
- `DELETE /api/v1/cart/{id}` - Удаление товара из корзины

### Покупки
- `POST /api/v1/purchases` - Оформление покупки
- `GET /api/v1/purchases` - История покупок

## Работа с изображениями

Система использует MinIO для хранения изображений товаров. Изображения хранятся в бакете `product-images` со следующей структурой:
```
product-images/
└── products/
    └── {product_id}/
        └── {uuid}.{extension}
```

### Загрузка изображений

```bash
curl -X POST "http://localhost:8000/api/v1/products/{id}/image" \
  -H "Authorization: Bearer {token}" \
  -F "file=@/path/to/image.jpg"
```

## Разработка

### Установка зависимостей для разработки
```bash
pip install -r requirements.txt
```

### Запуск тестов
```bash
# Запуск всех тестов
pytest

# Запуск конкретного модуля тестов
pytest app/tests/test_auth.py

# Запуск тестов с подробным выводом
pytest -v

# Запуск тестов с выводом print statements
pytest -s
```

### Форматирование кода
```bash
black .
isort .
flake8
```

## Лицензия

[MIT License](LICENSE)

## Команда
1. Климов Иван - тимлид, аналитик
2. Баталин Дмитрий - техлид, бекенд
3. Драновский Иван - S3 база данных, метрики
4. Елизавета Николаева - kafka, apache spark

## Тестирование Kafka

Для проверки работоспособности Kafka используется скрипт `tests/kafka_test.py`. Скрипт проверяет:

1. Работу Producer:
   - Отправляет 5 тестовых сообщений в топик "test-topic"
   - Каждое сообщение содержит ID, текст и временную метку
   - Выводит подтверждение доставки каждого сообщения

2. Работу Consumer:
   - Подписывается на топик "test-topic"
   - Пытается получить сообщения в течение 30 секунд
   - Выводит содержимое полученных сообщений
   - Останавливается после получения всех 5 тестовых сообщений

### Запуск теста Kafka

```bash
# Убедитесь, что Kafka запущена
python tests/kafka_test.py
```

Успешное выполнение теста подтверждает:
- Доступность Kafka брокера
- Возможность создания топиков
- Корректную работу producer и consumer
- Правильную сериализацию/десериализацию сообщений

## Аналитическая система

Проект включает комплексную систему аналитики, использующую Apache Spark для обработки данных и синхронизации между PostgreSQL и ClickHouse.

### Архитектура аналитической системы

1. **Источники данных**:
   - PostgreSQL (основная БД)
   - Kafka (потоковые данные о действиях пользователей)

2. **Обработка данных**:
   - Apache Spark для ETL процессов
   - Airflow для оркестрации и планирования задач

3. **Хранение аналитических данных**:
   - ClickHouse (OLAP база данных)

### Spark Jobs

1. **Historical Migration** (`spark/jobs/historical_migration.py`):
   - Единоразовая миграция исторических данных из PostgreSQL в ClickHouse
   - Полная синхронизация всех необходимых таблиц

2. **Incremental Sync** (`spark/jobs/incremental_sync.py`):
   - Регулярная синхронизация новых данных
   - Отслеживание изменений по временным меткам
   - Обработка только новых или измененных записей

3. **Data Aggregation** (`spark/jobs/data_aggregation.py`):
   - Агрегация данных о продажах
   - Анализ активности пользователей
   - Создание аналитических срезов

### Airflow DAGs

1. **Data Sync and Aggregation** (Hourly):
   ```
   data_sync_and_aggregation_dag
   ├── incremental_sync_task
   ├── data_aggregation_task
   └── data_quality_check_task
   ```

2. **Historical Migration** (One-time):
   ```
   historical_data_migration_dag
   ├── migration_task
   └── validation_task
   ```

### Аналитические таблицы в ClickHouse

1. **daily_sales_aggregation**:
   - Ежедневные агрегаты по продажам
   - Группировка по категориям товаров
   - Статистика по продавцам

2. **user_activity_aggregation**:
   - Метрики активности пользователей
   - Статистика просмотров товаров
   - Конверсия в покупки

### Запуск аналитической системы

1. Запуск всех сервисов:
```bash
docker-compose up -d
```

2. Проверка статуса сервисов:
```bash
docker-compose ps
```

3. Запуск исторической миграции:
```bash
airflow trigger_dag historical_data_migration_dag
```

4. Мониторинг:
- Airflow UI: http://localhost:8080
- Spark UI: http://localhost:4040
- ClickHouse UI: http://localhost:8123


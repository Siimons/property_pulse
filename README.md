### Property Pulse

## Описание проекта

Property Pulse — это веб-приложение для агрегации и анализа объявлений о продаже и аренде недвижимости. Приложение собирает данные с таких ресурсов, как Avito и ЦИАН, и предоставляет пользователям централизованную платформу для просмотра объявлений с актуальными ценами и ссылками на оригинальные источники.

Приложение также предоставляет API для управления объявлениями, запуска парсеров, а также инструменты для аналитики данных по недвижимости.

## Структура проекта

```
property_pulse/
│
├── app/                         # Основное приложение
│   ├── __init__.py              # Инициализация модуля
│   ├── config.py                # Конфигурационные параметры (например, API ключи, базы данных)
│   ├── api/                     # Модуль для API взаимодействия (веб-сервер)
│   │   ├── __init__.py
│   │   ├── exceptions.py        # Обработка ошибок
│   │   ├── routes.py            # Определение маршрутов API
│   │   ├── schemes.py           # Схемы для валидации и сериализации данных 
│   │   ├── views.py             # Визуализация данных для фронтенда
│   │   ├── dependencies.py      # Зависимости для маршрутов (например, авторизация)
│   │   └── utils.py             # Вспомогательные функции для API
│   ├── parsers/                 # Модуль парсинга
│   │   ├── __init__.py
│   │   ├── base_parser.py       # Базовый класс парсинга (общие функции)
│   │   ├── cian_parser.py       # Парсер для ЦИАН
│   │   ├── avito_parser.py      # Парсер для Авито
│   │   └── utils.py             # Вспомогательные функции для парсинга (например, работа с прокси)
│   ├── storage/                 # Модуль хранения данных
│   │   ├── __init__.py
│   │   ├── database.py          # Работа с базой данных (PostgreSQL/MongoDB)
│   │   ├── models.py            # Описание моделей данных (таблицы базы данных)
│   │   ├── cache.py             # Кэширование данных с помощью Redis или Memcached
│   │   └── migrations.py        # Миграции базы данных (если используется SQL)
│   ├── analysis/                # Модуль анализа данных
│   │   ├── __init__.py
│   │   ├── data_cleaning.py     # Обработка и очистка данных
│   │   ├── analytics.py         # Основные методы анализа данных
│   │   └── geo_analysis.py      # Географический анализ (например, карты, работа с GeoPandas)
│   ├── visualization/           # Модуль визуализации данных
│   │   ├── __init__.py
│   │   ├── plots.py             # Генерация графиков (Plotly, Matplotlib)
│   │   ├── maps.py              # Генерация карт (Folium, GeoPandas)
│   │   └── dashboards.py        # Создание интерактивных дашбордов (Dash, Streamlit)
│   └── notifications/           # Модуль уведомлений
│       ├── __init__.py
│       ├── email_notifications.py      # Отправка email-уведомлений
│       ├── telegram_notifications.py   # Уведомления через Telegram
│       └── scheduler.py                # Планировщик задач (Celery, Cron)
│
├── tests/                       # Тесты для различных модулей
│   ├── __init__.py
│   ├── test_parsers.py          # Тесты для парсеров
│   ├── test_api.py              # Тесты для API
│   ├── test_analysis.py         # Тесты для анализа данных
│   ├── test_visualization.py    # Тесты для визуализации данных
│   └── test_notifications.py    # Тесты для уведомлений
│
├── scripts/                     # Скрипты для разовых задач или автоматизации
│   ├── run_parsers.py           # Запуск всех парсеров
│   ├── update_data.py           # Скрипт для обновления данных в базе
│   └── generate_reports.py      # Генерация отчетов по данным
│
├── migrations/                  # Миграции базы данных (если используется SQL)
│   └── ...                      # Миграции будут добавляться сюда
├── static/                      # Статические файлы (если требуется фронтенд)
│   └── ...                      # Например, CSS, JS, изображения
├── templates/                   # Шаблоны HTML (если используется для фронтенда)
│   └── index.html               # Главная страница
├── docker-compose.yml           # Конфигурация Docker для развертывания проекта
├── Dockerfile                   # Файл для сборки Docker-контейнера
├── requirements.txt             # Зависимости Python для проекта (pip)
├── README.md                    # Описание проекта
└── .env                         # Файл для хранения переменных окружения (например, ключи API)
```



## Основной функционал (CRUD для объявлений)

# Объявления

- POST `/api/listing/` — создание нового объявления
- PUT `/api/listing/{id}` — обновление объявления
- DELETE `/api/listing/{id}` — удаление объявления
- GET `/api/listings/` — получение списка всех объявлений
- GET `/api/listing/{id}` — получение конкретного объявления

# Парсеры

- POST `/api/parsers/cian/` — запуск парсера для ЦИАН
- POST `/api/parsers/avito/` — запуск парсера для Avito

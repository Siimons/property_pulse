# Указываем базовый образ Python
FROM python:3.12.3-alpine

# Устанавливаем зависимости для работы FastAPI и Uvicorn
RUN apk add --no-cache gcc musl-dev libffi-dev

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Скопируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Указываем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1

# Добавляем аргументы для подключения к базе данных
ARG MYSQL_DATABASE
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_ROOT_PASSWORD

# Экспонируем порт для приложения
EXPOSE 8000

# Команда для запуска приложения (например, через uvicorn или другой сервер)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

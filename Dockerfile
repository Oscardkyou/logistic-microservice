FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Копирование файлов проекта
COPY . .

# Открытие порта
EXPOSE 8082

# Запуск приложения через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8082", "app:app"]

FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Открытие порта
EXPOSE 8888

# Запуск приложения
CMD ["python", "app.py", "--port=8888"]

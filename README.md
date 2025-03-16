# Система управления логистикой

Веб-приложение для планирования и отслеживания отгрузок по регионам Казахстана. Система позволяет управлять графиком отгрузок на текущую и следующую неделю.

## Функциональные возможности

- Просмотр графика отгрузок на текущую и следующую неделю
- Добавление новых отгрузок с указанием даты, пункта назначения, объема и статуса
- Редактирование существующих отгрузок
- Удаление отгрузок
- Автоматический расчет общего объема отгрузок на каждую неделю
- Цветовая кодировка дней недели для удобства восприятия
- Адаптивный дизайн для мобильных устройств

## Технологии

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Хранение данных**: JSON

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий
2. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Запустите приложение:
   ```
   python app.py
   ```
4. Откройте в браузере http://localhost:8082

## Развертывание на сервере (shopnclick.kz)

### Подготовка сервера

1. Убедитесь, что на сервере установлены Python 3.8+ и pip
2. Установите и настройте веб-сервер (Nginx или Apache)
3. Настройте WSGI-сервер (Gunicorn или uWSGI)

### Пример конфигурации Nginx для домена shopnclick.kz

```nginx
server {
    listen 80;
    server_name shopnclick.kz www.shopnclick.kz;

    location / {
        proxy_pass http://127.0.0.1:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/your/app/static;
    }
}
```

### Настройка SSL (HTTPS)

Для безопасной работы сайта рекомендуется настроить SSL-сертификат с помощью Let's Encrypt:

```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d shopnclick.kz -d www.shopnclick.kz
```

### Запуск приложения с помощью Gunicorn

1. Установите Gunicorn:
   ```
   pip install gunicorn
   ```

2. Создайте systemd сервис для автоматического запуска:
   ```
   sudo nano /etc/systemd/system/logistics.service
   ```

3. Добавьте следующее содержимое:
   ```
   [Unit]
   Description=Logistics Management System
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/your/app
   ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 127.0.0.1:8082 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. Активируйте и запустите сервис:
   ```
   sudo systemctl enable logistics.service
   sudo systemctl start logistics.service
   ```

## Деплой с использованием Docker и Docker Compose

### Вариант 1: Использование Docker и Docker Compose (рекомендуется)

Проект подготовлен для деплоя с использованием Docker и Docker Compose, что упрощает процесс развертывания.

#### Предварительные требования

- Установленный Docker
- Установленный Docker Compose

#### Шаги для деплоя

1. Клонируйте репозиторий на сервер:

```bash
git clone https://github.com/Oscardkyou/logistic-microservice.git
cd logistic-microservice
```

2. Запустите приложение с помощью Docker Compose:

```bash
docker-compose up -d
```

Приложение будет доступно по адресу http://your-server-ip/

#### Полезные команды Docker Compose

- Просмотр логов:
```bash
docker-compose logs -f
```

- Остановка приложения:
```bash
docker-compose down
```

- Перезапуск приложения после изменений:
```bash
docker-compose up -d --build
```

### Вариант 2: Традиционный деплой

Для деплоя приложения на продакшн-сервере без Docker рекомендуется использовать Gunicorn или uWSGI вместе с Nginx:

```bash
# Установите Gunicorn
pip install gunicorn

# Запустите приложение с помощью Gunicorn
gunicorn -w 4 -b 0.0.0.0:8082 app:app
```

## Обслуживание

### Резервное копирование данных

Регулярно создавайте резервные копии файла `shipments.json`:

```bash
cp /path/to/your/app/shipments.json /path/to/backup/shipments_$(date +%Y%m%d).json
```

### Обновление приложения

1. Остановите сервис:
   ```
   sudo systemctl stop logistics.service
   ```

2. Обновите код из репозитория

3. Запустите сервис:
   ```
   sudo systemctl start logistics.service
   ```

## Контакты

По вопросам поддержки и развития системы обращайтесь к администратору.

## График отгрузок - логистический микросервис

## Описание

Это веб-приложение на Flask для управления графиком отгрузок. Приложение позволяет просматривать график отгрузок на текущую и следующую неделю, добавлять новые отгрузки, редактировать существующие отгрузки, удалять отгрузки, а также рассчитывать общий объем отгрузок на каждую неделю.

## Основные функции

- Просмотр графика отгрузок на текущую и следующую неделю
- Добавление новых отгрузок с указанием даты, пункта назначения, объема и статуса
- Редактирование существующих отгрузок
- Удаление отгрузок
- Автоматический расчет общего объема отгрузок на каждую неделю
- Цветовая кодировка дней недели для удобства восприятия
- Адаптивный дизайн для мобильных устройств

## Технологии

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Хранение данных**: JSON

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Oscardkyou/logistic-microservice.git
cd logistic-microservice
```

2. Создайте и активируйте виртуальное окружение (не обязательно, но рекомендуется):

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# Или venv\Scripts\activate для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python app.py
```

Приложение будет доступно по адресу http://localhost:8082/

Вы можете указать другой порт с помощью параметра `--port`:

```bash
python app.py --port 8083
```

## Деплой

Для деплоя приложения на сервере рекомендуется использовать Gunicorn и Nginx:

```bash
# Установите Gunicorn
pip install gunicorn

# Запустите приложение с помощью Gunicorn
gunicorn -w 4 -b 0.0.0.0:8082 app:app
```

## Лицензия

MIT

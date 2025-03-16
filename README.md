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
4. Откройте в браузере http://localhost:8888

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
        proxy_pass http://127.0.0.1:8888;
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
   ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 127.0.0.1:8888 app:app
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

Приложение будет доступно по адресу http://your-server-ip:8888/

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

#### Дополнительная информация

Создаются два контейнера:
- `logistics-app` - сам веб-сервер на Flask/Gunicorn (порт 8888)
- `logistics-nginx` - Nginx для проксирования запросов и кеширования статических файлов (порт 8888)

3. Приложение будет доступно по адресу http://your-server-ip:8888/

### Вариант 2: Традиционный деплой

Для деплоя приложения на продакшн-сервере без Docker рекомендуется использовать Gunicorn и Nginx:

```bash
# Установите Gunicorn
pip install gunicorn

# Запустите приложение с помощью Gunicorn
gunicorn -w 4 -b 0.0.0.0:8888 app:app
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

Приложение будет доступно по адресу http://localhost:8888/

Вы можете указать другой порт с помощью параметра `--port`:

```bash
python app.py --port 8889
```

## Деплой

Для деплоя приложения на сервере рекомендуется использовать Gunicorn и Nginx:

```bash
# Установите Gunicorn
pip install gunicorn

# Запустите приложение с помощью Gunicorn
gunicorn -w 4 -b 0.0.0.0:8888 app:app
```

## Лицензия

MIT

## u0413u0440u0430u0444u0438u043a u041eu0442u0433u0440u0443u0437u043eu043a

u041fu0440u043eu0441u0442u043eu0435 u0432u0435u0431-u043fu0440u0438u043bu043eu0436u0435u043du0438u0435 u043du0430 Flask u0434u043bu044f u0443u043fu0440u0430u0432u043bu0435u043du0438u044f u0433u0440u0430u0444u0438u043au043eu043c u043eu0442u0433u0440u0443u0437u043eu043a.

## u0424u0443u043du043au0446u0438u0438

- u041eu0442u043eu0431u0440u0430u0436u0435u043du0438u0435 u0442u0435u043au0443u0449u0438u0445 u0438 u0431u0443u0434u0443u0449u0438u0445 u043eu0442u0433u0440u0443u0437u043eu043a
- u0414u043eu0431u0430u0432u043bu0435u043du0438u0435 u043du043eu0432u044bu0445 u043eu0442u0433u0440u0443u0437u043eu043a
- u0420u0435u0434u0430u043au0442u0438u0440u043eu0432u0430u043du0438u0435 u0441u0443u0447u0435u0441u0442u0432u0443u044eu0449u0438u0445 u043eu0442u0433u0440u0443u0437u043eu043a
- u041fu0440u0438u043cu0435u0447u0430u043du0438u0435 u0434u043bu044f u043cu0435u043du0435u0434u0436u0435u0440u043eu0432

## u0423u0441u0442u0430u043du043eu0432u043au0430 u0438 u0437u0430u043fu0443u0441u043a

### u041bu043eu043au0430u043bu044cu043du044bu0439 u0437u0430u043fu0443u0441u043a

1. u041au043bu043eu043du0438u0440u0443u0439u0442u0435 u0440u0435u043fu043eu0437u0438u0442u043eu0440u0438u0439:

```bash
git clone https://github.com/Oscardkyou/logistic-microservice.git
cd logistic-microservice
```

2. u0423u0441u0442u0430u043du043eu0432u0438u0442u0435 u0437u0430u0432u0438u0441u043cu043eu0441u0442u0438:

```bash
pip install -r requirements.txt
```

3. u0417u0430u043fu0443u0441u0442u0438u0442u0435 u043fu0440u0438u043bu043eu0436u0435u043du0438u0435:

```bash
python app.py
```

u041fu0440u0438u043bu043eu0436u0435u043du0438u0435 u0431u0443u0434u0435u0442 u0434u043eu0441u0442u0443u043fu043du043e u043fu043e u0430u0434u0440u0435u0441u0443 http://localhost:8888

### u0417u0430u043fu0443u0441u043a u0441 u0438u0441u043fu043eu043bu044cu0437u043eu0432u0430u043du0438u0435u043c Docker

1. u041au043bu043eu043du0438u0440u0443u0439u0442u0435 u0440u0435u043fu043eu0437u0438u0442u043eu0440u0438u0439:

```bash
git clone https://github.com/Oscardkyou/logistic-microservice.git
cd logistic-microservice
```

2. u0421u043eu0431u0435u0440u0438u0442u0435 u0438 u0437u0430u043fu0443u0441u0442u0438u0442u0435 Docker-u043au043eu043du0442u0435u0439u043du0435u0440:

```bash
# u0421u0431u043eu0440u043au0430 u043eo0431u0440u0430u0437u0430
docker build -t logistics-app .

# u0417u0430u043fu0443u0441u043a u043au043eu043du0442u0435u0439u043du0435u0440u0430
docker run -d --name logistics-app -p 8888:8888 -v "$(pwd)/shipments.json:/app/shipments.json" logistics-app
```

u041fu0440u0438u043bu043eu0436u0435u043du0438u0435 u0431u0443u0434u0435u0442 u0434u043eu0441u0442u0443u043fu043du043e u043fu043e u0430u0434u0440u0435u0441u0443 http://localhost:8888

## u0421u0442u0440u0443u043au0442u0443u0440u0430 u043fu0440u043eu0435u043au0442u0430

- `app.py` - u043eu0441u043du043eu0432u043du043eu043e u0444u0430u0439u043b u043fu0440u0438u043bu043eu0436u0435u043du0438u044f
- `shipments.json` - u0444u0430u0439u043b u0441 u0434u0430u043du043du044bu043cu0438 u043eu0431 u043eu0442u0433u0440u0443u0437u043au0430u0445
- `templates/` - HTML-u0448u0430u0431u043bu043eu043du044b
- `static/` - CSS, JavaScript u0438 u0434u0440u0443u0433u0438u0435 u0441u0442u0430u0442u0438u0447u0435u0441u043au0438u0435 u0444u0430u0439u043bu044b

## u041bu0438u0446u0435u043du0437u0438u044f

MIT

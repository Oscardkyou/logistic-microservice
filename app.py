from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import os
import argparse
from datetime import datetime, timedelta
import copy

app = Flask(__name__)
app.secret_key = 'secret_key'

# Data file path
DATA_FILE = 'shipments.json'

# Initialize data if it doesn't exist
def init_data():
    """Инициализация данных или загрузка существующих"""
    # Получаем текущую дату
    today = datetime.now()
    
    # Находим ближайший понедельник (начало текущей недели)
    days_until_monday = (0 - today.weekday()) % 7
    current_week_start = today + timedelta(days=days_until_monday)
    
    # Конец текущей недели - пятница
    current_week_end = current_week_start + timedelta(days=4)  # +4 дня = пятница
    
    # Следующая неделя начинается со следующего понедельника
    next_week_start = current_week_start + timedelta(days=7)
    next_week_end = next_week_start + timedelta(days=4)  # +4 дня = пятница
    
    # Форматирование дат для отображения
    current_week_str = f"{current_week_start.strftime('%d.%m')} - {current_week_end.strftime('%d.%m.%Y')}"
    next_week_str = f"{next_week_start.strftime('%d.%m')} - {next_week_end.strftime('%d.%m.%Y')}"
    
    # Создание структуры данных
    data = {
        'week_start': current_week_start.strftime('%d.%m.%Y'),
        'week_end': current_week_end.strftime('%d.%m.%Y'),
        'shipments': [],
        'next_id': 1,
        'notes': [],
        'next_note_id': 1
    }
    
    # Сохранение данных в JSON файл
    with open('shipments.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data

# Get day of week from date
def get_day_of_week(date_str):
    """Получить день недели из строки даты в формате DD.MM.YYYY"""
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return days[date_obj.weekday()]
    except Exception as e:
        print(f"Ошибка при определении дня недели: {e}")
        return ""

# Load data from file
def load_data():
    """Загрузка данных из файла"""
    if not os.path.exists(DATA_FILE):
        return init_data()
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Преобразование строк дат в объекты datetime
            if 'week_start' in data:
                data['week_start'] = datetime.strptime(data['week_start'], '%d.%m.%Y')
            if 'week_end' in data:
                data['week_end'] = datetime.strptime(data['week_end'], '%d.%m.%Y')
            
            # Добавление next_id, если его нет
            if 'next_id' not in data:
                data['next_id'] = 1
                if 'shipments' in data and data['shipments']:
                    # Находим максимальный ID и увеличиваем на 1
                    max_id = max([int(s.get('id', 0)) for s in data['shipments']])
                    data['next_id'] = max_id + 1
            
            # Добавление next_note_id, если его нет
            if 'next_note_id' not in data:
                data['next_note_id'] = 1
                if 'notes' in data and data['notes']:
                    # Находим максимальный ID и увеличиваем на 1
                    max_id = max([int(s.get('id', 0)) for s in data['notes']])
                    data['next_note_id'] = max_id + 1
            
            return data
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return init_data()

# Save data to file
def save_data(data):
    """Сохранение данных в файл"""
    # Преобразование дат в строки для JSON
    json_data = copy.deepcopy(data)
    
    if 'week_start' in json_data:
        json_data['week_start'] = json_data['week_start'].strftime('%d.%m.%Y')
    if 'week_end' in json_data:
        json_data['week_end'] = json_data['week_end'].strftime('%d.%m.%Y')
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

# Function to calculate total volume of shipments
def calculate_total_volume(shipments):
    total = 0
    for shipment in shipments:
        # Извлекаем числовое значение объема из строки (например, "10 тонн" -> 10)
        try:
            volume_str = shipment.get('volume', '0 тонн')
            volume_value = int(volume_str.split(' ')[0])
            total += volume_value
        except (ValueError, IndexError):
            continue
    return total

@app.route('/')
def index():
    data = load_data()
    
    # Получаем все отгрузки
    shipments = data.get('shipments', [])
    
    # Разделяем отгрузки на текущую и следующую неделю
    current_week_shipments = [s for s in shipments if s.get('week') != 'next']
    next_week_shipments = [s for s in shipments if s.get('week') == 'next']
    
    # Рассчитываем общий объем для каждой недели
    current_week_volume = calculate_total_volume(current_week_shipments)
    next_week_volume = calculate_total_volume(next_week_shipments)
    
    # Дни недели для отображения (только рабочие дни с понедельника по четверг)
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    
    # Группируем отгрузки по дням недели
    current_week_by_day = {day: [] for day in days}
    next_week_by_day = {day: [] for day in days}
    
    for shipment in current_week_shipments:
        day = shipment.get('day')
        if day in days:
            current_week_by_day[day].append(shipment)
    
    for shipment in next_week_shipments:
        day = shipment.get('day')
        if day in days:
            next_week_by_day[day].append(shipment)
    
    # Получаем строки с датами для отображения
    current_week_dates = data.get('week_start', '').strftime('%d.%m') + ' - ' + data.get('week_end', '').strftime('%d.%m.%Y')
    next_week_dates = (data.get('week_start', '') + timedelta(days=7)).strftime('%d.%m') + ' - ' + (data.get('week_end', '') + timedelta(days=7)).strftime('%d.%m.%Y')
    
    # Получаем примечания руководства
    notes = data.get('notes', [])
    
    return render_template('index.html', 
                           days=days,
                           current_week_shipments=current_week_shipments,
                           next_week_shipments=next_week_shipments,
                           current_week_by_day=current_week_by_day,
                           next_week_by_day=next_week_by_day,
                           current_week_volume=current_week_volume,
                           next_week_volume=next_week_volume,
                           current_week_dates=current_week_dates,
                           next_week_dates=next_week_dates,
                           notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_shipment():
    if request.method == 'POST':
        data = load_data()
        
        # Get the next ID
        next_id = data.get('next_id', 1)
        data['next_id'] = next_id + 1
        
        # Convert date from YYYY-MM-DD to DD.MM.YYYY
        date_str = request.form['date']
        if date_str:
            date_parts = date_str.split('-')
            if len(date_parts) == 3:
                formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
            else:
                formatted_date = date_str
        else:
            formatted_date = ""
        
        # Автоматически определяем день недели по дате
        day_of_week = get_day_of_week(formatted_date) if formatted_date else request.form['day']
        
        # Check which week we're adding shipment for
        is_next_week = request.form.get('week') == 'next'
        
        # Create new shipment
        new_shipment = {
            'id': next_id,
            'day': day_of_week,  # Используем определенный день недели
            'date': formatted_date,
            'destination': request.form['destination'],
            'volume': request.form['volume'],
            'status': request.form['status']
        }
        
        # If it's shipment for next week, add corresponding flag
        if is_next_week:
            new_shipment['week'] = 'next'
        
        # Add to data
        data['shipments'].append(new_shipment)
        save_data(data)
        
        return redirect(url_for('index'))
    
    # For GET request, show the form
    data = load_data()
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    
    # Check which week we're showing form for
    week_param = request.args.get('week', '')
    is_next_week = week_param == 'next'
    
    return render_template('add.html', days=days, is_next_week=is_next_week)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_shipment(id):
    data = load_data()
    
    # Find shipment by ID
    shipment = None
    is_next_week = False
    for s in data['shipments']:
        if s['id'] == id:
            shipment = s
            is_next_week = s.get('week') == 'next'
            break
    
    if shipment is None:
        flash('Отгрузка не найдена', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Convert date from YYYY-MM-DD to DD.MM.YYYY
        date_str = request.form['date']
        if date_str:
            date_parts = date_str.split('-')
            if len(date_parts) == 3:
                formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
            else:
                formatted_date = date_str
        else:
            formatted_date = ""
        
        # Автоматически определяем день недели по дате
        day_of_week = get_day_of_week(formatted_date) if formatted_date else request.form['day']
        
        # Check if week has changed
        new_is_next_week = request.form.get('week') == 'next'
        
        # Update shipment data
        shipment['day'] = day_of_week  # Используем определенный день недели
        shipment['date'] = formatted_date
        shipment['destination'] = request.form['destination']
        shipment['volume'] = request.form['volume']
        shipment['status'] = request.form['status']
        
        # Update week flag if it has changed
        if new_is_next_week and not is_next_week:
            shipment['week'] = 'next'
        elif not new_is_next_week and is_next_week:
            if 'week' in shipment:
                del shipment['week']
        
        save_data(data)
        flash('Отгрузка успешно обновлена', 'success')
        return redirect(url_for('index'))
    
    # Convert date from DD.MM.YYYY to YYYY-MM-DD for input field
    date_for_input = ""
    if shipment['date']:
        date_parts = shipment['date'].split('.')
        if len(date_parts) == 3:
            date_for_input = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
    
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return render_template('edit.html', shipment=shipment, days=days, date_for_input=date_for_input, is_next_week=is_next_week)

@app.route('/delete/<int:id>')
def delete_shipment(id):
    data = load_data()
    
    # Find shipment by ID
    shipment = None
    shipment_index = -1
    for i, s in enumerate(data['shipments']):
        if s['id'] == id:
            shipment = s
            shipment_index = i
            break
    
    if shipment is None:
        flash('Отгрузка не найдена', 'danger')
        return redirect(url_for('index'))
    
    # Delete shipment
    data['shipments'].pop(shipment_index)
    save_data(data)
    
    # Redirect if it's shipment for next week
    is_next_week = shipment.get('week') == 'next'
    
    if is_next_week:
        flash('Отгрузка на следующую неделю успешно удалена', 'success')
    else:
        flash('Отгрузка успешно удалена', 'success')
    
    return redirect(url_for('index'))

@app.route('/api/shipments')
def get_shipments():
    # Получаем данные о текущей и следующей неделе
    current_week_by_day, next_week_by_day, days = load_shipments_by_day()
    
    # Подготавливаем данные для JSON-ответа
    current_week = {}
    next_week = {}
    
    # Счетчики для статистики
    total_current_week_volume = 0
    total_next_week_volume = 0
    total_current_week_shipments = 0
    total_next_week_shipments = 0
    
    for day in days:
        # Текущая неделя
        current_week[day] = current_week_by_day[day]
        total_current_week_shipments += len(current_week_by_day[day])
        
        # Суммируем объемы
        for shipment in current_week_by_day[day]:
            if shipment.get('volume'):
                try:
                    volume_value = int(shipment['volume'].split(' ')[0])
                    total_current_week_volume += volume_value
                except (ValueError, IndexError):
                    pass
        
        # Следующая неделя
        next_week[day] = next_week_by_day[day]
        total_next_week_shipments += len(next_week_by_day[day])
        
        # Суммируем объемы
        for shipment in next_week_by_day[day]:
            if shipment.get('volume'):
                try:
                    volume_value = int(shipment['volume'].split(' ')[0])
                    total_next_week_volume += volume_value
                except (ValueError, IndexError):
                    pass
    
    return jsonify({
        'days': days,
        'currentWeek': current_week,
        'nextWeek': next_week,
        'stats': {
            'totalCurrentWeekVolume': total_current_week_volume,
            'totalNextWeekVolume': total_next_week_volume,
            'totalVolume': total_current_week_volume + total_next_week_volume,
            'totalCurrentWeekShipments': total_current_week_shipments,
            'totalNextWeekShipments': total_next_week_shipments,
            'totalShipments': total_current_week_shipments + total_next_week_shipments
        }
    })

@app.route('/api/shipment-volumes')
def get_shipment_volumes():
    # Получаем данные о текущей и следующей неделе
    current_week_by_day, next_week_by_day, days = load_shipments_by_day()
    
    # Рассчитываем объемы по дням недели
    current_week_data = []
    next_week_data = []
    
    for day in days[:5]:  # Только рабочие дни
        # Текущая неделя
        current_volume = 0
        for shipment in current_week_by_day[day]:
            if shipment.get('volume'):
                try:
                    volume_value = int(shipment['volume'].split(' ')[0])
                    current_volume += volume_value
                except (ValueError, IndexError):
                    pass
        current_week_data.append(current_volume)
        
        # Следующая неделя
        next_volume = 0
        for shipment in next_week_by_day[day]:
            if shipment.get('volume'):
                try:
                    volume_value = int(shipment['volume'].split(' ')[0])
                    next_volume += volume_value
                except (ValueError, IndexError):
                    pass
        next_week_data.append(next_volume)
    
    return jsonify({
        'days': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'],
        'currentWeek': current_week_data,
        'nextWeek': next_week_data
    })

@app.route('/add_note', methods=['POST'])
def add_note():
    author = request.form.get('author')
    content = request.form.get('content')
    
    if not author or not content:
        flash('Пожалуйста, заполните все поля', 'danger')
        return redirect(url_for('index'))
    
    data = load_data()
    
    # Создаем структуру для примечаний, если ее нет
    if 'notes' not in data:
        data['notes'] = []
    
    # Создаем структуру для next_note_id, если ее нет
    if 'next_note_id' not in data:
        data['next_note_id'] = 1
    
    # Создаем новое примечание
    note = {
        'id': data['next_note_id'],
        'author': author,
        'content': content,
        'date': datetime.now().strftime('%d.%m.%Y %H:%M')
    }
    
    # Увеличиваем счетчик ID для следующего примечания
    data['next_note_id'] += 1
    
    # Добавляем примечание в список
    data['notes'].append(note)
    
    # Сохраняем данные
    save_data(data)
    
    flash('Примечание успешно добавлено', 'success')
    return redirect(url_for('index'))

@app.route('/delete_note/<int:id>')
def delete_note(id):
    data = load_data()
    
    # Находим примечание по ID
    if 'notes' in data:
        data['notes'] = [note for note in data['notes'] if note.get('id') != id]
        
        # Сохраняем данные
        save_data(data)
        
        flash('Примечание успешно удалено', 'success')
    else:
        flash('Примечание не найдено', 'danger')
    
    return redirect(url_for('index'))

def load_shipments_by_day():
    data = load_data()
    shipments = data.get('shipments', [])
    
    # Разделяем отгрузки на текущую и следующую неделю
    current_week_shipments = [s for s in shipments if s.get('week') != 'next']
    next_week_shipments = [s for s in shipments if s.get('week') == 'next']
    
    # Дни недели для отображения (только рабочие дни с понедельника по четверг)
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    
    # Группируем отгрузки по дням недели
    current_week_by_day = {day: [] for day in days}
    next_week_by_day = {day: [] for day in days}
    
    for shipment in current_week_shipments:
        day = shipment.get('day')
        if day in days:
            current_week_by_day[day].append(shipment)
    
    for shipment in next_week_shipments:
        day = shipment.get('day')
        if day in days:
            next_week_by_day[day].append(shipment)
    
    return current_week_by_day, next_week_by_day, days

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Flask app for shipping schedule')
    parser.add_argument('--port', type=int, default=8888, help='Port to run the server on')
    args = parser.parse_args()
    
    app.run(host='0.0.0.0', port=args.port, debug=False)

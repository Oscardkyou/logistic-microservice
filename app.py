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
    # Устанавливаем фиксированные даты для текущей недели (17-20 марта 2025)
    # 21 марта - праздник Наурыз
    current_week_start = datetime(2025, 3, 17)  # Понедельник, 17 марта 2025
    current_week_end = datetime(2025, 3, 20)    # Четверг, 20 марта 2025
    
    # Следующая неделя начинается с 22 марта (после праздника)
    next_week_start = datetime(2025, 3, 22)  # Суббота, 22 марта 2025
    next_week_end = datetime(2025, 3, 28)    # Пятница, 28 марта 2025
    
    # Форматирование дат для отображения
    current_week_str = f"17.03 - 20.03.2025"
    next_week_str = f"22.03 - 28.03.2025"
    
    # Создание структуры данных
    data = {
        'current_week': {
            'start': current_week_start,
            'end': current_week_end,
            'display': current_week_str
        },
        'next_week': {
            'start': next_week_start,
            'end': next_week_end,
            'display': next_week_str
        },
        'shipments': [],
        'next_id': 1,
        'notes': [],
        'next_note_id': 1
    }
    
    # Сохранение данных в JSON файл
    with open('shipments.json', 'w', encoding='utf-8') as f:
        # Преобразование дат в строки для JSON
        json_data = {
            'current_week': {
                'start': current_week_start.strftime('%Y-%m-%d'),
                'end': current_week_end.strftime('%Y-%m-%d'),
                'display': current_week_str
            },
            'next_week': {
                'start': next_week_start.strftime('%Y-%m-%d'),
                'end': next_week_end.strftime('%Y-%m-%d'),
                'display': next_week_str
            },
            'shipments': [],
            'next_id': 1,
            'notes': [],
            'next_note_id': 1
        }
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    return data

# Load data from file
def load_data():
    """Загрузка данных из файла"""
    if not os.path.exists(DATA_FILE):
        return init_data()
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Преобразование строк дат в объекты datetime
            if 'current_week' in data and isinstance(data['current_week'], dict):
                if 'start' in data['current_week']:
                    data['current_week']['start'] = datetime.strptime(data['current_week']['start'], '%Y-%m-%d')
                if 'end' in data['current_week']:
                    data['current_week']['end'] = datetime.strptime(data['current_week']['end'], '%Y-%m-%d')
            
            if 'next_week' in data and isinstance(data['next_week'], dict):
                if 'start' in data['next_week']:
                    data['next_week']['start'] = datetime.strptime(data['next_week']['start'], '%Y-%m-%d')
                if 'end' in data['next_week']:
                    data['next_week']['end'] = datetime.strptime(data['next_week']['end'], '%Y-%m-%d')
            
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
    
    if 'current_week' in json_data and isinstance(json_data['current_week'], dict):
        if 'start' in json_data['current_week'] and isinstance(json_data['current_week']['start'], datetime):
            json_data['current_week']['start'] = json_data['current_week']['start'].strftime('%Y-%m-%d')
        if 'end' in json_data['current_week'] and isinstance(json_data['current_week']['end'], datetime):
            json_data['current_week']['end'] = json_data['current_week']['end'].strftime('%Y-%m-%d')
    
    if 'next_week' in json_data and isinstance(json_data['next_week'], dict):
        if 'start' in json_data['next_week'] and isinstance(json_data['next_week']['start'], datetime):
            json_data['next_week']['start'] = json_data['next_week']['start'].strftime('%Y-%m-%d')
        if 'end' in json_data['next_week'] and isinstance(json_data['next_week']['end'], datetime):
            json_data['next_week']['end'] = json_data['next_week']['end'].strftime('%Y-%m-%d')
    
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
    current_week_dates = data.get('current_week', {}).get('display', '17.03 - 20.03.2025')
    next_week_dates = data.get('next_week', {}).get('display', '22.03 - 28.03.2025')
    
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
        
        # Check which week we're adding shipment for
        is_next_week = request.form.get('week') == 'next'
        
        # Create new shipment
        new_shipment = {
            'id': next_id,
            'day': request.form['day'],
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
    for s in data['shipments']:
        if s['id'] == id:
            shipment = s
            break
    
    if not shipment:
        flash('Отгрузка не найдена', 'danger')
        return redirect(url_for('index'))
    
    # Determine if shipment is for next week
    is_next_week = shipment.get('week') == 'next'
    
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
        
        # Check if week has changed
        new_is_next_week = request.form.get('week') == 'next'
        
        # Update shipment data
        shipment['day'] = request.form['day']
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
def api_shipments():
    data = load_data()
    return jsonify(data)

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

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Flask app for shipping schedule')
    parser.add_argument('--port', type=int, default=8082, help='Port to run the server on')
    args = parser.parse_args()
    
    app.run(debug=True, host='0.0.0.0', port=args.port)

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = '111'  # Для повідомлень Flash

# Конфігурація бази даних
DB_CONFIG = {
    'dbname': 'battleresultsdb',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}

# Функція для підключення до бази даних
def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Головна сторінка (Read)
@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('index.html', records=[])
    
    cur = conn.cursor()
    cur.execute("SELECT Date, Location, EnemyLosses, FriendlyLosses, Outcome FROM Engagements")
    records = cur.fetchall()
    cur.close()
    conn.close()

    # Конвертуємо дату у формат рядка, 
    processed_records = []
    for record in records:
        date = record[1]
        if isinstance(date, datetime):  # Якщо це об'єкт datetime
            date = date.strftime('%Y-%m-%d')
        processed_records.append((record[0], date, *record[2:]))

    return render_template('index.html', records=processed_records)

# Сторінка для створення запису (Create)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        Date = request.form['Date']
        Location = request.form['Location']
        EnemyLosses = request.form['EnemyLosses']
        FriendlyLosses = request.form['FriendlyLosses']
        Outcome = request.form['Outcome']

        if not all([Date, Location, EnemyLosses, FriendlyLosses, Outcome]):
            flash('All fields are required!', 'error')
            return redirect(url_for('create'))

        try:
            datetime.strptime(Date, '%Y-%m-%d')  # Перевірка формату дати
        except ValueError:
            flash('Invalid date format! Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('create'))

        conn = get_db_connection()
        if not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('create'))
        
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Engagements (Date, Location, EnemyLosses, FriendlyLosses, Outcome) VALUES (%s, %s, %s, %s, %s)",
            (Date, Location, EnemyLosses, FriendlyLosses, Outcome)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Record created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('create.html')

# Сторінка для редагування запису (Update)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('index'))
    
    cur = conn.cursor()

    if request.method == 'POST':
        Date = request.form['Date']
        Location = request.form['Location']
        EnemyLosses = request.form['EnemyLosses']
        FriendlyLosses = request.form['FriendlyLosses']
        Outcome = request.form['Outcome']

        if not all([Date, Location, EnemyLosses, FriendlyLosses, Outcome]):
            flash('All fields are required!', 'error')
            return redirect(url_for('edit', id=id))

        try:
            datetime.strptime(Date, '%Y-%m-%d')  # Перевірка формату дати
        except ValueError:
            flash('Invalid date format! Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('edit', id=id))

        cur.execute(
            "UPDATE Engagements SET Date = %s, Location = %s, EnemyLosses = %s, FriendlyLosses = %s, Outcome = %s WHERE id = %s",
            (Date, Location, EnemyLosses, FriendlyLosses, Outcome, id)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Record updated successfully!', 'success')
        return redirect(url_for('index'))

    cur.execute("SELECT id, Date, Location, EnemyLosses, FriendlyLosses, Outcome FROM Engagements WHERE id = %s", (id,))
    record = cur.fetchone()
    cur.close()
    conn.close()

    if record:
        record = list(record)
        date = record[1]
        if isinstance(date, datetime):  # Якщо це об'єкт datetime
            record[1] = date.strftime('%Y-%m-%d')

    return render_template('edit.html', record=record)

# Видалення запису (Delete)
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('index'))
    
    cur = conn.cursor()
    cur.execute("DELETE FROM Engagements WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Record deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

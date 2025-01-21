import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Налаштування підключення до PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname="battleresultsdb", 
        user="postgres", 
        password="admin", 
        host="localhost", 
        port="5432"
    )
    return conn

# Головна сторінка з відображенням всіх зіткнень
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Engagements;')
    engagements = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', engagements=engagements)

# Сторінка для додавання нового зіткнення
@app.route('/add', methods=('GET', 'POST'))
def add_engagement():
    if request.method == 'POST':
        date = request.form['date']
        location = request.form['location']
        enemy_losses = request.form['enemy_losses']
        friendly_losses = request.form['friendly_losses']
        outcome = request.form['outcome']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO Engagements (Date, Location, EnemyLosses, FriendlyLosses, Outcome) '
            'VALUES (%s, %s, %s, %s, %s)',
            (date, location, enemy_losses, friendly_losses, outcome)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_engagement.html')

# Редагувати зіткнення
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_engagement(id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Отримуємо існуючий запис за ID
    cur.execute('SELECT * FROM Engagements WHERE id = %s', (id,))
    engagement = cur.fetchone()

    if engagement is None:
        return 'Запис не знайдено', 404

    if request.method == 'POST':
        # Оновлюємо запис в базі
        date = request.form['date']
        location = request.form['location']
        enemy_losses = request.form['enemy_losses']
        friendly_losses = request.form['friendly_losses']
        outcome = request.form['outcome']

        cur.execute(
            'UPDATE Engagements SET Date = %s, Location = %s, EnemyLosses = %s, FriendlyLosses = %s, Outcome = %s WHERE id = %s',
            (date, location, enemy_losses, friendly_losses, outcome, id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    cur.close()
    conn.close()
    return render_template('edit_engagement.html', engagement=engagement)

# Видалити зіткнення
@app.route('/delete/<int:id>', methods=('POST',))
def delete_engagement(id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Видаляємо запис за ID
    cur.execute('DELETE FROM Engagements WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
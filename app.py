from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect("todo.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            task TEXT NOT NULL
                        )''')
init_db()

# Home Route (Displays tasks and search)
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        if search_query:
            cursor.execute("SELECT * FROM tasks WHERE task LIKE ?", ('%' + search_query + '%',))
        else:
            cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    
    return render_template('index.html', tasks=tasks, search_query=search_query)

# Add Task
@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form['task']
    if task_text:
        with sqlite3.connect("todo.db") as conn:
            conn.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
            conn.commit()
    return redirect(url_for('index'))

# Update Task
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    new_task = request.form['task']
    with sqlite3.connect("todo.db") as conn:
        conn.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
        conn.commit()
    return redirect(url_for('index'))

# Delete Task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect("todo.db") as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

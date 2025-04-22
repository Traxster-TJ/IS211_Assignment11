from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

#list of To-Do items
todo_list = []

@app.route('/')
def index():
    return render_template('index.html', todo_list=todo_list)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')
    
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        return redirect(url_for('index'))
  
    
    if priority not in ['Low', 'Medium', 'High']:
        return redirect(url_for('index'))
    
    
    todo_list.append({
        'task': task,
        'email': email,
        'priority': priority
    })
    
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    todo_list.clear()
    return redirect(url_for('index'))

# Extra Credit I: 
import os
import pickle

@app.route('/save', methods=['POST'])
def save():
    with open('todolist.pkl', 'wb') as f:
        pickle.dump(todo_list, f)
    return redirect(url_for('index'))

# Extra Credit II:
@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if 0 <= index < len(todo_list):
        todo_list.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Extra Credit I: Load saved list if it exists
    if os.path.exists('todolist.pkl'):
        with open('todolist.pkl', 'rb') as f:
            todo_list = pickle.load(f)
    
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from itertools import combinations

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['POST'])
def tasks():
    tasks = request.form.get('tasks').split('\n')
    session['tasks'] = tasks
    session['comparisons'] = list(combinations(range(len(tasks)), 2))
    session['scores'] = [0] * len(tasks)
    return redirect(url_for('compare'))

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        choice = int(request.form.get('choice'))
        scores = session['scores']
        scores[choice] += 1
        session['scores'] = scores  # Reassign to ensure the session updates

        comparisons = session['comparisons']
        comparisons.pop(0)
        session['comparisons'] = comparisons  # Reassign to ensure the session updates
    
    if session['comparisons']:
        pair = session['comparisons'][0]
        task1 = session['tasks'][pair[0]]
        task2 = session['tasks'][pair[1]]
        return render_template('compare.html', task1=task1, task2=task2, pair=pair)
    else:
        return redirect(url_for('results'))

@app.route('/results')
def results():
    tasks = session['tasks']
    scores = session['scores']
    ranked_tasks = sorted(zip(tasks, scores), key=lambda x: x[1], reverse=True)
    return render_template('results.html', ranked_tasks=ranked_tasks)

if __name__ == '__main__':
    app.run(debug=True)

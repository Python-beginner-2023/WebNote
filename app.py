import os
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

CHAT_FILE = 'chat.txt'


def read_messages():
    if not os.path.exists(CHAT_FILE):
        return []
    with open(CHAT_FILE, 'r') as f:
        lines = f.readlines()
    messages = []
    for line in lines:
        parts = line.strip().split('\t')
        timestamp = datetime.fromisoformat(parts[0])
        content = parts[1]
        messages.append((timestamp, content))
    return messages


def write_message(content):
    with open(CHAT_FILE, 'a') as f:
        f.write(f'{datetime.now().isoformat()}\t{content}\n')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        write_message(content)
        return redirect('/')
    else:
        messages = read_messages()
        messages.reverse()
        return render_template('index.html.jinja2', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
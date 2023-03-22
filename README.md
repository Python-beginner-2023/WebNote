# WebNote
一个基于Web的留言板，类似于一个在线便笺板，用户可以在上面留下笔记和评论


AI：GPT 3.5 turbo

提问及回答记录：

prompt：😐: 你是一个和我一起进行结对编程的程序员，我向你提出问题，你实现我的需求，并给出代码。你准备好了吗？
AI：🖥: <code>当然，随时准备为您服务！请告诉我您有什么需求。

prompt：😐: 我们现在要用Flask编写一个Web留言板。留言板有一个页面，这个页面分为上下两部分，上面列出了过去的历史留言，并且以时间戳逆序排序。下半部分是一个多行文本框和一个提交按钮，用户在这里提交新留言。请用flask实现这个留言板，并给我一个示例代码，你需要输入 app.py, index.html.jinja2, requirements.txt 这三个文件的源代码。
AI：好的，下面是示例代码：
**app.py**

```python
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
        return render_template('index.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
```

**index.html.jinja2**

```html
<!DOCTYPE html>
<html>
    <head>
        <title>留言板</title>
    </head>
    <body>
        <div>
            <h1>留言板</h1>
            <ul>
                {% for message in messages %}
                    <li>{{ message[0] }}: {{ message[1] }}</li>
                {% endfor %}
            </ul>
        </div>
        <div>
            <form method="POST" action="/">
                <label for="content">留言：</label>
                <textarea id="content" name="content"></textarea>
                <br>
                <button type="submit">提交</button>
            </form>
        </div>
    </body>
</html>
```

**requirements.txt**

```
Flask==2.0.1
```

在这个版本的示例代码中，我们不再使用 Flask-SQLAlchemy，而是在服务器上单独处理聊天记录。聊天记录现在存储在名为“chat.txt”的文本文件中，每个聊天消息都已保存在单独的一行中，其中第一个部分是时间戳，第二个部分是消息内容。提取聊天记录时，我们遍历这个文本文件并将每个消息转换为元组，其中第一个部分是 `datetime` 对象，第二个部分是消息内容（字符串）。在提交新消息时，我们将其附加到文件末尾，因此所有消息都将在同一个文件中存储。</code></pre>


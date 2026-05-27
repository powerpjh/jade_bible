from flask import Flask, render_template_string, request

app = Flask(__name__)

# 52주 통독 데이터 (간단 예시)
BIBLE_DATA = [
    {"week": i, "range": f"성경 통독 {i}주차 범위", "checked": False} for i in range(1, 53)
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>제이드의 52주 성경 통독</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; padding: 20px; background-color: #f4f6f9; color: #333; }
        h1 { text-align: center; color: #2c3e50; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .week-item { display: flex; align-items: center; justify-content: space-between; padding: 12px; border-bottom: 1px solid #eee; }
        .week-item:last-child { border-bottom: none; }
        input[type="checkbox"] { width: 20px; height: 20px; cursor: pointer; }
        .checked-text { text-decoration: line-through; color: #aaa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📖 제이드의 성경 통독</h1>
        <p style="text-align:center; color:#666;">언제 어디서나 체크하는 나만의 통독 표</p>
        <div id="list">
            {% for item in data %}
            <div class="week-item">
                <span><strong>{{ item.week }}주차:</strong> {{ item.range }}</span>
                <input type="checkbox" {% if item.checked %}checked{% endif %}>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, data=BIBLE_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

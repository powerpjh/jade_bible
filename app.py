import os
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# 성경책 한글 이름과 파일 내부 약어 매핑 사전 (가장 안전한 연결창 매칭)
BIBLE_MAP = {
    "창세기": "창", "출애굽기": "출", "레위기": "레", "민수기": "민", "신명기": "신",
    "여호수아": "수", "사사기": "삿", "룻기": "룻", "사무엘상": "삼상", "사무엘하": "삼하",
    "열왕기상": "왕상", "열왕기하": "왕하", "역대상": "대상", "역대하": "대하", "에스라": "스",
    "느헤미야": "느", "에스더": "에", "욥기": "욥", "시편": "시", "잠언": "잠",
    "전도서": "전", "아가": "아", "이사야": "사", "예레미야": "렘", "예레미야애가": "애",
    "에스겔": "겔", "다니엘": "단", "호세아": "호", "요엘": "욜", "아모스": "암",
    "오바댜": "옵", "요나": "요나", "미가": "미", "나훔": "나", "하박국": "합",
    "스바냐": "습", "학개": "학", "스가랴": "슥", "말라기": "말",
    "마태복음": "마", "마가복음": "막", "누가복음": "눅", "요한복음": "요", "사도행전": "행",
    "로마서": "롬", "고린도전서": "고전", "고린도후서": "고후", "갈라디아서": "갈", "에베소서": "엡",
    "빌립보서": "빌", "골로새서": "골", "데살로니가전서": "데전", "데살로니가후서": "데후",
    "디모데전서": "디전", "디모데후서": "디후", "디도서": "딛", "빌레몬서": "몬", "히브리서": "히",
    "야고보서": "약", "베드로전서": "벧전", "베드로후서": "벧후", "요한1서": "요일", "요한2서": "요이",
    "요한3서": "요삼", "유다서": "유", "요한계시록": "계"
}

RAW_PLAN = [
    {
        "part": "PART 1: 초대 그리스도인이 현대 그리스도인에게",
        "steps": [
            {"step": "STEP 01", "books": [("베드로전서", list(range(1, 6))), ("마가복음", list(range(1, 17))), ("베드로후서", list(range(1, 4)))]},
            {"step": "STEP 02", "books": [("빌립보서", list(range(1, 5))), ("데살로니가전서", list(range(1, 6))), ("데살로니가후서", list(range(1, 4))), ("디모데전서", list(range(1, 7))), ("디모데후서", list(range(1, 5)))]}
        ]
    },
    {
        "part": "PART 2: 인생 최대의 질문 다섯 가지",
        "steps": [
            {"step": "STEP 03", "books": [("전도서", list(range(1, 13))), ("시편", [37, 38, 39, 41]), ("욥기", list(range(1, 4))), ("시편", [49, 73, 88])]},
            {"step": "STEP 04", "books": [("욥기", list(range(4, 27)))]},
            {"step": "STEP 05", "books": [("에베소서", list(range(1, 7))), ("욥기", list(range(27, 43)))]},
            {"step": "STEP 06", "books": [("창세기", [1, 2]), ("시편", [1, 8, 19, 104, 148]), ("창세기", [3]), ("시편", [14]), ("창세기", [4, 5]), ("시편", [10]), ("창세기", [6, 7]), ("시편", [29]), ("창세기", [8, 9]), ("시편", [9, 32, 33, 65])]},
            {"step": "STEP 07", "books": [("요한복음", list(range(1, 22))), ("시편", [22, 69])]}
        ]
    },
    {
        "part": "PART 3: 하나님의 나라가 이 땅에 이루어지이다",
        "steps": [
            {"step": "STEP 08", "books": [("시편", [2]), ("창세기", list(range(10, 21))), ("로마서", list(range(1, 12)))]},
            {"step": "STEP 09", "books": [("갈라디아서", list(range(1, 7))), ("창세기", list(range(21, 28))), ("로마서", list(range(12, 17))), ("시편", [15, 131, 67, 86])]},
            {"step": "STEP 10", "books": [("창세기", list(range(28, 51)))]},
            {"step": "STEP 11", "books": [("출애굽기", list(range(1, 16))), ("시편", [114, 136, 77]), ("출애굽기", list(range(16, 19))), ("시편", [105, 78])]},
            {"step": "STEP 12", "books": [("출애굽기", list(range(19, 41))), ("시편", [97, 99])]},
            {"step": "STEP 13", "books": [("히브리서", list(range(1, 14))), ("야고보서", list(range(1, 6))), ("시편", [95, 110, 117, 119])]},
            {"step": "STEP 14", "books": [("골로새서", list(range(1, 5))), ("레위기", list(range(1, 17))), ("시편", [20, 50, 103])]},
            {"step": "STEP 15", "books": [("요한1서", [1, 2, 3, 4, 5]), ("레위기", list(range(17, 28))), ("빌레몬서", [1]), ("잠언", [31])]},
            {"step": "STEP 16", "books": [("민수기", list(range(1, 18))), ("고린도전서", list(range(1, 7))), ("유다서", [1])]},
            {"step": "STEP 17", "books": [("민수기", list(range(18, 37))), ("고린도전서", list(range(7, 11)))]}
        ]
    }
]

processed_plan = []
for p_idx, p in enumerate(RAW_PLAN):
    step_list = []
    for s_idx, s in enumerate(p["steps"]):
        book_list = []
        for b_idx, (b_title, ch_list) in enumerate(s["books"]):
            book_id = f"p{p_idx}-s{s_idx}-b{b_idx}"
            book_list.append({
                "id": book_id,
                "title": b_title,
                "chapters": ch_list
            })
        step_list.append({
            "step_num": s["step"],
            "books": book_list
        })
    processed_plan.append({
        "part_title": p["part"],
        "steps": step_list
    })

html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>제이드의 52주 성경통독 독립앱</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f0f2f5; padding: 20px; margin: 0; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { text-align: center; color: #1a2a6c; margin-bottom: 30px; font-size: 1.6em; }
        .part { background-color: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; padding: 25px; border-left: 6px solid #1a2a6c; }
        .part-title { font-size: 1.2em; font-weight: bold; color: #1a2a6c; padding-bottom: 10px; margin-bottom: 20px; border-bottom: 1px dashed #ddd; }
        .step { background: #f8f9fa; border-radius: 8px; padding: 15px; margin-bottom: 15px; border: 1px solid #e9ecef; }
        .step-num { font-size: 1.0em; font-weight: bold; color: #e96479; margin-bottom: 10px; display: inline-block; background: #ffeef1; padding: 2px 8px; border-radius: 4px; }
        .book { margin-left: 10px; margin-bottom: 12px; }
        .book-title { font-weight: bold; color: #495057; display: block; margin-bottom: 6px; font-size: 0.95em; }
        .chapters { display: flex; flex-wrap: wrap; gap: 6px; }
        .chapter { 
            display: inline-block; min-width: 32px; height: 32px; line-height: 32px; text-align: center; 
            border: 1px solid #ced4da; border-radius: 6px; background-color: #fff; cursor: pointer; user-select: none; 
            font-size: 0.85em; color: #495057; transition: all 0.2s;
        }
        .chapter:hover { background-color: #e9ecef; }
        .chapter.checked { background-color: #2b8a3e; color: white; border-color: #2b8a3e; font-weight: bold; }
        
        .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); }
        .modal-content { background-color: #fff; margin: 8% auto; padding: 25px; border-radius: 16px; width: 85%; max-width: 600px; max-height: 75vh; overflow-y: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1a2a6c; padding-bottom: 10px; margin-bottom: 15px; }
        .modal-title { font-size: 1.3em; font-weight: bold; color: #1a2a6c; }
        .close-btn { font-size: 28px; font-weight: bold; color: #aaa; cursor: pointer; }
        .close-btn:hover { color: #000; }
        .bible-text { font-size: 1.15em; line-height: 1.8; color: #222; text-align: justify; word-break: keep-all; }
        .verse { margin-bottom: 12px; }
        .verse-num { font-weight: bold; color: #e96479; margin-right: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📖 제이드의 개역한글 성경통독 마스터</h1>
        {% for part in plan %}
        <div class="part">
            <div class="part-title">{{ part.part_title }}</div>
            {% for step in part.steps %}
            <div class="step">
                <div class="step-num">{{ step.step_num }}</div>
                {% for book in step.books %}
                <div class="book">
                    <span class="book-title">📍 {{ book.title }}</span>
                    <div class="chapters">
                        {% for chapter in book.chapters %}
                        <div class="chapter" 
                             id="btn-{{ book.id }}-{{ chapter }}" 
                             data-book="{{ book.title }}"
                             data-chapter="{{ chapter }}"
                             onclick="readBible(this)">{{ chapter }}</div>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>

    <div id="bibleModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="modal-title" id="modalTitle">성경 말씀</span>
                <span class="close-btn" onclick="closeModal()">&times;</span>
            </div>
            <div class="bible-text" id="modalBody">
                말씀을 불러오는 중입니다...
            </div>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            document.querySelectorAll('.chapter').forEach(function(element) {
                if (localStorage.getItem(element.id) === "checked") {
                    element.classList.add('checked');
                }
            });
        });

        function readBible(element) {
            element.classList.toggle('checked');
            if (element.classList.contains('checked')) {
                localStorage.setItem(element.id, "checked");
            } else {
                localStorage.removeItem(element.id);
            }

            const book = element.getAttribute('data-book');
            const chapter = element.getAttribute('data-chapter');
            
            document.getElementById('modalTitle').innerText = `${book} ${chapter}장`;
            document.getElementById('modalBody').innerText = "통짜 파일에서 말씀을 검색하고 있습니다...";
            document.getElementById('bibleModal').style.display = "block";

            fetch(`/get_bible?book=${encodeURIComponent(book)}&chapter=${chapter}`)
                .then(response => response.json())
                .then(data => {
                    const body = document.getElementById('modalBody');
                    body.innerHTML = "";
                    if (data.error) {
                        body.innerText = data.error;
                    } else {
                        data.verses.forEach(v => {
                            body.innerHTML += `<div class="verse"><span class="verse-num">${v.num}</span>${v.text}</div>`;
                        });
                    }
                })
                .catch(err => {
                    document.getElementById('modalBody').innerText = "성경 파일을 읽어오지 못했습니다. 파일명을 확인해 주세요!";
                });
        }

        function closeModal() {
            document.getElementById('bibleModal').style.display = "none";
        }

        window.onclick = function(event) {
            const modal = document.getElementById('bibleModal');
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, plan=processed_plan)

# 🎯 제이드님이 업로드하신 한 개의 큰 파일에서 구절을 기가 막히게 뽑아내는 안전 필터 기능!
@app.route('/get_bible')
def get_bible():
    book = request.args.get('book', '')
    chapter = request.args.get('chapter', '')
    
    file_name = "개역한글판성경.txt"
    short_code = BIBLE_MAP.get(book, "")
    
    # 🎯 핵심 수정: 파일 내부에는 "민1:1" 처럼 저장되어 있으므로 패턴을 정확히 일치시킴
    prefix = f"{short_code}{chapter}:" 
    verses = []
    
    try:
        with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # 라인 맨 앞에 prefix가 있는지 확인
                if line.startswith(prefix):
                    parts = line.split(' ', 1)
                    text = parts[1] if len(parts) > 1 else ""
                    # "민1:1" 에서 "1"만 추출
                    vs_num = parts[0].split(':')[1]
                    verses.append({"num": vs_num, "text": text})
    except Exception as e:
        return jsonify({"error": "파일을 읽는 중 오류가 발생했습니다."})
    
    return jsonify({"verses": verses})

import os
from flask import Flask, render_template_string

app = Flask(__name__)

# 한글엘프(hocr.net) 사이트의 성경별 고유 코드 매핑
BIBLE_CODE_MAP = {
    "창세기": "gen", "출애굽기": "exo", "레위기": "lev", "민수기": "num", "신명기": "deu",
    "여호수아": "jos", "사사기": "jdg", "룻기": "rut", "사무엘상": "1sa", "사무엘하": "2sa",
    "열왕기상": "1ki", "열왕기하": "2ki", "역대상": "1ch", "역대하": "2ch", "에스라": "ezr",
    "느헤미야": "neh", "에스더": "est", "욥기": "job", "시편": "psa", "잠언": "pro",
    "전도서": "ecc", "아가": "sng", "이사야": "isa", "예레미야": "jer", "예레미야애가": "lam",
    "에스겔": "ezk", "다니엘": "dan", "호세아": "hos", "요엘": "jol", "아모스": "amo",
    "오바디야": "oba", "요나": "jon", "미가": "mic", "나훔": "nam", "하박국": "hab",
    "스바냐": "zep", "학개": "hag", "스가랴": "zec", "말라기": "mal",
    "마태복음": "mat", "마가복음": "mrk", "누가복음": "luk", "요한복음": "jhn", "사도행전": "act",
    "로마서": "rom", "고린도전서": "1co", "고린도후서": "2co", "갈라디아서": "gal", "에베소서": "eph",
    "빌립보서": "php", "골로새서": "col", "데살로니가전서": "1th", "데살로니가후서": "2th", "디모데전서": "1ti",
    "디모데후서": "2ti", "디도서": "tit", "빌레몬서": "phm", "히브리서": "heb", "야고보서": "jas",
    "베드로전서": "1pe", "베드로후서": "2pe", "요한1서": "1jn", "요한2서": "2jn", "요한3서": "3jn",
    "유다서": "jud", "요한계시록": "rev"
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
    },
    {
        "part": "PART 4: 하나님의 통치 안에 거하는 삶",
        "steps": [
            {"step": "STEP 18", "books": [("고린도전서", list(range(1, 17))), ("고린도후서", list(range(1, 14))), ("시편", [68, 81, 107])]},
            {"step": "STEP 19", "books": [("신명기", list(range(1, 12))), ("잠언", list(range(1, 11))), ("시편", [90, 91])]},
            {"step": "STEP 20", "books": [("신명기", list(range(12, 27))), ("잠언", list(range(11, 19)))]},
            {"step": "STEP 21", "books": [("신명기", list(range(27, 35))), ("잠언", list(range(19, 30))), ("시편", [94, 112])]},
            {"step": "STEP 22", "books": [("여호수아", list(range(1, 25)))]},
            {"step": "STEP 23", "books": [("사사기", list(range(1, 22))), ("시편", [106])]},
            {"step": "STEP 24", "books": [("룻기", list(range(1, 5))), ("사무엘상", list(range(1, 17))), ("시편", [23, 113])]}
        ]
    },
    {
        "part": "PART 5: 王의 길, 선지자의 길",
        "steps": [
            {"step": "STEP 25", "books": [("역대상", [1, 2]), ("마태복음", list(range(1, 21)))]},
            {"step": "STEP 26", "books": [("마태복음", list(range(21, 29))), ("역대상", list(range(3, 10))), ("사무엘상", [17, 18, 19]), ("시편", [118, 139])]},
            {"step": "STEP 27", "books": [("사무엘상", list(range(20, 27))), ("시편", [34, 52, 54, 56, 57, 58, 59, 63, 64, 109, 140, 141, 142])]},
            {"step": "STEP 28", "books": [("사무엘상", list(range(27, 32))), ("사무엘하", [1]), ("역대상", [10]), ("시편", [6, 13, 16, 28, 98])]},
            {"step": "STEP 29", "books": [("사무엘하", list(range(2, 11))), ("역대상", list(range(11, 20))), ("시편", [21, 24, 25, 51, 60, 66, 89, 96, 101, 132])]},
            {"step": "STEP 30", "books": [("사무엘하", list(range(11, 21))), ("시편", [3, 4, 42, 43, 55, 61, 62, 71, 143, 144])]},
            {"step": "STEP 31", "books": [("사무엘하", [21, 22, 23, 24]), ("역대상", [21, 22, 23, 24, 25, 26, 27, 28, 29]), ("열왕기상", [1, 2]), ("시편", [18, 30, 72, 145])]},
            {"step": "STEP 32", "books": [("열왕기상", list(range(3, 12))), ("역대하", list(range(1, 10))), ("아가", list(range(1, 9))), ("시편", [45, 135, 136])]},
            {"step": "STEP 33", "books": [("열왕기상", [12, 13, 14, 15, 16]), ("역대하", list(range(10, 17))), ("오바디야", [1]), ("요엘", list(range(1, 4)))]},
            {"step": "STEP 34", "books": [("열왕기상", list(range(17, 23))), ("열왕기하", list(range(1, 9))), ("역대하", list(range(17, 22))), ("호세아", list(range(1, 15)))]},
            {"step": "STEP 35", "books": [("아모스", list(range(1, 10))), ("요나", list(range(1, 5))), ("열왕기하", [9, 10, 11, 12, 13, 14]), ("역대하", [22, 23, 24, 25]), ("이사야", list(range(1, 7)))]},
            {"step": "STEP 36", "books": [("미가", list(range(1, 8))), ("열왕기하", [15, 16]), ("역대하", [26, 27, 28]), ("이사야", list(range(7, 13)))]}
        ]
    },
    {
        "part": "PART 6: 멸망과 심판 속에서 외친 예언자들",
        "steps": [
            {"step": "STEP 37", "books": [("열왕기하", [17, 18, 19, 20, 21]), ("역대하", [29, 30, 31, 32, 33]), ("이사야", list(range(36, 40))), ("시편", [46, 47, 48, 76, 80, 133])]},
            {"step": "STEP 38", "books": [("이사야", list(range(13, 36)))]},
            {"step": "STEP 39", "books": [("이사야", list(range(40, 67)))]},
            {"step": "STEP 40", "books": [("나훔", list(range(1, 4))), ("스바냐", list(range(1, 4))), ("하박국", list(range(1, 4))), ("열왕기하", [22, 23]), ("역대하", [34, 35]), ("예레미야", list(range(1, 11)))]},
            {"step": "STEP 41", "books": [("예레미야", [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 25, 26, 35, 36, 45, 46, 47, 48, 49]), ("열왕기하", [24]), ("역대하", [36])]},
            {"step": "STEP 42", "books": [("예레미야", [21, 24, 27, 28, 29, 30, 31, 32, 33, 34, 37, 38, 39, 52])]}
        ]
    },
    {
        "part": "PART 7: 절망 속에서 보는 소망",
        "steps": [
            {"step": "STEP 43", "books": [("예레미야애가", list(range(1, 6))), ("예레미야", [40, 41, 42, 43, 44, 50, 51]), ("열왕기하", [25]), ("시편", [74, 79, 137])]},
            {"step": "STEP 44", "books": [("다니엘", list(range(1, 13)))]},
            {"step": "STEP 45", "books": [("에스겔", list(range(1, 25)))]},
            {"step": "STEP 46", "books": [("에스겔", list(range(25, 49)))]},
            {"step": "STEP 47", "books": [("에스라", list(range(1, 7))), ("학개", [1, 2]), ("스가랴", list(range(1, 15))), ("시편", [121, 124, 127, 128, 146, 147])]}
        ]
    },
    {
        "part": "PART 8: 메시아가 오시다",
        "steps": [
            {"step": "STEP 48", "books": [("에스더", list(range(1, 11))), ("에스라", list(range(7, 11))), ("시편", [120, 125, 129])]},
            {"step": "STEP 49", "books": [("느헤미야", list(range(1, 14))), ("말라기", list(range(1, 5))), ("시편", [126, 133])]},
            {"step": "STEP 50", "books": [("누가복음", list(range(1, 25)))]},
            {"step": "STEP 51", "books": [("로마서", list(range(1, 17)))]},
            {"step": "STEP 52", "books": [("사도행전", list(range(1, 29))), ("요한계시록", list(range(1, 23)))]}
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
                "code": BIBLE_CODE_MAP.get(b_title, "gen"),
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
    <title>제이드의 52주 통독 마스터 앱</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f0f2f5; padding: 20px; margin: 0; padding-bottom: 120px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { text-align: center; color: #1a2a6c; margin-bottom: 30px; font-size: 1.6em; word-break: keep-all; }
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
        .chapter:hover { background-color: #e9ecef; border-color: #adb5bd; }
        .chapter.checked { background-color: #2b8a3e; color: white; border-color: #2b8a3e; font-weight: bold; }
        .bible-bar {
            position: fixed; bottom: 0; left: 0; right: 0;
            background-color: #ffffff; box-shadow: 0 -4px 15px rgba(0,0,0,0.1);
            padding: 15px 20px; display: none; z-index: 1000;
            border-top-left-radius: 16px; border-top-right-radius: 16px;
        }
        .bible-bar-content { max-width: 900px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .bible-info { font-size: 1.0em; font-weight: bold; color: #333; }
        .bible-btn {
            background-color: #e96479; color: white; border: none;
            padding: 10px 18px; font-size: 0.95em; font-weight: bold;
            border-radius: 8px; cursor: pointer; text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📖 제이드의 52주 성경통독 마스터</h1>
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
                             data-code="{{ book.code }}"
                             data-chapter="{{ chapter }}"
                             onclick="toggleCheck(this)">{{ chapter }}</div>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>

    <div class="bible-bar" id="bibleBar">
        <div class="bible-bar-content">
            <div class="bible-info" id="bibleInfo">선택된 장 정보</div>
            <a href="#" target="_blank" class="bible-btn" id="bibleLink">📖 우리말성경 읽기</a>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            document.querySelectorAll('.chapter').forEach(function(element) {
                var savedState = localStorage.getItem(element.id);
                if (savedState === "checked") {
                    element.classList.add('checked');
                }
            });
        });

        function toggleCheck(element) {
            element.classList.toggle('checked');
            const bookTitle = element.getAttribute('data-book');
            const bibleCode = element.getAttribute('data-code');
            const chapter = element.getAttribute('data-chapter');
            const bar = document.getElementById('bibleBar');
            
            if (element.classList.contains('checked')) {
                localStorage.setItem(element.id, "checked");
                
                document.getElementById('bibleInfo').innerText = `📍 ${bookTitle} ${chapter}장`;
                
                const padChapter = String(chapter).padStart(2, '0');
                document.getElementById('bibleLink').href = `https://hnocr.net/korwrm/read.php?b=${bibleCode}&c=${padChapter}`;
                
                bar.style.display = 'block';
            } else {
                localStorage.removeItem(element.id);
                bar.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, plan=processed_plan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

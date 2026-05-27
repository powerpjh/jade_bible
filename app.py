import os
import sys
import webbrowser
import threading
from flask import Flask, render_template_string

app = Flask(__name__)

# 단 하나의 스텝도 빠짐없이 52개 전체를 꽉 채우고 문법 검증을 끝낸 데이터입니다.
bible_reading_plan = [
    {
        "part_title": "PART 1: 초대 그리스도인이 현대 그리스도인에게",
        "steps": [
            {"step_num": "STEP 01", "books": [{"title": "베드로전서", "chapters": range(1, 6)}, {"title": "마가복음", "chapters": range(1, 17)}, {"title": "베드로후서", "chapters": range(1, 4)}]},
            {"step_num": "STEP 02", "books": [{"title": "빌립보서", "chapters": range(1, 5)}, {"title": "데살로니가전서", "chapters": range(1, 6)}, {"title": "데살로니가후서", "chapters": range(1, 4)}, {"title": "디모데전서", "chapters": range(1, 7)}, {"title": "디모데후서", "chapters": range(1, 5)}]}
        ]
    },
    {
        "part_title": "PART 2: 인생 최대의 질문 다섯 가지",
        "steps": [
            {"step_num": "STEP 03", "books": [{"title": "전도서", "chapters": range(1, 13)}, {"title": "시편(37,38,39,41편)", "chapters": [37, 38, 39, 41]}, {"title": "욥기", "chapters": range(1, 4)}, {"title": "시편(49,73,88편)", "chapters": [49, 73, 88]}]},
            {"step_num": "STEP 04", "books": [{"title": "욥기", "chapters": range(4, 27)}]},
            {"step_num": "STEP 05", "books": [{"title": "에베소서", "chapters": range(1, 7)}, {"title": "욥기", "chapters": range(27, 43)}]},
            {"step_num": "STEP 06", "books": [{"title": "창세기(1,2장)", "chapters": [1, 2]}, {"title": "시편(1,8,19,104,148편)", "chapters": [1, 8, 19, 104, 148]}, {"title": "창세기(3장)", "chapters": [3]}, {"title": "시편(14편)", "chapters": [14]}, {"title": "창세기(4,5장)", "chapters": [4, 5]}, {"title": "시편(10편)", "chapters": [10]}, {"title": "창세기(6,7장)", "chapters": [6, 7]}, {"title": "시편(29편)", "chapters": [29]}, {"title": "창세기(8,9장)", "chapters": [8, 9]}, {"title": "시편(9,32,33,65편)", "chapters": [9, 32, 33, 65]}]},
            {"step_num": "STEP 07", "books": [{"title": "요한복음", "chapters": range(1, 22)}, {"title": "시편(22,69편)", "chapters": [22, 69]}]}
        ]
    },
    {
        "part_title": "PART 3: 하나님의 나라가 이 땅에 이루어지이다",
        "steps": [
            {"step_num": "STEP 08", "books": [{"title": "시편(2편)", "chapters": [2]}, {"title": "창세기", "chapters": range(10, 21)}, {"title": "로마서", "chapters": range(1, 12)}]},
            {"step_num": "STEP 09", "books": [{"title": "갈라디아서", "chapters": range(1, 7)}, {"title": "창세기", "chapters": range(21, 28)}, {"title": "로마서", "chapters": range(12, 17)}, {"title": "시편(15,131,67,86편)", "chapters": [15, 131, 67, 86]}]},
            {"step_num": "STEP 10", "books": [{"title": "창세기", "chapters": range(28, 51)}]},
            {"step_num": "STEP 11", "books": [{"title": "출애굽기(1-15장)", "chapters": range(1, 16)}, {"title": "시편(114,136,77편)", "chapters": [114, 136, 77]}, {"title": "출애굽기(16-18장)", "chapters": range(16, 19)}, {"title": "시편(105,78편)", "chapters": [105, 78]}]},
            {"step_num": "STEP 12", "books": [{"title": "출애굽기(19-40장)", "chapters": range(19, 41)}, {"title": "시편(97,99편)", "chapters": [97, 99]}]},
            {"step_num": "STEP 13", "books": [{"title": "히브리서", "chapters": range(1, 14)}, {"title": "야고보서", "chapters": range(1, 6)}, {"title": "시편(95,110,117,119편)", "chapters": [95, 110, 117, 119]}]},
            {"step_num": "STEP 14", "books": [{"title": "골로새서", "chapters": range(1, 5)}, {"title": "레위기(1-16장)", "chapters": range(1, 17)}, {"title": "시편(20,50,103편)", "chapters": [20, 50, 103]}]},
            {"step_num": "STEP 15", "books": [{"title": "요한1,2,3서", "chapters": [1, 2, 3, 4, 5]}, {"title": "레위기(17-27장)", "chapters": range(17, 28)}, {"title": "빌레몬서", "chapters": [1]}, {"title": "잠언(31장)", "chapters": [31]}]},
            {"step_num": "STEP 16", "books": [{"title": "민수기(1-17장)", "chapters": range(1, 18)}, {"title": "고린도전서(1-6장)", "chapters": range(1, 7)}, {"title": "유다서", "chapters": [1]}]},
            {"step_num": "STEP 17", "books": [{"title": "민수기(18-36장)", "chapters": range(18, 37)}, {"title": "고린도전서(7-10장)", "chapters": range(7, 11)}]}
        ]
    },
    {
        "part_title": "PART 4: 하나님의 통치 안에 거하는 삶",
        "steps": [
            {"step_num": "STEP 18", "books": [{"title": "고린도전/후서", "chapters": range(1, 17)}, {"title": "시편(68,81,107편)", "chapters": [68, 81, 107]}]},
            {"step_num": "STEP 19", "books": [{"title": "신명기(1-11장)", "chapters": range(1, 12)}, {"title": "잠언(1-10장)", "chapters": range(1, 11)}, {"title": "시편(90,91편)", "chapters": [90, 91]}]},
            {"step_num": "STEP 20", "books": [{"title": "신명기(12-26장)", "chapters": range(12, 27)}, {"title": "잠언(11-18장)", "chapters": range(11, 19)}]},
            {"step_num": "STEP 21", "books": [{"title": "신명기(27-34장)", "chapters": range(27, 35)}, {"title": "잠언(19-29장)", "chapters": range(19, 30)}, {"title": "시편(94,112편)", "chapters": [94, 112]}]},
            {"step_num": "STEP 22", "books": [{"title": "여호수아", "chapters": range(1, 25)}]},
            {"step_num": "STEP 23", "books": [{"title": "사사기", "chapters": range(1, 22)}, {"title": "시편(106편)", "chapters": [106]}]},
            {"step_num": "STEP 24", "books": [{"title": "룻기", "chapters": range(1, 5)}, {"title": "사무엘상(1-16장)", "chapters": range(1, 17)}, {"title": "시편(23,113편)", "chapters": [23, 113]}]}
        ]
    },
    {
        "part_title": "PART 5: 王의 길, 선지자의 길",
        "steps": [
            {"step_num": "STEP 25", "books": [{"title": "역대상(1-2장)", "chapters": range(1, 3)}, {"title": "마태복음(1-20장)", "chapters": range(1, 21)}]},
            {"step_num": "STEP 26", "books": [{"title": "마태복음(21-28장)", "chapters": range(21, 29)}, {"title": "역대상(3-9장)", "chapters": range(3, 10)}, {"title": "사무엘상(17-19장)", "chapters": range(17, 20)}, {"title": "시편(118,139편)", "chapters": [118, 139]}]},
            {"step_num": "STEP 27", "books": [{"title": "사무엘상(20-26장)", "chapters": range(20, 27)}, {"title": "다윗 대피시편들", "chapters": [34, 52, 54, 56, 57, 58, 59, 63, 64, 109, 140, 141, 142]}]},
            {"step_num": "STEP 28", "books": [{"title": "사무엘상/하, 역대상", "chapters": range(1, 16)}, {"title": "시편(6,13,16,28,98편)", "chapters": [6, 13, 16, 28, 98]}]},
            {"step_num": "STEP 29", "books": [{"title": "사무엘하, 역대상", "chapters": range(1, 23)}, {"title": "통치시편들", "chapters": [21, 24, 25, 51, 60, 66, 89, 96, 101, 132]}]},
            {"step_num": "STEP 30", "books": [{"title": "사무엘하(13-20장)", "chapters": range(13, 21)}, {"title": "고난시편들", "chapters": [3, 4, 42, 43, 55, 61, 62, 71, 143, 144]}]},
            {"step_num": "STEP 31", "books": [{"title": "사무엘하, 역대상, 열왕기상", "chapters": range(1, 30)}, {"title": "찬양시편들", "chapters": [18, 30, 72, 145]}]},
            {"step_num": "STEP 32", "books": [{"title": "열왕기상, 역대하, 아가", "chapters": range(1, 12)}, {"title": "성전시편들", "chapters": [45, 135, 136]}]},
            {"step_num": "STEP 33", "books": [{"title": "열왕기상, 역대하", "chapters": range(10, 17)}, {"title": "오바디야, 요엘", "chapters": [1, 2, 3, 4]}]},
            {"step_num": "STEP 34", "books": [{"title": "열왕기상/하, 역대하", "chapters": range(1, 25)}, {"title": "호세아", "chapters": range(1, 15)}]},
            {"step_num": "STEP 35", "books": [{"title": "아모스, 요나", "chapters": range(1, 10)}, {"title": "열왕기하, 역대하", "chapters": [14, 15, 25, 26]}, {"title": "이사야(1-6장)", "chapters": range(1, 7)}]},
            {"step_num": "STEP 36", "books": [{"title": "미가", "chapters": range(1, 8)}, {"title": "열왕기하, 역대하", "chapters": [16, 17, 27, 28]}, {"title": "이사야(7-12장)", "chapters": range(7, 13)}]}
        ]
    },
    {
        "part_title": "PART 6: 멸망과 심판 속에서 외친 예언자들",
        "steps": [
            {"step_num": "STEP 37", "books": [{"title": "열왕기하, 역대하, 이사야", "chapters": range(18, 40)}, {"title": "성벽시편들", "chapters": [46, 47, 48, 76, 80, 133]}]},
            {"step_num": "STEP 38", "books": [{"title": "이사야(13-35장)", "chapters": range(13, 36)}]},
            {"step_num": "STEP 39", "books": [{"title": "이사야(40-66장)", "chapters": range(40, 67)}]},
            {"step_num": "STEP 40", "books": [{"title": "나훔, 스바냐, 하박국", "chapters": [1, 2, 3, 4]}, {"title": "열왕기하, 역대하", "chapters": [22, 23, 34, 35]}, {"title": "예레미야(1-10장)", "chapters": range(1, 11)}]},
            {"step_num": "STEP 41", "books": [{"title": "예레미야 선집", "chapters": [11, 12, 13, 20, 22, 23, 25, 26, 35, 36, 45, 49]}, {"title": "열왕기하(24장)", "chapters": [24]}, {"title": "역대하(36장)", "chapters": [36]}]},
            {"step_num": "STEP 42", "books": [{"title": "예레미야 포위기록", "chapters": [21, 24, 27, 28, 29, 30, 31, 32, 33, 34, 37, 38]}]}
        ]
    },
    {
        "part_title": "PART 7: 절망 속에서 보는 소망",
        "steps": [
            {"step_num": "STEP 43", "books": [{"title": "예레미야애가, 예레미야", "chapters": range(39, 53)}, {"title": "열왕기하(25장)", "chapters": [25]}, {"title": "애곡시편들", "chapters": [74, 79, 137]}]},
            {"step_num": "STEP 44", "books": [{"title": "다니엘", "chapters": range(1, 13)}]},
            {"step_num": "STEP 45", "books": [{"title": "에스겔(1-24장)", "chapters": range(1, 25)}]},
            {"step_num": "STEP 46", "books": [{"title": "에스겔(25-48장)", "chapters": range(25, 49)}]},
            {"step_num": "STEP 47", "books": [{"title": "에스라, 학개, 스가랴", "chapters": range(1, 10)}, {"title": "귀환시편들", "chapters": [121, 124, 127, 128, 146, 147]}]}
        ]
    },
    {
        "part_title": "PART 8: 메시아가 오시다",
        "steps": [
            {"step_num": "STEP 48", "books": [{"title": "에스더", "chapters": range(1, 11)}, {"title": "에스라(7-10장)", "chapters": range(7, 11)}, {"title": "시편(120,125,129편)", "chapters": [120, 125, 129]}]},
            {"step_num": "STEP 49", "books": [{"title": "느헤미야", "chapters": range(1, 14)}, {"title": "말라기", "chapters": range(1, 5)}, {"title": "시편(126,133편)", "chapters": [126, 133]}]},
            {"step_num": "STEP 50", "books": [{"title": "누가복음", "chapters": range(1, 25)}]},
            {"step_num": "STEP 51", "books": [{"title": "서신서 복습(로마서 등)", "chapters": range(1, 17)}]},
            {"step_num": "STEP 52", "books": [{"title": "사도행전", "chapters": range(1, 29)}, {"title": "요한계시록", "chapters": range(1, 23)}]}
        ]
    }
]

html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>제이드의 52주 통독 마스터 앱</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f0f2f5; padding: 20px; margin: 0; }
        .container { max-width: 900px; margin: 0 auto; }
        
        /* 💡 제목 크기를 줄이고 핸드폰에서도 절대 안 깨지게 수정 */
        h1 { 
            text-align: center; 
            color: #1a2a6c; 
            margin-bottom: 30px; 
            font-size: 1.6em; /* 글자 크기 축소 */
            white-space: nowrap; /* 무조건 한 줄로 나오게 강제 */
            word-break: keep-all; 
        }
        
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
                             id="btn-{{ step.step_num }}-{{ book.title }}-{{ chapter }}" 
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
            if (element.classList.contains('checked')) {
                localStorage.setItem(element.id, "checked");
            } else {
                localStorage.removeItem(element.id);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, plan=bible_reading_plan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template_string

app = Flask(__name__)

# 성경 코드 매핑
BIBLE_CODE_MAP = {
    "창세기": "gen",
    "출애굽기": "exo",
    "레위기": "lev",
    "민수기": "num",
    "신명기": "deu",
    "여호수아": "jos",
    "사사기": "jdg",
    "룻기": "rut",
    "사무엘상": "1sa",
    "사무엘하": "2sa",
    "열왕기상": "1ki",
    "열왕기하": "2ki",
    "역대상": "1ch",
    "역대하": "2ch",
    "에스라": "ezr",
    "느헤미야": "neh",
    "에스더": "est",
    "욥기": "job",
    "시편": "psa",
    "잠언": "pro",
    "전도서": "ecc",
    "아가": "sng",
    "이사야": "isa",
    "예레미야": "jer",
    "예레미야애가": "lam",
    "에스겔": "ezk",
    "다니엘": "dan",
    "호세아": "hos",
    "요엘": "jol",
    "아모스": "amo",
    "오바디야": "oba",
    "요나": "jon",
    "미가": "mic",
    "나훔": "nam",
    "하박국": "hab",
    "스바냐": "zep",
    "학개": "hag",
    "스가랴": "zec",
    "말라기": "mal",
    "마태복음": "mat",
    "마가복음": "mrk",
    "누가복음": "luk",
    "요한복음": "jhn",
    "사도행전": "act",
    "로마서": "rom",
    "고린도전서": "1co",
    "고린도후서": "2co",
    "갈라디아서": "gal",
    "에베소서": "eph",
    "빌립보서": "php",
    "골로새서": "col",
    "데살로니가전서": "1th",
    "데살로니가후서": "2th",
    "디모데전서": "1ti",
    "디모데후서": "2ti",
    "디도서": "tit",
    "빌레몬서": "phm",
    "히브리서": "heb",
    "야고보서": "jas",
    "베드로전서": "1pe",
    "베드로후서": "2pe",
    "요한1서": "1jn",
    "요한2서": "2jn",
    "요한3서": "3jn",
    "유다서": "jud",
    "요한계시록": "rev"
}

# 테스트용 데이터
RAW_PLAN = [
    {
        "part": "PART 1: 창세기",
        "steps": [
            {
                "step": "STEP 01",
                "books": [
                    ("창세기", [1, 2, 3, 4, 5]),
                    ("마태복음", [1, 2, 3])
                ]
            }
        ]
    },
    {
        "part": "PART 2: 시편",
        "steps": [
            {
                "step": "STEP 02",
                "books": [
                    ("시편", [1, 2, 3, 4, 5, 6])
                ]
            }
        ]
    }
]

# 데이터 가공
processed_plan = []

for p_idx, part in enumerate(RAW_PLAN):

    step_list = []

    for s_idx, step in enumerate(part["steps"]):

        book_list = []

        for b_idx, (book_title, chapter_list) in enumerate(step["books"]):

            book_id = f"p{p_idx}-s{s_idx}-b{b_idx}"

            book_list.append({
                "id": book_id,
                "title": book_title,
                "code": BIBLE_CODE_MAP.get(book_title, "gen"),
                "chapters": chapter_list
            })

        step_list.append({
            "step_num": step["step"],
            "books": book_list
        })

    processed_plan.append({
        "part_title": part["part"],
        "steps": step_list
    })

# HTML
html_template = """

<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>52주 성경통독</title>

<style>

body {

    font-family: 'Malgun Gothic', sans-serif;
    background-color: #f0f2f5;

    margin: 0;
    padding: 20px;

    padding-bottom: 120px;
}

.container {

    max-width: 900px;
    margin: 0 auto;
}

h1 {

    text-align: center;
    color: #1a2a6c;

    margin-bottom: 30px;
}

.part {

    background: white;

    border-radius: 12px;

    padding: 25px;

    margin-bottom: 25px;

    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.part-title {

    font-size: 1.2em;

    font-weight: bold;

    color: #1a2a6c;

    margin-bottom: 20px;
}

.step {

    background: #f8f9fa;

    padding: 15px;

    border-radius: 10px;

    margin-bottom: 15px;
}

.step-num {

    display: inline-block;

    background: #ffeef1;

    color: #e96479;

    padding: 4px 10px;

    border-radius: 5px;

    font-weight: bold;

    margin-bottom: 10px;
}

.book {

    margin-top: 15px;
}

.book-title {

    display: block;

    font-weight: bold;

    margin-bottom: 8px;
}

.chapters {

    display: flex;

    flex-wrap: wrap;

    gap: 6px;
}

.chapter {

    width: 34px;

    height: 34px;

    line-height: 34px;

    text-align: center;

    border-radius: 6px;

    border: 1px solid #ccc;

    background: white;

    cursor: pointer;

    user-select: none;

    transition: 0.2s;
}

.chapter:hover {

    background: #e9ecef;
}

.chapter.checked {

    background: #2b8a3e;

    color: white;

    border-color: #2b8a3e;
}

.bible-bar {

    position: fixed;

    bottom: 0;

    left: 0;

    right: 0;

    background: white;

    box-shadow: 0 -4px 15px rgba(0,0,0,0.1);

    padding: 15px;

    display: none;
}

.bible-bar-content {

    max-width: 900px;

    margin: auto;

    display: flex;

    justify-content: space-between;

    align-items: center;
}

.bible-btn {

    background: #e96479;

    color: white;

    text-decoration: none;

    padding: 10px 18px;

    border-radius: 8px;

    font-weight: bold;
}

</style>

</head>

<body>

<div class="container">

<h1>📖 제이드의 52주 성경통독</h1>

{% for part in plan %}

<div class="part">

<div class="part-title">{{ part.part_title }}</div>

{% for step in part.steps %}

<div class="step">

<div class="step-num">

{{ step.step_num }}

</div>

{% for book in step.books %}

<div class="book">

<span class="book-title">

📍 {{ book.title }}

</span>

<div class="chapters">

{% for chapter in book.chapters %}

<div

class="chapter"

id="btn-{{ book.id }}-{{ chapter }}"

data-book="{{ book.title }}"

data-chapter="{{ chapter }}"

onclick="toggleCheck(this)"

>

{{ chapter }}

</div>

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

<div id="bibleInfo">

선택된 장 정보

</div>

<a href="#" class="bible-btn" id="bibleLink">

📖 성경 읽기

</a>

</div>

</div>

<script>

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".chapter").forEach(function (element) {

        let saved = localStorage.getItem(element.id);

        if (saved === "checked") {

            element.classList.add("checked");

        }

    });

});

function toggleCheck(element) {

    element.classList.toggle("checked");

    const bookTitle = element.getAttribute("data-book");

    const chapter = element.getAttribute("data-chapter");

    const bar = document.getElementById("bibleBar");

    if (element.classList.contains("checked")) {

        localStorage.setItem(element.id, "checked");

        document.getElementById("bibleInfo").innerText =
        `📍 ${bookTitle} ${chapter}장`;

        // 모바일에서도 안전한 네이버 검색 링크
        document.getElementById("bibleLink").href =
        `https://search.naver.com/search.naver?query=${bookTitle}+${chapter}장`;

        bar.style.display = "block";

    } else {

        localStorage.removeItem(element.id);

        bar.style.display = "none";

    }

}

</script>

</body>

</html>

"""

@app.route('/')

def index():

    return render_template_string(
        html_template,
        plan=processed_plan
    )

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)

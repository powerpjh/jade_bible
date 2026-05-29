// ── 책 이름 → 약어 매핑 ──
const bookMap = {
    "갈라디아서": "갈", "고린도전서": "고전", "고린도후서": "고후",
    "골로새서": "골", "나훔": "나", "누가복음": "눅", "느헤미야": "느",
    "다니엘": "단", "데살로니가전서": "살전", "데살로니가후서": "살후",
    "디모데전서": "딤전", "디모데후서": "딤후", "레위기": "레",
    "로마서": "롬", "룻기": "룻", "마가복음": "막", "마태복음": "마",
    "말라기": "말", "미가": "미", "민수기": "민", "베드로전서": "벧전",
    "베드로후서": "벧후", "빌레몬서": "몬", "빌립보서": "빌",
    "사도행전": "행", "사무엘상": "삼상", "사무엘하": "삼하",
    "사사기": "삿", "스가랴": "슥", "스바냐": "습", "시편": "시",
    "신명기": "신", "아가": "아", "아모스": "암", "야고보서": "약",
    "에베소서": "엡", "에스겔": "겔", "에스더": "에", "에스라": "스",
    "여호수아": "수", "역대상": "대상", "역대하": "대하",
    "열왕기상": "왕상", "열왕기하": "왕하", "예레미야": "렘",
    "예레미야애가": "애", "오바댜": "옵", "요나": "욘", "요엘": "욜",
    "요한계시록": "계", "요한복음": "요", "요한일서": "요일",
    "욥기": "욥", "유다서": "유", "이사야": "사", "잠언": "잠",
    "전도서": "전", "창세기": "창", "출애굽기": "출", "하박국": "합",
    "학개": "학", "호세아": "호", "히브리서": "히"
};

const container  = document.getElementById('plan-container');
const verseTitle   = document.getElementById('verse-title');
const verseContent = document.getElementById('verse-content');

// ── 통독표 생성 ──
function createPlan() {
    bibleReadingPlan.forEach(part => {
        const partDiv = document.createElement('div');
        partDiv.className = 'part';

        partDiv.innerHTML = `<div class="part-title">${part.part_title}</div>`;

        part.steps.forEach(step => {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'step';
            stepDiv.innerHTML = `<div class="step-title">${step.step_num}</div>`;

            step.books.forEach(book => {
                const bookDiv = document.createElement('div');
                bookDiv.className = 'book';
                bookDiv.innerHTML = `<div class="book-title">📍 ${book.title}</div>`;

                const chaptersDiv = document.createElement('div');
                chaptersDiv.className = 'chapters';

                book.chapters.forEach(chapter => {
                    const btn = document.createElement('button');
                    btn.className = 'chapter';
                    btn.textContent = chapter;

                    // localStorage 키: "창세기-1"
                    const key = `${book.title}-${chapter}`;
                    if (localStorage.getItem(key) === 'done') {
                        btn.classList.add('checked');
                    }

                    btn.addEventListener('click', () => {
                        loadBibleChapter(book.title, chapter);
                        toggleCheck(btn, key);
                    });

                    chaptersDiv.appendChild(btn);
                });

                bookDiv.appendChild(chaptersDiv);
                stepDiv.appendChild(bookDiv);
            });

            partDiv.appendChild(stepDiv);
        });

        container.appendChild(partDiv);
    });
}

// ── 체크 저장/해제 ──
function toggleCheck(btn, key) {
    btn.classList.toggle('checked');
    if (btn.classList.contains('checked')) {
        localStorage.setItem(key, 'done');
    } else {
        localStorage.removeItem(key);
    }
}

// ── 성경 본문 불러오기 ──
async function loadBibleChapter(bookTitle, chapter) {
    verseTitle.textContent = `${bookTitle} ${chapter}장`;
    verseContent.innerHTML = '<p style="color:#aaa">불러오는 중...</p>';

    const shortName = bookMap[bookTitle];
    if (!shortName) {
        verseContent.innerHTML = `<p style="color:red">❗ bookMap에 "${bookTitle}" 약어를 추가해주세요.</p>`;
        return;
    }

    try {
        const res = await fetch(`bible/${bookTitle}.txt`);
        if (!res.ok) throw new Error('파일 없음');
        const text = await res.text();

        const lines = text.split(/\r?\n/).filter(line =>
            line.startsWith(`${shortName}${chapter}:`)
        );

        if (lines.length === 0) {
            verseContent.innerHTML = '<p style="color:#aaa">해당 장을 찾을 수 없습니다.</p>';
            return;
        }

        verseContent.innerHTML = '';
        lines.forEach(line => {
            const div = document.createElement('div');
            div.className = 'verse';

            // "창1:1 태초에..." → "1:1 태초에..."
            const body = line.replace(`${shortName}${chapter}:`, `${chapter}:`);
            const colonIdx = body.indexOf(' ');
            const ref = body.substring(0, colonIdx);
            const txt = body.substring(colonIdx + 1);

            div.innerHTML = `<span class="verse-num">${ref}</span>${txt}`;
            verseContent.appendChild(div);
        });

        // 본문 뷰어로 스크롤
        document.getElementById('verse-viewer').scrollIntoView({ behavior: 'smooth' });
        localStorage.setItem('lastRead', `${bookTitle}-${chapter}`);

    } catch (e) {
        verseContent.innerHTML = `
            <p style="color:#e63946">
                📂 <strong>bible/${bookTitle}.txt</strong> 파일을 찾을 수 없습니다.<br>
                bible 폴더에 txt 파일을 넣어주세요.
            </p>`;
    }
}

// ── 시작 ──
createPlan();
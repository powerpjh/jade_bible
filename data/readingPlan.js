const range = (start, end) => Array.from({ length: end - start }, (_, i) => start + i);

const bibleReadingPlan = [
    {
        "part_title": "PART 1: 초대 그리스도인이 현대 그리스도인에게",
        "steps": [
            { "step_num": "STEP 01", "books": [{ "title": "베드로전서", "chapters": range(1, 6) }, { "title": "마가복음", "chapters": range(1, 17) }, { "title": "베드로후서", "chapters": range(1, 4) }] },
            { "step_num": "STEP 02", "books": [{ "title": "빌립보서", "chapters": range(1, 5) }, { "title": "데살로니가전서", "chapters": range(1, 6) }, { "title": "데살로니가후서", "chapters": range(1, 4) }, { "title": "디모데전서", "chapters": range(1, 7) }, { "title": "디모데후서", "chapters": range(1, 5) }] }
        ]
    },
    {
        "part_title": "PART 2: 인생 최대의 질문 다섯 가지",
        "steps": [
            { "step_num": "STEP 03", "books": [{ "title": "전도서", "chapters": range(1, 13) }, { "title": "시편", "chapters": [37, 38, 39, 41] }, { "title": "욥기", "chapters": range(1, 4) }, { "title": "시편", "chapters": [49, 73, 88] }] },
            { "step_num": "STEP 04", "books": [{ "title": "욥기", "chapters": range(4, 27) }] },
            { "step_num": "STEP 05", "books": [{ "title": "에베소서", "chapters": range(1, 7) }, { "title": "욥기", "chapters": range(27, 43) }] },
            { "step_num": "STEP 06", "books": [{ "title": "창세기", "chapters": [1, 2] }, { "title": "시편", "chapters": [1, 8, 19, 104, 148] }, { "title": "창세기", "chapters": [3] }, { "title": "시편", "chapters": [14] }, { "title": "창세기", "chapters": [4, 5] }, { "title": "시편", "chapters": [10] }, { "title": "창세기", "chapters": [6, 7] }, { "title": "시편", "chapters": [29] }, { "title": "창세기", "chapters": [8, 9] }, { "title": "시편", "chapters": [9, 32, 33, 65] }] },
            { "step_num": "STEP 07", "books": [{ "title": "요한복음", "chapters": range(1, 22) }, { "title": "시편", "chapters": [22, 69] }] }
        ]
    },
    {
        "part_title": "PART 3: 하나님의 나라가 이 땅에 이루어지이다",
        "steps": [
            { "step_num": "STEP 08", "books": [{ "title": "시편", "chapters": [2] }, { "title": "창세기", "chapters": range(10, 21) }, { "title": "로마서", "chapters": range(1, 12) }] },
            { "step_num": "STEP 09", "books": [{ "title": "갈라디아서", "chapters": range(1, 7) }, { "title": "창세기", "chapters": range(21, 28) }, { "title": "로마서", "chapters": range(12, 17) }, { "title": "시편", "chapters": [15, 131, 67, 86] }] },
            { "step_num": "STEP 10", "books": [{ "title": "창세기", "chapters": range(28, 51) }] },
            { "step_num": "STEP 11", "books": [{ "title": "출애굽기", "chapters": range(1, 16) }, { "title": "시편", "chapters": [114, 136, 77] }, { "title": "출애굽기", "chapters": range(16, 19) }, { "title": "시편", "chapters": [105, 78] }] },
            { "step_num": "STEP 12", "books": [{ "title": "출애굽기", "chapters": range(19, 41) }, { "title": "시편", "chapters": [97, 99] }] },
            { "step_num": "STEP 13", "books": [{ "title": "히브리서", "chapters": range(1, 14) }, { "title": "야고보서", "chapters": range(1, 6) }, { "title": "시편", "chapters": [95, 110, 117, 119] }] },
            { "step_num": "STEP 14", "books": [{ "title": "골로새서", "chapters": range(1, 5) }, { "title": "레위기", "chapters": range(1, 17) }, { "title": "시편", "chapters": [20, 50, 103] }] },
            { "step_num": "STEP 15", "books": [{ "title": "요한일서", "chapters": range(1, 6) }, { "title": "레위기", "chapters": range(17, 28) }, { "title": "빌레몬서", "chapters": [1] }, { "title": "잠언", "chapters": [31] }] },
            { "step_num": "STEP 16", "books": [{ "title": "민수기", "chapters": range(1, 18) }, { "title": "고린도전서", "chapters": range(1, 7) }, { "title": "유다서", "chapters": [1] }] },
            { "step_num": "STEP 17", "books": [{ "title": "민수기", "chapters": range(18, 37) }, { "title": "고린도전서", "chapters": range(7, 11) }] }
        ]
    },
    {
        "part_title": "PART 4: 하나님의 통치 안에 거하는 삶",
        "steps": [
            { "step_num": "STEP 18", "books": [{ "title": "고린도전서", "chapters": range(1, 17) }, { "title": "시편", "chapters": [68, 81, 107] }] },
            { "step_num": "STEP 19", "books": [{ "title": "신명기", "chapters": range(1, 12) }, { "title": "잠언", "chapters": range(1, 11) }, { "title": "시편", "chapters": [90, 91] }] },
            { "step_num": "STEP 20", "books": [{ "title": "신명기", "chapters": range(12, 27) }, { "title": "잠언", "chapters": range(11, 19) }] },
            { "step_num": "STEP 21", "books": [{ "title": "신명기", "chapters": range(27, 35) }, { "title": "잠언", "chapters": range(19, 30) }, { "title": "시편", "chapters": [94, 112] }] },
            { "step_num": "STEP 22", "books": [{ "title": "여호수아", "chapters": range(1, 25) }] },
            { "step_num": "STEP 23", "books": [{ "title": "사사기", "chapters": range(1, 22) }, { "title": "시편", "chapters": [106] }] },
            { "step_num": "STEP 24", "books": [{ "title": "룻기", "chapters": range(1, 5) }, { "title": "사무엘상", "chapters": range(1, 17) }, { "title": "시편", "chapters": [23, 113] }] }
        ]
    },
    {
        "part_title": "PART 5: 王의 길, 선지자의 길",
        "steps": [
            { "step_num": "STEP 25", "books": [{ "title": "역대상", "chapters": range(1, 3) }, { "title": "마태복음", "chapters": range(1, 21) }] },
            { "step_num": "STEP 26", "books": [{ "title": "마태복음", "chapters": range(21, 29) }, { "title": "역대상", "chapters": range(3, 10) }, { "title": "사무엘상", "chapters": range(17, 20) }, { "title": "시편", "chapters": [118, 139] }] },
            { "step_num": "STEP 27", "books": [{ "title": "사무엘상", "chapters": range(20, 27) }, { "title": "시편", "chapters": [34, 52, 54, 56, 57, 58, 59, 63, 64, 109, 140, 141, 142] }] },
            { "step_num": "STEP 28", "books": [{ "title": "사무엘상", "chapters": range(1, 16) }, { "title": "시편", "chapters": [6, 13, 16, 28, 98] }] },
            { "step_num": "STEP 29", "books": [{ "title": "사무엘하", "chapters": range(1, 23) }, { "title": "시편", "chapters": [21, 24, 25, 51, 60, 66, 89, 96, 101, 132] }] },
            { "step_num": "STEP 30", "books": [{ "title": "사무엘하", "chapters": range(13, 21) }, { "title": "시편", "chapters": [3, 4, 42, 43, 55, 61, 62, 71, 143, 144] }] },
            { "step_num": "STEP 31", "books": [{ "title": "사무엘하", "chapters": range(1, 30) }, { "title": "시편", "chapters": [18, 30, 72, 145] }] },
            { "step_num": "STEP 32", "books": [{ "title": "열왕기상", "chapters": range(1, 12) }, { "title": "시편", "chapters": [45, 135, 136] }] },
            { "step_num": "STEP 33", "books": [{ "title": "열왕기상", "chapters": range(10, 17) }, { "title": "오바댜", "chapters": [1] }, { "title": "요엘", "chapters": range(1, 4) }] },
            { "step_num": "STEP 34", "books": [{ "title": "열왕기상", "chapters": range(1, 25) }, { "title": "호세아", "chapters": range(1, 15) }] },
            { "step_num": "STEP 35", "books": [{ "title": "아모스", "chapters": range(1, 10) }, { "title": "요나", "chapters": range(1, 5) }, { "title": "이사야", "chapters": range(1, 7) }] },
            { "step_num": "STEP 36", "books": [{ "title": "미가", "chapters": range(1, 8) }, { "title": "이사야", "chapters": range(7, 13) }] }
        ]
    },
    {
        "part_title": "PART 6: 멸망과 심판 속에서 외친 예언자들",
        "steps": [
            { "step_num": "STEP 37", "books": [{ "title": "열왕기하", "chapters": range(18, 40) }, { "title": "시편", "chapters": [46, 47, 48, 76, 80, 133] }] },
            { "step_num": "STEP 38", "books": [{ "title": "이사야", "chapters": range(13, 36) }] },
            { "step_num": "STEP 39", "books": [{ "title": "이사야", "chapters": range(40, 67) }] },
            { "step_num": "STEP 40", "books": [{ "title": "나훔", "chapters": range(1, 4) }, { "title": "스바냐", "chapters": range(1, 4) }, { "title": "하박국", "chapters": range(1, 4) }, { "title": "예레미야", "chapters": range(1, 11) }] },
            { "step_num": "STEP 41", "books": [{ "title": "예레미야", "chapters": [11, 12, 13, 20, 22, 23, 25, 26, 35, 36, 45, 49] }] },
            { "step_num": "STEP 42", "books": [{ "title": "예레미야", "chapters": [21, 24, 27, 28, 29, 30, 31, 32, 33, 34, 37, 38] }] }
        ]
    },
    {
        "part_title": "PART 7: 절망 속에서 보는 소망",
        "steps": [
            { "step_num": "STEP 43", "books": [{ "title": "예레미야애가", "chapters": range(1, 6) }, { "title": "예레미야", "chapters": range(39, 53) }, { "title": "시편", "chapters": [74, 79, 137] }] },
            { "step_num": "STEP 44", "books": [{ "title": "다니엘", "chapters": range(1, 13) }] },
            { "step_num": "STEP 45", "books": [{ "title": "에스겔", "chapters": range(1, 25) }] },
            { "step_num": "STEP 46", "books": [{ "title": "에스겔", "chapters": range(25, 49) }] },
            { "step_num": "STEP 47", "books": [{ "title": "에스라", "chapters": range(1, 7) }, { "title": "학개", "chapters": range(1, 3) }, { "title": "스가랴", "chapters": range(1, 15) }, { "title": "시편", "chapters": [121, 124, 127, 128, 146, 147] }] }
        ]
    },
    {
        "part_title": "PART 8: 메시아가 오시다",
        "steps": [
            { "step_num": "STEP 48", "books": [{ "title": "에스더", "chapters": range(1, 11) }, { "title": "에스라", "chapters": range(7, 11) }, { "title": "시편", "chapters": [120, 125, 129] }] },
            { "step_num": "STEP 49", "books": [{ "title": "느헤미야", "chapters": range(1, 14) }, { "title": "말라기", "chapters": range(1, 5) }, { "title": "시편", "chapters": [126, 133] }] },
            { "step_num": "STEP 50", "books": [{ "title": "누가복음", "chapters": range(1, 25) }] },
            { "step_num": "STEP 51", "books": [{ "title": "로마서", "chapters": range(1, 17) }] },
            { "step_num": "STEP 52", "books": [{ "title": "사도행전", "chapters": range(1, 29) }, { "title": "요한계시록", "chapters": range(1, 23) }] }
        ]
    }
];
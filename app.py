import os
import sys
from flask import Flask, render_template_string

app = Flask(__name__)

# 한글엘프(hocr.net) 사이트의 각 성경별 고유 주소 번호 매핑 테이블
bible_url_mapping = {
    "창세기": "gen", "출애굽기(1-15장)": "exo", "출애굽기(19-40장)": "exo", "레위기(1-16장)": "lev", "레위기(17-27장)": "lev",
    "민수기(1-17장)": "num", "민수기(18-36장)": "num", "신명기(1-11장)": "deu", "신명기(12-26장)": "deu", "신명기(27-34장)": "deu",
    "여호수아": "jos", "사사기": "jdg", "룻기": "rut", "사무엘상(1-16장)": "1sa", "사무엘상(17-19장)": "1sa", "사무엘상(20-26장)": "1sa",
    "사무엘상/하, 역대상": "1sa", "사무엘하, 역대상": "2sa", "사무엘하(13-20장)": "2sa", "사무엘하, 역대상, 열왕기상": "2sa",
    "열왕기상, 역대하, 아가": "1ki", "열왕기상, 역대하": "1ki", "열왕기상/하, 역대하": "1ki", "열왕기하, 역대하": "2ki",
    "열왕기하, 역대하, 이사야": "2ki", "역대상(1-2장)": "1ch", "역대상(3-9장)": "1ch", "에스라, 학개, 스가랴": "ezr",
    "에스라(7-10장)": "ezr", "느헤미야": "neh", "에스더": "est", "욥기": "job", "전도서": "ecc", "아가": "sng",
    "이사야(1-6장)": "isa", "이사야(7-12장)": "isa", "이사야(13-35장)": "isa", "이사야(40-66장)": "isa",
    "예레미야(1-10장)": "jer", "예레미야 선집": "jer", "예레미야 포위기록": "jer", "예레미야애가, 예레미야": "lam",
    "에스겔(1-24장)": "ezk", "에스겔(25-48장)": "ezk", "다니엘": "dan", "호세아": "hos", "요엘": "jol",
    "아모스, 요나": "amo", "오바디야, 요엘": "oba", "요나": "jon", "미가": "mic", "나훔, 스바냐, 하박국": "nam",
    "하박국": "hab", "스바냐": "zep", "학개": "hag", "스가랴": "zec", "말라기": "mal",
    "마태복음(1-20장)": "mat", "마태복음(21-28장)": "mat", "마가복음": "mrk", "누가복음": "luk", "요한복음": "jhn",
    "사도행전": "act", "로마서": "rom", "서신서 복습(로마서 등)": "rom", "고린도전서(1-6장)": "1co", "고린도전서(7-10장)": "1co",
    "고린도전/후서": "1co", "갈라디아서": "gal", "에베소서": "eph", "빌립보서": "php", "골로새서": "col",
    "데살로니가전서": "1th", "데살로니가후서": "2th", "디모데전서": "1ti", "디모데후서": "2ti", "디도서": "tit",
    "빌레몬서": "phm", "히브리서": "heb", "야고보서": "jas", "베드로전서": "1pe", "베드로후서": "2pe",
    "요한1,2,3서": "1jn", "유다서": "jud", "요한계시록": "rev",
    "시편(37,38,39,41편)": "psa", "시편(49,73,88편)": "psa", "시편(1,8,19,104,148편)": "psa", "시편(3장)": "psa",
    "창세기(1,2장)": "gen", "창세기(3장)": "gen", "창세기(4,5장)": "gen", "창세기(6,7장)": "gen", "창세기(8,9장)": "gen",
    "시편(14편)": "psa", "시편(10편)": "psa", "시편(29편)": "psa", "시편(9,32,33,65편)": "psa", "시편(22,69편)": "psa",
    "시편(2편)": "psa", "시편(15,131,67,86편)": "psa", "시편(114,136,77편)": "psa", "시편(105,78편)": "psa",
    "시편(97,99편)": "psa", "시편(95,110,117,119편)": "psa", "시편(20,50,103편)": "psa", "잠언(31장)": "pro",
    "잠언(1-10장)": "pro", "잠언(11-18장)": "pro", "잠언(19-29장)": "pro", "시편(90,91편)": "psa",
    "시편(94,112편)": "psa", "시편(106편)": "psa", "시편(23,113편)": "psa", "다윗 대피시편들": "psa",
    "시편(6,13,16,28,98편)": "psa", "통치시편들": "psa", "고난시편들": "psa", "찬양시편들": "psa",
    "성전시편들": "psa", "성벽시편들": "psa", "애곡시편들": "psa", "귀환시편들": "psa", "시편(120,125,129편)": "psa",
    "시편(126,133편)": "psa"
}

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
            {"step_num": "STEP 42", "books":

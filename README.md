# 📚 Library CI/CD – ระบบยืม-คืนหนังสือห้องสมุด

Mini-Project รายวิชา 832208/632218 เดฟออปและการผสมผสานระบบ ภาคเรียนที่ 1/2569
จัดทำโดย Peeraphat Aisising รหัสนักศึกษา 6752410001

## ระบบที่เลือก
ระบบยืม-คืนหนังสือของห้องสมุดขนาดเล็ก (เว็บแอป Python + Flask) ทำงานได้จริงแต่ไม่ครบทุกฟังก์ชันของระบบห้องสมุดจริง

| ฟังก์ชัน | รายละเอียด |
|---|---|
| ดูรายการหนังสือ | แสดงสถานะ ว่าง / ถูกยืม / เกินกำหนดคืน |
| ค้นหา | ค้นจากชื่อหนังสือหรือผู้แต่ง |
| เพิ่มหนังสือ | กรอกชื่อและผู้แต่ง ระบบออกรหัสให้อัตโนมัติ |
| ยืมหนังสือ | ระบุชื่อผู้ยืม กำหนดคืน 7 วัน ยืมซ้ำไม่ได้ |
| คืนหนังสือ | คืนแล้วสถานะกลับเป็นว่าง |
| Health check | `GET /health` ใช้ตรวจหลัง Deploy |

## วิธีรันบนเครื่อง
```bash
pip install -r requirements.txt
python app.py
# เปิด http://localhost:5000
```

## โครงสร้างโปรเจกต์
```
library-cicd/
├── app.py             เว็บแอป Flask (หน้าเว็บ + routes)
├── library.py         ตรรกะยืม-คืน (แยกจากหน้าเว็บเพื่อให้ทดสอบง่าย)
├── templates/
│   └── index.html     หน้าเว็บ
├── test_library.py    Unit test ของตรรกะ (10 กรณี)
├── test_app.py        ทดสอบหน้าเว็บผ่าน Flask test client (4 กรณี)
├── smoke_check.py     ตรวจแอปหลัง Deploy
├── requirements.txt   flask, pytest, flake8
├── Jenkinsfile        Pipeline CI/CD
└── .gitignore
```

## CI/CD ด้วย GitHub + Jenkins

```
นักพัฒนา ──git push──▶ GitHub ──(Jenkins poll ทุก 2 นาที)──▶ Jenkins Pipeline
                                                         │
   Checkout → Setup Python → Lint → Test → Build → Deploy ┘
```

| Stage | ทำอะไร | ถ้าล้มเหลว |
|---|---|---|
| Checkout | ดึงโค้ดล่าสุดจาก GitHub | หยุด pipeline |
| Setup Python | สร้าง venv และติดตั้ง requirements | หยุด pipeline |
| Lint | ตรวจโค้ดด้วย flake8 | โค้ดผิดรูปแบบจะไม่ถูก deploy |
| Test | รัน pytest 14 กรณี และเก็บผลเป็น JUnit report | โค้ดที่ทำให้ระบบพังจะไม่ถูก deploy |
| Build | บีบอัดเป็น `dist/library-cicd-<build>.zip` และเก็บเป็น artifact | - |
| Deploy | คัดลอกไปที่ `C:\JenkinsDeploy\library-cicd` แล้วรัน smoke check | แจ้ง failure |

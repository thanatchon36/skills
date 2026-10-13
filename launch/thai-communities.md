NOT READY: the README's first screen has no real example (it starts at line 64), and this draft describes the 7 skills of v0.1.0, not the 8 in v0.2.0 (eval-harness is missing). Fix both before posting.

# กลุ่มนักพัฒนาไทย

## ที่ที่น่าโพสต์

- **Thai Programmer (Facebook group):** กลุ่มนักพัฒนาทั่วไป เหมาะกับ flow หลัก เช็กกฎเรื่องโปรโมตผลงานตัวเองก่อนโพสต์
- **Python Thailand (Facebook group):** โพสต์โดยเปิดด้วย `leakage-audit` เพราะคนในกลุ่มใช้ pandas/sklearn กันเยอะ
- **กลุ่ม AI/LLM หรือ Claude ภาษาไทยที่คุณอยู่:** TBD เลือกกลุ่มเอง
- **Blognone:** ส่งเป็น news tip ได้ แต่ไม่ควรโพสต์ขายของเอง

## โพสต์

coding agent ทุกวันนี้เขียนโค้ดได้ดีแล้วครับ แต่งานอีกครึ่งของการปล่อยโปรเจกต์ open source มันชอบข้าม
เช่น ไม่ตรวจก่อนบอกว่าเสร็จ แต่ง output ใส่ README เอง หรือเผลอทำให้ repo เป็น public ก่อนเราจะได้ดู
(TBD: ใส่ประสบการณ์จริงของคุณเองถ้ามี)

เลยเขียน agent skills ขึ้นมา 7 ตัว ทำเป็น Claude Code plugin

- `/mission-brief` ถามทีละข้อ แล้วเขียน MISSION.md ที่มี success criteria ตรวจได้จริง
- `/ship-oss` ทำตาม brief ทีละ phase และจะหยุดรอให้พิมพ์ "go" ก่อนสร้าง repo, push, tag หรือ release
- `/launch-kit` ร่างโพสต์เปิดตัว (โพสต์นี้ก็ร่างจากตัวนี้) แต่ไม่โพสต์ให้เอง
- `runtime-drift` หาว่า `.nvmrc`, Dockerfile และ CI ใช้เวอร์ชัน Node/Python/Go ไม่ตรงกันตรงไหน
- `leakage-audit` หา data leakage ในโค้ด pandas, scikit-learn, PySpark บอก `file:line` ทุกจุด

ทุก skill มี eval ทั้ง prompt ที่ควรเรียกและที่ต้องไม่เรียก ผลอยู่ใน `docs/evals.md`
ข้อจำกัดคือตอนนี้ทดสอบกับ Claude Code อย่างเดียว agent อื่นติดตั้งผ่าน `npx skills` ได้แต่ยังไม่ได้ทดสอบ

ติดตั้ง:

```text
/plugin marketplace add thanatchon36/skills
/plugin install thanatchon-skills@thanatchon
```

https://github.com/thanatchon36/skills

ถ้าลองแล้วเจอ skill ทำงานผิดจังหวะ เปิด issue บอกได้เลยครับ ช่วยผมได้มากที่สุด

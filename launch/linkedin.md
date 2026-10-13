# LinkedIn

Plain text, since LinkedIn doesn't render Markdown. The first two lines show before "see more".
Pick one language per post, or post the Thai version a day later.

## English (about 210 words)

```text
Coding agents are good at writing code. They're much worse at the rest of shipping an open-source project: deciding what "done" means, writing a README a stranger can act on, cutting a release, announcing it.

So I built eight agent skills for that part, packaged as a Claude Code plugin.

The main flow:
→ /mission-brief interviews you and writes a one-page brief with checkable success criteria
→ /ship-oss executes it phase by phase, and stops for an explicit "go" before creating a repo, pushing, tagging, or releasing
→ /launch-kit drafts posts like this one, and never posts them

Plus four standalone skills: README review, runtime-version drift, ML data-leakage audits, and LLM eval sets.

What surprised me: the evals caught bugs that trying a few prompts never would have. One skill sometimes counted the same problem twice and reported 5 issues instead of 4. Another correctly redacted a card number from the logs, but its report never said so. Both were fixed in the skill itself, not by loosening the test.

Every skill is also tested on prompts that must NOT trigger it.

MIT licensed and tested with Claude Code. Other agents can install it via npx skills, but I haven't tested those yet.

https://github.com/thanatchon36/skills

If a skill fires when it shouldn't, I'd love to hear about it.

#ClaudeCode #OpenSource #AIAgents
```

## ภาษาไทย

```text
coding agent ทุกวันนี้เขียนโค้ดเก่งแล้วครับ แต่งานอีกครึ่งของการปล่อยโปรเจกต์ open source มันยังทำได้ไม่ดี ทั้งการตกลงว่า "เสร็จ" คืออะไร เขียน README ให้คนแปลกหน้าลองใช้ได้ทันที ออก release และประกาศเปิดตัว

ผมเลยเขียน agent skills ขึ้นมา 8 ตัวสำหรับงานส่วนนี้ ทำเป็น Claude Code plugin

flow หลัก:
→ /mission-brief ถามทีละข้อ แล้วเขียน brief หน้าเดียวที่มี success criteria ตรวจสอบได้
→ /ship-oss ทำตาม brief ทีละ phase และหยุดรอให้เราพิมพ์ "go" ก่อนสร้าง repo, push, tag หรือ release
→ /launch-kit ร่างโพสต์แบบโพสต์นี้ แต่ไม่โพสต์ให้เอง

และ skill เดี่ยวอีก 4 ตัว: รีวิว README, หาเวอร์ชัน Node/Python/Go ที่ไม่ตรงกันใน repo, ตรวจ data leakage ในโค้ด ML และสร้าง eval set สำหรับทดสอบ LLM ก่อนเปลี่ยน prompt หรือโมเดล

สิ่งที่ผมไม่คาดคิด: eval จับบั๊กที่ลองพิมพ์ prompt ดูเองไม่มีทางเจอ เช่น skill ตัวหนึ่งนับปัญหาเดิมซ้ำสองครั้ง รายงานว่าเจอ 5 ทั้งที่มี 4 อีกตัวลบเลขบัตรออกจาก log ถูกต้อง แต่ไม่เคยบอกในรายงานว่าลบไปแล้ว ทั้งสองเรื่องแก้ที่ตัว skill ไม่ได้แก้โดยทำให้เทสต์หลวมลง

ทุก skill ยังถูกทดสอบด้วย prompt ที่ต้อง "ไม่" เรียกมันขึ้นมาด้วย

MIT license ทดสอบกับ Claude Code แล้ว ส่วน agent อื่นติดตั้งผ่าน npx skills ได้ แต่ยังไม่ได้ทดสอบ

https://github.com/thanatchon36/skills

ถ้าลองแล้วเจอ skill ทำงานผิดจังหวะ บอกผมได้เลยครับ

#ClaudeCode #OpenSource #AIAgents
```

## Why it's written this way

- The first two lines state the problem, because that's all LinkedIn shows before "see more".
- The "what surprised me" paragraph is true: both bugs are recorded in `docs/evals.md`. Replace
  it with your own story if you have one.
- Three hashtags. More reads as spam.
- No numbers that aren't in the repo (no stars, users, or speed claims).

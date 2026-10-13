# thanatchon-skills

ชุด agent skills ที่พาโปรเจกต์ open source จาก MISSION.md หน้าเดียว ไปจนเป็น repo สาธารณะที่ใช้งานได้จริง

> ผลงานอีกชิ้นของผม: [verdrift](https://github.com/thanatchon36/verdrift) หาทุกจุดใน repo ที่ระบุเวอร์ชัน
> Node, Python หรือ Go แล้วบอกว่าตรงไหนไม่ตรงกัน

[English](./README.md) | ภาษาไทย

## ติดตั้ง

Claude Code:

```text
/plugin marketplace add thanatchon36/skills
/plugin install thanatchon-skills@thanatchon
```

agent อื่น ๆ ที่ [skills.sh](https://skills.sh) รองรับ เช่น Cursor, Codex (วิธีนี้จะ copy ไฟล์ skill มาไว้ในโปรเจกต์ให้แก้เองได้):

```sh
npx skills@latest add thanatchon36/skills
```

เลือกติดตั้งทางใดทางหนึ่งพอนะครับ ถ้าติดตั้งทั้งสองทาง skill จะขึ้นซ้ำกัน ทั้งสองคำสั่งด้านบนทดสอบติดตั้งจาก GitHub
แล้วเมื่อ 2026-10-13 (Claude Code 2.1.296, skills 1.7.2) ได้ skill ครบ 8 ตัวเหมือนกัน

## หน้าตาเวลาใช้งาน

`/ship-oss MISSION.md` จะสร้างโปรเจกต์และเขียน docs ตาม brief แล้วหยุดก่อนทำอะไรที่เป็นสาธารณะ
ตัวอย่างด้านล่างตัดมาจากข้อความสุดท้ายของการรันจริงกับ [brief เล็ก ๆ](./fixtures/ship-oss/tiny-mission/MISSION.md)
([ข้อความเต็ม](./docs/examples/ship-oss-stop-gate.md)):

```text
STOP GATE A: create the public repo example-dev/mdcount, push main, tag v0.1.0

Repo:        example-dev/mdcount
Visibility:  public
Description: Count words in Markdown files, skipping fenced code blocks and YAML front matter.
...
Secrets scan (every file to be pushed): "no obvious secrets"

Commands that will run on "go" (after the three local commits above):
  gh repo create example-dev/mdcount --public --source . --remote origin \
    --description "Count words in Markdown files, skipping fenced code blocks and YAML front matter."
  git push -u origin main
  git tag -a v0.1.0 -m "mdcount 0.1.0"
  git push origin v0.1.0

Reply "go" to run exactly these, or tell me what to change.
```

ไม่แน่ใจว่าควรเริ่มจากตัวไหน? ลองพิมพ์ `/thanatchon-skills:ask-thanatchon` ใน Claude Code แล้วเล่าว่ากำลังทำอะไรอยู่

## ทำไมต้องมี

ทุกวันนี้ coding agent เขียนโค้ดได้ดีแล้ว แต่การปล่อยโปรเจกต์ open source ยังมีงานอีกครึ่งหนึ่ง
ทั้งกำหนด scope, เขียน README ที่คนไม่รู้จักเราอ่านแล้วลองใช้ได้ทันที, เลือก license, ออก release
และประกาศเปิดตัว งานพวกนี้แหละที่ agent ชอบข้าม ชอบแต่งตัวเลขหรือ output ขึ้นมาเอง
และบางทีก็เผลอ push ขึ้น public ก่อนที่เราจะได้ตรวจ

skills ชุดนี้ช่วยงานครึ่งหลังนั้น แต่ละตัวเล็ก บอกชัดว่าไม่ควรใช้ตอนไหน และตัวที่อาจทำอะไรเป็นสาธารณะได้จะหยุดรอให้เราสั่ง "go" ก่อนทุกครั้ง

## มีอะไรบ้าง

### เส้นทางหลัก: จากไอเดียถึง repo ที่ปล่อยแล้ว

เรียกใช้เองเท่านั้น (agent จะไม่เรียกเองอัตโนมัติ)

| ปัญหาที่เจอ | Skill | ทำอะไร |
| --- | --- | --- |
| agent ลงมือเขียนโค้ดก่อนจะตกลงกันว่า "เสร็จ" หน้าตาเป็นยังไง | [`/mission-brief`](./skills/workflow/mission-brief/SKILL.md) | ถามทีละข้อพร้อมคำตอบที่แนะนำ แล้วเขียน `MISSION.md` ที่มี success criteria ตรวจสอบได้ มี phase และ stop gate |
| งานยาว ๆ เริ่มหลุด ข้ามการตรวจ หรือ push ก่อนเราจะได้ดู | [`/ship-oss`](./skills/workflow/ship-oss/SKILL.md) | ทำตาม brief ทีละ phase แต่ละ phase ต้องผ่านการตรวจที่รันจริง และจะหยุดรอ "go" ก่อนสร้าง repo, push, tag, release, publish หรือแตะ repo อื่น |
| โพสต์เปิดตัวที่อวยเกินจริง หรือ copy ข้อความเดียวไปแปะทุกที่ | [`/launch-kit`](./skills/workflow/launch-kit/SKILL.md) | ร่างโพสต์ Show HN, X thread, LinkedIn, Reddit, กลุ่มนักพัฒนาไทย, GitHub topics และ brief รูป social preview ไว้ใน `launch/` ตรวจว่าทุก claim มีหลักฐานใน repo และไม่โพสต์ให้เอง |

### Skill ที่ใช้ได้เดี่ยว ๆ

agent จะเรียกใช้เองเมื่องานตรงกับ skill หรือจะสั่งชื่อตรง ๆ ก็ได้

| ปัญหาที่เจอ | Skill | ทำอะไร |
| --- | --- | --- |
| คนกด star แต่ไม่มีใครลองใช้จริง | [`readme-that-converts`](./skills/workflow/readme-that-converts/SKILL.md) | เขียนหรือรีวิว README ให้ประโยคแรกบอกปัญหา คำสั่งติดตั้งอยู่หน้าแรก มี output จริงจากการรันจริง และบอกข้อจำกัด พร้อม lint script |
| `.nvmrc` บอก 22, Dockerfile ใช้ 20, CI ยังเทสต์ 18 | [`runtime-drift`](./skills/engineering/runtime-drift/SKILL.md) | รัน [verdrift](https://github.com/thanatchon36/verdrift) (ล็อกเวอร์ชัน v0.1.0 และบอกก่อนรันทุกครั้ง) แล้วเสนอการแก้ที่น้อยที่สุด ถ้าไม่มี Node 22 หรือไม่มีเน็ต จะตรวจเองตาม checklist แทน |
| โมเดลได้ 0.99 ตอน offline แต่พังบน production | [`leakage-audit`](./skills/data-ml/leakage-audit/SKILL.md) | ตรวจโค้ด pandas, scikit-learn, PySpark หา target leakage, temporal leakage, train/test ปนกัน และ preprocessing ที่ fit กับข้อมูลทั้งชุด ทุก finding มี `file:line` |
| กำลังจะเปลี่ยนโมเดลหรือแก้ prompt แต่ทดสอบแค่ลองพิมพ์ไม่กี่ข้อ | [`eval-harness`](./skills/data-ml/eval-harness/SKILL.md) | สร้าง eval set แบบ JSONL จาก input จริงและเคสที่เคยพัง ตรวจว่า grader สอบตกได้จริง รัน baseline (หลังเราอนุญาตให้เรียก API) แล้วเทียบผลทีละ case พร้อมบอกว่า case ไหนเปลี่ยนจากผ่านเป็นตกหรือกลับกัน และค่า sign test |
| จำไม่ได้ว่าควรใช้ตัวไหน | [`/ask-thanatchon`](./skills/meta/ask-thanatchon/SKILL.md) | ช่วยเลือก skill ที่เหมาะ และบอกตรง ๆ ถ้างานนั้นไม่ต้องใช้ skill เลย |

## ตัวอย่าง: `runtime-drift` กับ repo ที่เวอร์ชันไม่ตรงกัน

สั่งให้ตรวจ [`fixtures/runtime-drift/drifted`](./fixtures/runtime-drift/drifted) skill จะรัน verdrift และได้ 4 ปัญหานี้:

```text
✗ .github/workflows/ci.yml:24  python 3.10 (setup-python python-version) is a YAML number, so the action receives "3.1". Quote it: '3.10'  yaml-number
✗ .github/workflows/ci.yml:8   node 18 (setup-node matrix.node) is outside ">=20" (package.json:5 engines.node)  outside-range
✗ Dockerfile:1                 FROM node:20-alpine disagrees with 22 (.nvmrc:1)  pin-mismatch
✗ api/Dockerfile:1             FROM python:3.10-slim is outside ">=3.11" (api/pyproject.toml:4 requires-python)  outside-range
```

จากนั้นจะเสนอวิธีแก้ทีละปัญหาพร้อมเหตุผล และจะไม่แตะไฟล์ถ้าเราไม่ได้สั่งให้แก้

## ทดสอบยังไง

ทุก skill มี prompt ที่ควรเรียก skill อย่างน้อย 3 ข้อ และ prompt ที่ใกล้เคียงแต่ต้องไม่เรียกอีกอย่างน้อย 3 ข้อ
รันด้วย [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals) และถ้าผลลัพธ์ตรวจได้ ก็ตรวจผลลัพธ์ด้วย เช่น
`leakage-audit` ต้องเจอ leak ทั้ง 8 จุดที่ฝังไว้ใน [`fixtures/leakage/leaky`](./fixtures/leakage/EXPECTED.md) ถูกบรรทัด
และต้องรายงาน 0 finding กับเวอร์ชันที่แก้แล้ว ผลล่าสุดอยู่ที่ [`docs/evals.md`](./docs/evals.md)

## สร้างด้วย skills ชุดนี้

- **verdrift** ทำตาม workflow นี้จาก brief จนปล่อยได้: เริ่มจาก slice บาง ๆ ที่ทำงานครบตั้งแต่ต้นจนจบก่อน
  ([`0a6f535`](https://github.com/thanatchon36/verdrift/commit/0a6f535)) แล้วค่อยเพิ่มเทสต์ กฎ docs และ CI
  ([commit history](https://github.com/thanatchon36/verdrift/commits/main)), [CI ผ่าน](https://github.com/thanatchon36/verdrift/actions/runs/38226583610)
  และ [release v0.1.0](https://github.com/thanatchon36/verdrift/releases/tag/v0.1.0) (brief ของ verdrift ไม่ได้เปิดเผย)
- **repo นี้** เป็นตัวอย่างที่สอง และเปิด brief ให้อ่านได้ที่ [`docs/mission/MISSION.md`](./docs/mission/MISSION.md)

## ข้อจำกัด

- ทดสอบกับ Claude Code เท่านั้น ติดตั้งลง agent อื่นผ่าน `npx skills` ได้ แต่ยังไม่ได้ทดสอบ
- `runtime-drift` รองรับแค่ Node, Python และ Go ตาม scope ของ verdrift และต้องมี Node 22 ขึ้นไปพร้อมเน็ต
- `leakage-audit` อ่านโค้ดแบบ static มองไม่เห็น leak ใน SQL, feature store หรือ notebook ที่ไม่ได้ให้มันอ่าน และจะบอกตรง ๆ แทนที่จะสรุปว่าปลอดภัย
- `eval-harness` เขียน runner ครอบโค้ดของเราเอง และจะถามก่อนใช้โควตา API ถ้าไม่มี credentials จะหยุดก่อนรัน baseline และบอกตรง ๆ ส่วน sign test ใช้กับผลแบบผ่าน/ตกเท่านั้น ใช้กับคะแนนไม่ได้
- คะแนน eval มาจากการรันจำนวนไม่มาก ผลอาจต่างกันในแต่ละรอบ

## แผนต่อไป

skill ที่ยังร่างอยู่ใน [`skills/in-progress/`](./skills/in-progress/) (ยังไม่ปล่อย): `rag-triage`, `backtest-honesty`, `model-card`

## ร่วมพัฒนา

ที่ช่วยได้มากที่สุดคือส่ง prompt ที่ skill ทำงานผิดจังหวะมาให้ ทั้งกรณีที่เรียกทั้งที่ไม่ควร และกรณีที่ควรเรียกแต่ไม่เรียก ดูรายละเอียดที่ [CONTRIBUTING.md](./CONTRIBUTING.md)

## ผลงานอื่น

- [verdrift](https://github.com/thanatchon36/verdrift): หาทุกจุดใน repo ที่ระบุเวอร์ชัน Node, Python หรือ Go แล้วบอกว่าตรงไหนไม่ตรงกัน
- [gemini-candlestick](https://github.com/thanatchon36/gemini-candlestick): โปรเจกต์ประกวด Gemini API จำลองบอร์ดลงทุนที่ถกกันเรื่องกราฟแท่งเทียนและ indicator
- [nvidia-gpu-operator-k8s-cluster](https://github.com/thanatchon36/nvidia-gpu-operator-k8s-cluster): คู่มือติดตั้ง NVIDIA GPU Operator บน Kubernetes cluster บน AWS ทีละขั้น

## License

[MIT](./LICENSE)

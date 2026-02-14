# AI Grader

Grading can be time-consuming, and evaluation outcomes may sometimes be influenced by factors such as mood, fatigue, or implicit bias.

To help address this, I built an **AI Grader** that provides consistent, rubric-based evaluations. It also allows students to evaluate their work against a rubric before submission, helping them improve their assignments in advance.

---

## Demo

🔗 https://ai-grader-180.onrender.com/

**Notes:**
- You can try it using the examples in the `examples` folder.
- The app may take up to a minute to load (cold start).

![AI Grader](https://github.com/user-attachments/assets/3499bf14-c0ff-4f92-818b-b29e3693ddeb)

---

## Features

The AI Grader:

- Accepts a **rubric file** (bullet-point or table format)
- Accepts an **assignment file**
- Returns:
  - A detailed score breakdown
  - Rubric backed score explainations
  - Suggestions for improvement

---

## Built With

- Python  
- FastAPI  
- Groq API  
- HTML  
- Bootstrap 5  
- JavaScript  

---

## Why This Project?

Most existing AI grading tools are either paid services or provide generic feedback without strictly following a teacher’s rubric. In schools, teachers rely on detailed rubrics to ensure assignments are graded fairly and consistently across specific criteria.

This AI Grader addresses that gap by grading assignments directly against a provided rubric. It generates a clear breakdown of scores by category and offers targeted suggestions for improvement—closely mimicking how a teacher evaluates student work.

This project explores how AI can support educators by reducing grading workload while increasing consistency and transparency. At the same time, it helps students better understand grading criteria and improve their work before submission.

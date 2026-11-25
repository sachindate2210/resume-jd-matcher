# 🎯 Resume vs Job Description Matcher

Upload a resume and paste a job description. An LLM acting as a recruiter returns a **match score, matched and missing skills, tailored resume edits and likely interview questions**, alongside a model-free keyword-overlap baseline.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

## Features
- **Structured output:** the model returns strict JSON (`response_format=json_object`), rendered as score cards
- **Skill-gap analysis:** what the JD asks for that the resume does / doesn't show
- **Actionable suggestions:** specific bullets to add or reword for *this* job
- **Interview prep:** 3 likely questions based on the resume + JD
- **Baseline check:** simple keyword-overlap % next to the AI score, so you can sanity-check the model
- Reads **PDF** or text resumes

## Run it
```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # add your free Groq API key
streamlit run app.py
```
CLI: `python matcher.py path/to/resume.pdf path/to/jd.txt` (defaults to the files in `samples/`).

## Project structure
```
matcher.py      prompt, JSON analysis, keyword-overlap baseline
app.py          Streamlit UI with score cards
samples/        sample resume and job description
```

---
Built by **[Sunil Date](https://github.com/sachindate2210)**

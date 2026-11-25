"""Streamlit UI for the Resume vs Job Description matcher."""
import tempfile
from pathlib import Path

import streamlit as st

from matcher import analyze, read_resume

st.set_page_config(page_title="Resume–JD Matcher", page_icon="🎯", layout="wide")
st.title("🎯 Resume vs Job Description Matcher")
st.caption("Upload your resume, paste a job description, and get a match score, skill gaps and tailored resume suggestions.")

left, right = st.columns(2)
with left:
    upload = st.file_uploader("Resume (PDF or TXT)", type=["pdf", "txt"])
    use_sample = st.checkbox("Use sample resume", value=upload is None)
with right:
    sample_jd = Path("samples/jd_genai_engineer.txt").read_text(encoding="utf-8")
    jd = st.text_area("Job description", value=sample_jd, height=260)

if st.button("Analyze match", type="primary"):
    if upload:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(upload.name).suffix) as tmp:
            tmp.write(upload.getvalue())
        resume = read_resume(tmp.name)
    elif use_sample:
        resume = read_resume("samples/resume.txt")
    else:
        st.warning("Upload a resume or tick 'Use sample resume'.")
        st.stop()

    with st.spinner("Comparing resume with the job description..."):
        r = analyze(resume, jd)

    st.subheader(r.get("role", "Result"))
    c1, c2, c3 = st.columns(3)
    c1.metric("AI match score", f"{r.get('score', 0)}/100")
    c2.metric("Keyword overlap", f"{r.get('keyword_overlap', 0)}%")
    c3.metric("Verdict", r.get("verdict", "-"))
    st.progress(min(int(r.get("score", 0)), 100) / 100)
    st.info(r.get("experience_fit", ""))

    a, b = st.columns(2)
    with a:
        st.markdown("#### ✅ Matched skills")
        st.markdown(" ".join(f"`{s}`" for s in r.get("matched_skills", [])) or "-")
        st.markdown("#### 💪 Strengths")
        for s in r.get("strengths", []):
            st.markdown(f"- {s}")
    with b:
        st.markdown("#### ❌ Missing skills")
        st.markdown(" ".join(f"`{s}`" for s in r.get("missing_skills", [])) or "None 🎉")
        st.markdown("#### ✏️ Resume suggestions")
        for s in r.get("suggestions", []):
            st.markdown(f"- {s}")

    st.markdown("#### 🎤 Likely interview questions")
    for i, q in enumerate(r.get("interview_questions", []), 1):
        st.markdown(f"{i}. {q}")

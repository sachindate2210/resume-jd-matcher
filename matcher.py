"""Compare a resume with a job description: match score, skill gaps and concrete resume suggestions."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

PROMPT = """You are an experienced technical recruiter and ATS expert.
Compare the RESUME with the JOB DESCRIPTION and return ONLY a JSON object with this shape:
{
  "role": "job title from the JD",
  "score": 0-100 integer, how well the resume fits the JD,
  "verdict": "Strong match" | "Good match" | "Partial match" | "Weak match",
  "matched_skills": ["skills/tools required by the JD that the resume clearly shows"],
  "missing_skills": ["skills/tools required by the JD that the resume does not show"],
  "experience_fit": "one sentence on years/seniority fit",
  "strengths": ["2-4 short points"],
  "suggestions": ["3-5 specific edits to the resume for THIS job, e.g. which bullet to add or reword"],
  "interview_questions": ["3 likely interview questions for this candidate and job"]
}
Rules: judge only from the text given, never invent experience the resume doesn't show.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}"""


def read_resume(path: str | Path) -> str:
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        return "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def keyword_overlap(resume: str, jd: str) -> float:
    """Cheap, model-free baseline: share of JD keywords (tech-looking words) present in the resume."""
    words = lambda t: set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]{1,}", t.lower()))
    stop = {"and", "the", "with", "for", "you", "our", "are", "will", "have", "years", "experience",
            "work", "team", "skills", "strong", "ability", "good", "knowledge", "role", "using", "who"}
    jd_terms = {w for w in words(jd) if w not in stop and len(w) > 2}
    if not jd_terms:
        return 0.0
    return round(100 * len(jd_terms & words(resume)) / len(jd_terms), 1)


def analyze(resume: str, jd: str) -> dict:
    client = Groq()
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": PROMPT.replace("{resume}", resume[:12000]).replace("{jd}", jd[:6000])}],
    )
    result = json.loads(resp.choices[0].message.content)
    result["keyword_overlap"] = keyword_overlap(resume, jd)
    return result


if __name__ == "__main__":
    import sys

    resume_path = sys.argv[1] if len(sys.argv) > 1 else "samples/resume.txt"
    jd_path = sys.argv[2] if len(sys.argv) > 2 else "samples/jd_genai_engineer.txt"
    out = analyze(read_resume(resume_path), Path(jd_path).read_text(encoding="utf-8"))
    print(json.dumps(out, indent=2))

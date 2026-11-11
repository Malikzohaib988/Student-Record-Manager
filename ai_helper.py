"""
ai_helper.py
All Groq AI related functions for AI Student Record Manager.
API key is loaded from .env file — never hardcoded.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ─── API Key ─────────────────────────────────────────────────────────────────

def get_api_key() -> str:
    """Read Groq API key from environment variable."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "GROQ_API_KEY not found. Please add it to your .env file.\n"
            "Example:  GROQ_API_KEY=your_actual_api_key_here"
        )
    return key


# ─── Model Selection ─────────────────────────────────────────────────────────

def choose_model(client) -> str:
    """
    Return model name from .env or auto-select the first available
    text-generation model from the user's Groq account.
    """
    model_from_env = os.getenv("GROQ_MODEL", "").strip()
    if model_from_env:
        return model_from_env

    # Auto-select: try common free/available models in order
    preferred = [
        "llama3-8b-8192",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it",
        "gemma2-9b-it",
    ]
    try:
        available = [m.id for m in client.models.list().data]
        for model in preferred:
            if model in available:
                return model
        # Fall back to first available model
        if available:
            return available[0]
    except Exception:
        pass

    # Last resort default
    return "llama3-8b-8192"


# ─── Core AI call ─────────────────────────────────────────────────────────────

def ask_ai(prompt: str) -> str:
    """
    Send a prompt to Groq API and return the text response.
    Raises exceptions with clear messages on failure.
    """
    try:
        from groq import Groq
    except ImportError:
        raise ImportError(
            "Groq library is not installed. Run:  pip install groq"
        )

    api_key = get_api_key()

    try:
        client = Groq(api_key=api_key)
        model = choose_model(client)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful academic advisor for school teachers. "
                        "Provide concise, practical, and encouraging feedback. "
                        "Use simple language suitable for students. "
                        "Format your response with clear sections and bullet points. "
                        "Keep responses brief and to the point."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        error_msg = str(e).lower()
        if "api_key" in error_msg or "authentication" in error_msg or "auth" in error_msg:
            raise Exception(
                "Invalid Groq API key. Please check your .env file and make sure "
                "GROQ_API_KEY is correct."
            )
        elif "rate" in error_msg or "limit" in error_msg or "429" in error_msg or "tokens" in error_msg:
            raise Exception(
                "Groq API rate limit reached. Please wait a moment and try again."
            )
        elif "model" in error_msg or "not found" in error_msg or "404" in error_msg:
            raise Exception(
                "The selected AI model is not available. Try updating GROQ_MODEL "
                "in your .env file or remove it to auto-select."
            )
        elif "connection" in error_msg or "network" in error_msg or "timeout" in error_msg:
            raise Exception(
                "Could not connect to Groq API. Please check your internet connection."
            )
        else:
            raise Exception(f"Groq API error: {str(e)}")


# ─── Student description (privacy-safe) ──────────────────────────────────────

def describe_student(student: dict) -> str:
    """
    Build a privacy-safe text description of a student.
    Does NOT include student name or ID.
    """
    marks = student.get("marks", {})
    subjects_text = "\n".join(
        f"  - {subject}: {mark}/100"
        for subject, mark in marks.items()
    )
    return (
        f"Class/Semester: {student.get('class', 'N/A')}\n"
        f"Subjects and Marks:\n{subjects_text}\n"
        f"Total Marks: {student.get('total', 0)}\n"
        f"Average Percentage: {student.get('average', 0)}%\n"
        f"Overall Grade: {student.get('grade', 'N/A')}"
    )


# ─── Feature 1: Analyze Performance ──────────────────────────────────────────

def analyze_performance(student: dict) -> str:
    """
    Analyze a student's academic performance using Groq AI.
    Returns a detailed performance analysis.
    """
    description = describe_student(student)

    prompt = f"""
A teacher wants you to analyze this student's academic performance.

Student Academic Data:
{description}

Please provide:
1. **Performance Summary** - A brief overall assessment
2. **Strong Subjects** - Subjects where the student performed well (above 75%)
3. **Weak Subjects** - Subjects that need improvement (below 60%)
4. **Subject-wise Analysis** - Short comment on each subject
5. **Improvement Suggestions** - 3-4 practical tips to improve academic performance

Keep the response encouraging, concise, and actionable.
"""
    return ask_ai(prompt)


# ─── Feature 2: Generate Study Tips ──────────────────────────────────────────

def generate_study_tips(student: dict) -> str:
    """
    Generate a personalized weekly study plan and tips using Groq AI.
    Returns actionable study recommendations.
    """
    description = describe_student(student)

    prompt = f"""
A teacher wants personalized study tips for a student based on their academic performance.

Student Academic Data:
{description}

Please provide:
1. **Weekly Study Plan** - A simple day-by-day schedule (Monday to Sunday)
2. **Focus Areas** - Which subjects need extra attention and why
3. **Daily Study Tips** - 4-5 practical daily habits for better learning
4. **Learning Strategies** - Specific techniques for improving weak subjects
5. **Motivational Message** - A short encouraging note to keep the student motivated

Make it practical, specific to the marks shown, and easy to follow.
"""
    return ask_ai(prompt)

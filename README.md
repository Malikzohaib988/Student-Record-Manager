# AI Student Record Manager

A beginner-friendly web application for teachers to manage student academic records and get AI-powered performance analysis using the Groq API.

---

## Features

- **Add / Update / Delete** student records
- **Automatic grade calculation** (Total, Average %, Grade A–F)
- **Search** students by name or ID
- **AI Performance Analysis** — subject-wise feedback via Groq API
- **AI Study Tips** — personalized weekly study plan via Groq API
- **JSON-based storage** — data persists between sessions
- Clean **green & white** responsive interface

---

## Technologies Used

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3, Flask                   |
| AI       | Groq API (via groq SDK)           |
| Storage  | JSON file (students.json)         |
| Frontend | HTML5, CSS3, JavaScript, Fetch API|
| Config   | python-dotenv (.env file)         |

---

## Project Folder Structure

```
AI_Student_Record_Manager_Web/
│
├── app.py               # Flask backend — all routes
├── ai_helper.py         # Groq AI integration
├── students.json        # Student records (auto-created)
├── requirements.txt     # Python dependencies
├── .env                 # Your API key (DO NOT share)
├── .env.example         # Template for .env
├── .gitignore           # Excludes .env and venv from git
│
├── templates/
│   └── index.html       # Full frontend (HTML + CSS + JS)
│
└── README.md            # This file
```

---

## Setup Instructions

### Step 1 — Make sure Python is installed

Open a terminal and run:

```
python --version
```

You should see Python 3.8 or higher. If not, download it from https://python.org

---

### Step 2 — Open the project folder

```
cd path\to\AI_Student_Record_Manager_Web
```

---

### Step 3 — Create a virtual environment

```
python -m venv venv
```

---

### Step 4 — Activate the virtual environment

**Windows:**
```
venv\Scripts\activate
```

**Mac / Linux:**
```
source venv/bin/activate
```

You will see `(venv)` appear at the start of your terminal line.

---

### Step 5 — Install dependencies

```
python -m pip install -r requirements.txt
```

---

### Step 6 — Get your Groq API Key

1. Go to https://console.groq.com
2. Sign up for a free account
3. Click **API Keys** → **Create API Key**
4. Copy the key

---

### Step 7 — Configure your API key

Open the `.env` file in the project folder and replace the placeholder:

```
GROQ_API_KEY=your_actual_api_key_here
```

Save the file.

> **Important:** Never share your `.env` file or upload it to GitHub.

---

### Step 8 — Run the application

```
python app.py
```

The app will start and automatically open in your browser at:

```
http://127.0.0.1:5000
```

Keep the terminal open while using the app. Press `Ctrl + C` to stop.

---

## How to Use

### Adding a Student
1. Fill in Student ID, Name, Class/Semester
2. Enter subjects separated by commas — e.g. `Python, Math, English`
3. Enter matching marks — e.g. `88, 76, 92`
4. Click **Add**

### Updating a Student
1. Click on a student row in the table to select them
2. Edit the fields in the form (ID cannot change)
3. Click **Update**

### Deleting a Student
1. Click on a student row to select them
2. Click **Delete**
3. Confirm in the popup dialog

### Searching Students
- Type a name or ID in the search box — results filter live
- Click **Show All** to reset the view

### AI Performance Analysis
1. Click on a student row to select them
2. Click **Analyze Performance**
3. Wait for the AI response (requires internet + valid API key)

### AI Study Tips
1. Click on a student row to select them
2. Click **Generate Study Tips**
3. The AI will generate a personalized weekly study plan

---

## Grading Criteria

| Grade | Percentage     |
|-------|----------------|
| A     | 85% and above  |
| B     | 70% – 84%      |
| C     | 60% – 69%      |
| D     | 50% – 59%      |
| F     | Below 50%      |

---

## Common Errors and Solutions

| Error | Solution |
|-------|----------|
| `GROQ_API_KEY not found` | Open `.env` and add your API key |
| `Invalid Groq API key` | Double-check the key at console.groq.com |
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `Address already in use` | Another app is using port 5000 — close it or restart |
| `Student ID already exists` | Use a different unique ID |
| `Number of subjects must match marks` | Count commas — subjects and marks must be equal |
| AI response not loading | Check your internet connection and API key |
| `Rate limit reached` | Wait 30 seconds and try again |

---

## Privacy Note

The AI features only send the following to the Groq API:
- Class / Semester
- Subject names and marks
- Total, average, grade

Student names and IDs are **never sent** to the AI.

---

## Requirements

```
flask==3.0.3
groq==0.9.0
python-dotenv==1.0.1
```

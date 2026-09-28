from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_quiz_key"

# Load questions from JSON
def load_questions():
    path = os.path.join("data", "questions.json")
    with open(path, "r") as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["subject"] = request.form.get("subject")
        session["score"] = 0
        session["current_index"] = 0
        session["streak"] = 0
        session["difficulty"] = "easy"
        return redirect(url_for("quiz"))
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions_data = load_questions()
    subject = session.get("subject", "python")
    questions = questions_data.get(subject, [])
    
    current_index = session.get("current_index", 0)
    
    # Check if quiz is finished
    if current_index >= len(questions):
        return redirect(url_for("result"))
    
    current_q = questions[current_index]

    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct_answer = current_q["answer"]
        
        # Scoring & Adaptive Logic
        if user_answer == correct_answer:
            session["score"] += 10 if current_q["difficulty"] == "easy" else 20
            session["streak"] += 1
            # Adaptive pathway: Increase difficulty if streak >= 2
            if session["streak"] >= 2:
                session["difficulty"] = "medium"
        else:
            session["streak"] = 0
            
        session["current_index"] += 1
        return redirect(url_for("quiz"))

    return render_template("quiz.html", question=current_q, index=current_index + 1)

@app.route("/result")
def result():
    score = session.get("score", 0)
    return render_template("result.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)
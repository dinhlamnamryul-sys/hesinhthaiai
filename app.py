from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

demo_quiz = [
    {"id":1,"question":"1+1=?","options":["A.1","B.2","C.3","D.4"],"answer":"B"},
    {"id":2,"question":"2*3=?","options":["A.5","B.6","C.7","D.8"],"answer":"B"},
    {"id":3,"question":"5>3 đúng hay sai?","options":["A.Đúng","B.Sai"],"answer":"A"}
]

@app.route("/")
def index():
    return render_template("arena.html")

@app.route("/generate", methods=["POST"])
def generate():
    return jsonify({"quiz": demo_quiz})

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    answers = data.get("answers")
    quiz = data.get("quiz")
    score = sum(1 for q in quiz if answers.get(str(q["id"]))==q["answer"])
    return jsonify({"score":score,"total":len(quiz)})

if __name__=="__main__":
    app.run(debug=True)

# app.py

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from rag import ask_question

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    question = data["question"]

    result = ask_question(question)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)


# python app.py
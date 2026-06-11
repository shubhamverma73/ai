# app.py

from flask import (
    Flask,
    render_template,
    request,
    Response,
    jsonify
)

from tools.rag_tool import (
    stream_answer
)
from agent import stream_agent_answer

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    question = data["question"]

    return Response(
        stream_agent_answer(question),
        mimetype="text/plain"
    )


@app.route("/sources")
def sources():

    return jsonify(
        getattr(
            stream_answer,
            "last_sources",
            []
        )
    )


if __name__ == "__main__":

    app.run(
        debug=False,
        use_reloader=False,
        threaded=True
    )


# python app.py
# app.py

from flask import (
    Flask,
    render_template,
    request,
    Response,
    jsonify
)

from rag import stream_answer

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    question = data["question"]

    return Response(
        stream_answer(question),
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
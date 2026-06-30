from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS

from lib.validation import validate_question
from lib.rag_service import ask_question

app = Flask(__name__)

CORS(app)


@app.route("/api/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if data is None:
        return jsonify(
            {
                "error": "Request body is required."
            }
        ), 400

    question, error = validate_question(
        data.get("question")
    )

    if error:

        return jsonify(
            {
                "error": error
            }
        ), 400

    response = ask_question(question)

    return jsonify(response)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
    )
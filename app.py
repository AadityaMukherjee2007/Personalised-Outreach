from flask import Flask, jsonify, render_template, request
import personalise

app = Flask(__name__)
personalise.init()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/get_email_content", methods=["POST"])
def get_email_content():
    if request.method == "POST":
        data = request.get_json()
        url = data.get("url") if data else None
        email_content=""

        if url:
            print(url)
            email_content = personalise.generate_email(url)
            print(email_content)

    return jsonify({
        "email_content": email_content,
    })

if __name__ == "__main__":
    app.run(debug=True)
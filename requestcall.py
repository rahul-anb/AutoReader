from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def sessions():
    return render_template('session.html')

@app.route("/get-user/")
def home():
    return "Home"


if __name__ == "__main__":
    app.run(debug=True)
    
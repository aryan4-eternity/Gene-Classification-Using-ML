from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API = "http://127.0.0.1:8000/predict"   # your FastAPI endpoint

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    seqs = request.form["sequences"].strip().splitlines()
    r = requests.post(API, json={"sequences": seqs})
    r.raise_for_status()
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(port=5500, debug=True)   # Flask on 5500, FastAPI stays on 8000

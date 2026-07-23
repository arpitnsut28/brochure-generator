from flask import Flask, render_template, request, jsonify
from brochure_logic import create_brochure  # your existing function

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    company_name = data.get("company_name")
    url = data.get("url")
    brochure_markdown = create_brochure(company_name, url)  # returns markdown text
    return jsonify({"brochure": brochure_markdown})

if __name__ == "__main__":
    app.run(debug=True)
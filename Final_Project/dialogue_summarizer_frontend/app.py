from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/pratiknichite/TrainedTextSummerizerBART"
headers = {"Authorization": "Bearer " + os.environ["API_KEY"]}


def query(payload):
    try:
        response = request.post(API_URL, headers=headers, json=payload, timeout = 300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return e

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output_length = 100

    if request.method == "POST":
        data = request.form["text"]
        output_length = int(request.form["min_output_length"])

        #change query input
        result = query({"inputs": data, "parameters": {"min_length": output_length}})

        output = result[0]["summary_text"]

        return render_template('summarize.html', summary=output, input_text=data, min_l=output_length)
    else:
        return render_template('summarize.html', min_l=output_length)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# pipe = pipeline('summarization', model="t5-base")
# pipe = pipeline('summarization', model="./bart_trained_model") # importing local trained model
pipe = pipeline("summarization", model="pratiknichite/TrainedTextSummerizerBART") #our trained model

@app.route('/', methods=['GET', 'POST'])
def index():
    output_length = 100

    if request.method == "POST":
        data = request.form["text"]
        output_length = int(request.form["min_output_length"])

        processed_text = pipe(data, min_length=output_length)[0]['summary_text']
        # processed_text = pipe(data)[0]['summary_text']

        return render_template('summerize.html', summary=processed_text, input_text=data, min_l=output_length)
    else:
        return render_template('summerize.html', min_l=output_length)

if __name__ == '__main__':
    app.run(debug=True)
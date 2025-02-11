from flask import Flask, request, render_template
import comparisons

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def twin():
    text = request.form['text']
    processed_text = comparisons.getTwin(text)
    return processed_text

@app.route('/compareTwo')
def compareTwo():
    return "Me!"

def run():
    app.run(host="127.0.0.1", port=8080, debug=True)

if __name__ == "__main__":
    run()
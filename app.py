from flask import Flask, render_template

from translate.translate import Translate

app = Flask(__name__)


@app.route('/')
def start_page():
    return 'Ana are mere'


@app.route('/<int:count>')
def second_page(count):
    return render_template('index.html', no=range(count))


@app.route('/translate/<value>')
def translate(value):
    trs = Translate()
    response = trs.translate(value)
    print(response[0])
    return render_template('translate.html', result=response[0])



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

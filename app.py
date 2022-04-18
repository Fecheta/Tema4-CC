from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def start_page():
    return 'Ana are mere'


@app.route('/<int:count>')
def second_page(count):

    return render_template('index.html', no=range(count))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

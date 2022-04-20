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
    # def getconn():
    #     conn = connector.connect(
    #         "cc-tema3-345518:europe-north1:database",
    #         "pymysql",
    #         user="root",
    #         password="12345",
    #         db="tema3-db"
    #     )
    #     return conn
    #
    # pool = sqlalchemy.create_engine(
    #     "mysql+pymysql://",
    #     creator=getconn,
    # )
    #
    # result = translate_text('ro', value)
    # original = value
    # translated = result['translatedText']
    # fromLanguage = result['detectedSourceLanguage']
    # toLanguage = 'ro'
    #
    # # query or insert into Cloud SQL database
    # with pool.connect() as db_conn:
    #     # query database
    #     query_result = db_conn.execute(f"INSERT INTO translate (original, translated, from_lang, to_lang) VALUES (\"{original}\", \"{translated}\", \"{fromLanguage}\", \"{toLanguage}\")")
    #
    # return render_template('translate.html', result=result, db='Translation added to database')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

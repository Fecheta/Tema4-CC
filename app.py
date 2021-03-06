from flask import Flask, render_template, request, redirect

from FormRecognizer import FormRecognizer
from speech import text_to_speech
from storage import Storage
from computer_vision import ComputerVision
from TextAnalytics import TextAnalytics


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"


@app.route('/')
def start_page():
    return render_template('index.html')



@app.route('/textAnalytics')
def text_analytics():
    return render_template('textAnalytics.html')


@app.route('/textAnalytics/result', methods=['POST', 'GET'])
def text_analytics_results():
    output = request.form.to_dict()
    description = output["description"]
    print(description)
    results = TextAnalytics.reviews(description)
    print(results)
    return render_template('textAnalytics.html', description=results)


@app.route('/formRecognizer')
def form_recognizer():
    return render_template('form.html')


@app.route('/formRecognizer/result', methods=['POST', 'GET'])
def form_recognizer_results():
    output = request.form.to_dict()
    description = output["description"]
    print(description)
    results = FormRecognizer.get_information(description)
    print(results)
    return render_template('form.html', description=results)


@app.route('/<int:count>')
def second_page(count):
    return render_template('ana.html', no=range(count))


@app.route("/view-photos")
def view_photos():
    storage = Storage.storage()
    blob_items = storage.container_client.list_blobs()

    urls = []
    for blob in blob_items:
        blob_client = storage.container_client.get_blob_client(blob=blob.name)
        urls.append(blob_client.url)

    return render_template('photos.html', urls=urls)


@app.route("/upload-photos", methods=['GET', 'POST'])
def upload_photos():
    if request.method == 'POST':
        storage = Storage.storage()

        for file in request.files.getlist('photos'):
            try:
                storage.container_client.upload_blob(file.filename,
                                             file)
            except Exception as e:
                print('File already exist')

        return redirect('/view-photos')

    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/Hand-To-Text', methods=['GET', 'POST'])
def hand_to_text():
    if request.method == 'GET':
        return render_template('image_form.html')

    if request.method == 'POST':
        computer_vision = ComputerVision()

        file_to_analyze = request.files.getlist('photos')[0]
        print(file_to_analyze.filename)

        texts = computer_vision.identify_text_from_local_file_str(file_to_analyze)

        # storage = Storage.storage()
        # storage.container_client.upload_blob(file_to_analyze.filename, file_to_analyze)
        #
        # url = None
        # blob_items = storage.container_client.list_blobs()
        # for blob in blob_items:
        #     print(blob.name)
        #     if blob.name == file_to_analyze.filename:
        #         blob_client = storage.container_client.get_blob_client(blob=blob.name)
        #         url = blob_client.url
        #         break

        return render_template('image_text.html', image=file_to_analyze, texts=texts)



@app.route('/texttospeech',methods=("GET", "POST"))
def text_to_speech_page():
    form = text_to_speech.Widgets()
    if request.method == "GET":
        return render_template('speech.html', form=form)
    if request.method == "POST":
        text = request.form["text"]
        text_to_speech.text_to_speach(text)
        return render_template('speech.html', form=form)
    return render_template('speech.html', form=form)

@app.route('/search')
def search_page():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

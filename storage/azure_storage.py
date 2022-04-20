from flask import Flask, request, redirect, render_template
from storage import Storage

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

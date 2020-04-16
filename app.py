from flask import *
import shutil
import json
import os
from settings import *
from data import db_session
from data import files
from functions import *


app = Flask(__name__)
app.config.from_pyfile("settings.py")
db_session.global_init("db/files.sqlite")


@app.route('/', methods=["GET", "POST"])
def upload_page():
    if request.method == 'POST':
        files_list = request.files
        print(files_list)

        link = custom_link(6)
        obj = files.Files()
        obj.link = link
        s = db_session.create_session()
        s.add(obj)
        s.commit()

        path = os.path.join(app.config['UPLOAD_FOLDER'], link)
        os.mkdir(path)
        for index in files_list:
            file = request.files[index]
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], link, filename))

        url = request.url
        if request.url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        url += link
        return url

    return render_template("upload.html")


@app.route('/<download_url>')
def download_page(download_url):
    path = os.path.join(app.config['UPLOAD_FOLDER'], download_url)
    #path = os.path.join(path, os.listdir(path)[0])
    return render_template("download.html", download_url=download_url)


@app.route('/<download_url>/download/')
def download(download_url):
    path = os.path.join(app.config['UPLOAD_FOLDER'], download_url)
    print("download", path)
    if os.path.exists(path):
        shutil.make_archive(path, 'zip', path)
        return send_file(path + ".zip", attachment_filename='files.zip', as_attachment=True)



if __name__ == '__main__':
    app.run()

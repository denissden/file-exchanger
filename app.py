from flask import *
import atexit
import shutil
import time
import json
import os
from settings import *
from data import db_session
from data import files
from functions import *
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_pyfile("settings.py")
db_session.global_init("db/files.sqlite")

#schedule cleanup
scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup, trigger="interval", **CLEANUP_EVERY)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route('/', methods=["GET", "POST"])
def upload_page():
    if request.method == 'POST':
        files_list = request.files
        expiration_id = request.values.get("expire")
        print(files_list, expiration_id)

        link = custom_link(6)
        expires = get_expiration_time(expiration_id)

        obj = files.Files()
        obj.link = link
        obj.expiration_date = expires
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

        if os.path.exists(path):
            shutil.make_archive(os.path.join(ZIPS_FOLDER, link), 'zip', path)

        url = request.url
        if request.url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        url += link
        return url

    return render_template("upload.html")


@app.route('/<download_url>')
def download_page(download_url):
    path = os.path.join(app.config['UPLOAD_FOLDER'], download_url)
    if not os.path.exists(path):
        abort(404)

    files = []
    for file in os.listdir(path):
        file_data = dict()
        file_data["name"] = file
        p = os.path.join(path, file)
        file_data["size"] = readable_size(os.path.getsize(p))
        files.append(file_data)
        print(file_data)

    s = db_session.create_session()
    dates = s.execute(f'SELECT created_date, expiration_date FROM files WHERE (link == "{download_url}")').next()
    print(dates)
    return render_template("download.html",
                           download_url=download_url,
                           files=files,
                           **get_dates(download_url))



@app.route('/<download_url>/download/')
def download(download_url):
    path = os.path.join(app.config['UPLOAD_FOLDER'], download_url);
    if not os.path.exists(path):
        abort(404)

    list_dir = os.listdir(path)
    print(list_dir)
    if len(list_dir) == 1:
        name = list_dir[0]
        file = os.path.join(path, name)

        print("download", file)
        inc_downloads(download_url)

        return send_file(file, attachment_filename=name, as_attachment=True)
    else:
        zip_file = os.path.join(ZIPS_FOLDER, download_url) + ".zip"

        print("download", zip_file)
        inc_downloads(download_url)

        return send_file(zip_file, attachment_filename=f"{download_url}_all_files.zip", as_attachment=True)


@app.route('/<download_url>/download/<file_name>')
def download_file(download_url, file_name):
    file = os.path.join(app.config['UPLOAD_FOLDER'], download_url, file_name);
    print("download", file)
    if os.path.exists(file):
        inc_downloads(download_url)
        return send_file(file, attachment_filename=file_name, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
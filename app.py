# I pretty much followed this tutorial for this project:
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

from flask import Flask, render_template, request, flash, send_from_directory
from werkzeug.utils import redirect

import config as Config
from upload import uploadFile, getPictures

config = Config.Config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
    return render_template('homepage.html', data=getPictures())


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(config.UPLOAD_FOLDER, filename, as_attachment=False)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if 'author' not in request.form:
            flash('No selected author')
            return redirect(request.url)
        author = request.form['author']
        if 'title' not in request.form:
            flash('No selected title')
            return redirect(request.url)
        title = request.form['title']

        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(config.UPLOAD_FOLDER, filename))
            uploadFile(file, title, author)
            return redirect('/')
    return render_template('upload.html', title='Upload a File')


if __name__ == '__main__':
    app.run()

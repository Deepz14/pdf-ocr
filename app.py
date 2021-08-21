import os
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from module import extract
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['UPLOAD_FOLDER'] = './data_directory'
app.config['MAX_CONTENT_PATH'] = 9999999
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        if not os.path.isdir(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(file_path)
        extract_details(file_path)
        return render_template("success.html", name=f.filename)


# @app.route("/add")
# def add_book():
#     name = request.args.get('name')
#     author = request.args.get('author')
#     published = request.args.get('published')
#     try:
#         book = Pdf(
#             name=name,
#             author=author,
#             published=published
#         )
#         db.session.add(book)
#         db.session.commit()
#         return "Pdf added. book id={}".format(book.id)
#     except Exception as e:
#         return (str(e))


# @app.route("/getall")
def get_all():
    try:
        books = Pdf.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return (str(e))


# @app.route("/get/<id_>")
# def get_by_id(id_):
#     try:
#         book = Pdf.query.filter_by(id=id_).first()
#         return jsonify(book.serialize())
#     except Exception as e:
#         return (str(e))


def extract_details(file_path):
    extraction_module = extract.PdfExtract(file_path)
    extracted_data = extraction_module.process()
    try:
        book = Pdf(
            name=extracted_data['name'],
            contact_number=extracted_data['contact_number'],
            policy_number=extracted_data['policy_number']
        )
        db.session.add(book)
        db.session.commit()
        return "Pdf added. book id={}".format(book.id)
    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()

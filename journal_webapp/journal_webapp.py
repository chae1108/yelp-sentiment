from flask import Flask, render_template, redirect, url_for
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text
from sklearn.externals import joblib
from os import path
from flask_wtf import Form
from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from django.shortcuts import render_to_response

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///journal.db'
db = SQLAlchemy(app)
WTF_CSRF_ENABLED = False

class Journal(db.Model):
    id = Column(Integer, primary_key=True)
    body = Column(Text, unique=False)
    nb = Column(Integer, unique=False)

db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Journal,methods=['GET','POST','DELETE','PUT'])

class JournalForm(Form):
    journal = TextAreaField('journal', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = JournalForm(csrf_enabled=False)
    if form.validate_on_submit():
        APP_ROOT = path.dirname(path.abspath(__file__))
        APP_STATIC = path.join(APP_ROOT,'static')
        vect_nb = joblib.load(path.join(APP_STATIC,'joblib/vect_nb_pipeline_ttt.pkl'))
        if str(vect_nb.predict([form.journal.data]))=='[1]':
            journal = Journal(body=form.journal.data,nb=1)
        elif str(vect_nb.predict([form.journal.data]))=='[2]':
            journal = Journal(body=form.journal.data,nb=2)
        elif str(vect_nb.predict([form.journal.data]))=='[3]':
            journal = Journal(body=form.journal.data,nb=3)
        db.session.add(journal)
        db.session.commit()
    return render_template("index.html",form=form)

# @app.route('/', methods=['GET', 'POST'])
# def model():
#     form = JournalForm(csrf_enabled=False)
#     if form.validate_on_submit():
#         APP_ROOT = path.dirname(path.abspath(__file__))
#         APP_STATIC = path.join(APP_ROOT,'static')
#         vect_nb = joblib.load(path.join(APP_STATIC,'vect_nb.pkl'))
#         journal = Journal(body=form.journal.data,nb=1)
#         db.session.add(journal)
#         db.session.commit()
#         return HttpResponseRedirect("/")
#     return render_to_response("index.html", RequestContext(request, {}) )

# @app.route('/add', methods=['POST'])
# def add_entry():
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))

app.debug = True

if __name__ == '__main__':
    app.run()

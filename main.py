import flask
from flask_sqlalchemy import  SQLAlchemy
import base64
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField,FileField
from wtforms.validators import DataRequired, URL
from flask import Flask, render_template, redirect, url_for, session, request
from flask_bootstrap import Bootstrap
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Detail(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),  nullable=False)
    address = db.Column(db.String(300),  nullable=False)
    mob = db.Column(db.String(120),  nullable=False)
    luck= db.Column(db.String(120),  nullable=False)
    group= db.Column(db.String(120),  nullable=False)
    mimetype=db.Column(db.Text,nullable=False)
    img=db.Column(db.Text,nullable=False)
    filename=db.Column(db.Text,nullable=False)
class Form(FlaskForm):
    name=StringField("name",validators=[DataRequired()])
    address=StringField("address",validators=[DataRequired()])
    mob=StringField("mobile number",validators=[DataRequired()])
    luck=StringField("Lucky number",validators=[DataRequired()])
    group=StringField("Group number",validators=[DataRequired()])
    pic=FileField("drop the pic",validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField("Submit")

db.create_all()
@app.route('/',methods=["GET","POST"])
def start():
    form=Form()
    if request.method=="POST":
        pic =request.files['pic']
        if not pic :
            return "no pic uploaded",400
        filename=secure_filename(pic.filename)
        mimetype=pic.mimetype
        new=Detail(

        name=form.name.data,
        address=form.address.data,
        mob=form.mob.data,
        luck=form.luck.data,
        group=form.group.data,
        img=pic.read(),
        mimetype=mimetype,
        filename=filename

        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('start'))
    return render_template('index.html',form=form)
@app.route('/card/<id>')
def home(id):
  all =Detail.query.get(id)
  pic=base64.b64encode(all.img).decode('ascii')


  return render_template('card.html',all=all,pic=pic)


if __name__=="__main__":
   app.run(debug=True)
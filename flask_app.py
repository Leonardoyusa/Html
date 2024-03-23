python 
from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy 
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired 
from flask_wtf import FlaskForm 
import secrets 
import pandas as pd  

app = Flask(__name__) 
app.config['SECRET_KEY'] = secrets.token_urlsafe(16) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

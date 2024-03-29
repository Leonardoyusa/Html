python 
# main.py 
from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired 
import secrets 
import pandas as pd  

app = Flask(__name__) 
app.config['SECRET_KEY'] = secrets.token_urlsafe(16) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)  

class Treatment(db.Model): 
id = db.Column(db.Integer, primary_key=True) 
name = db.Column(db.String(50), nullable=False) 
frequency = db.Column(db.String(20), nullable=False) 
start_time = db.Column(db.String(5), nullable=False)  

class TreatmentForm(FlaskForm): 
name = StringField('Treatment Name', validators=[DataRequired()]) 
frequency = StringField('Frequency', validators=[DataRequired()]) 
start_time = StringField('Start Time', validators=[DataRequired()]) 
submit = SubmitField('Generate Schedule')  

@app.route('/') 
def show_form(): 
form = TreatmentForm() 
return render_template('index.html', form=form)  

@app.route('/generate-schedule', methods=['POST']) 
def handle_form(): 
form = TreatmentForm(request.form) 
if form.validate(): 
treatment = Treatment(name=form.name.data, 
frequency=form.frequency.data, start_time=form.start_time.data) 
db.session.add(treatment) 
db.session.commit()  

# Create a dictionary from the Form data 
data = {'Treatment Name': [form.name.data], 
'Frequency': [form.frequency.data], 
'Start Time': [form.start_time.data]}  

# Convert that dictionary to a DataFrame 
df = pd.DataFrame(data)  

# Convert the DataFrame to an HTML table and append it to the response string 
return ('Treatment schedule generated and saved! 
Here is your input:<br>' 
+ df.to_html())  

else: 
return 'Invalid'

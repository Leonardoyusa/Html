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
db = SQLAlchemy(app)  

class Treatment(db.Model): 
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(50), nullable=False) 
  time = db.Column(db.String(5), nullable=False)  
  
  class TreatmentForm(FlaskForm): 
    name = StringField('Treatment Name', validators=[DataRequired()]) 
    time = StringField('Time', validators=[DataRequired()]) 
    submit = SubmitField('Generate Schedule')  
    
    @app.route('/') 
    def show_form(): 
      form = TreatmentForm() 
      return render_template('index.html', form=form)  
      
      @app.route('/generate-schedule', methods=['POST']) 
      def handle_form(): 
        form = TreatmentForm(request.form) 
        if form.validate_on_submit(): 
          treatment = Treatment( 
            name=form.name.data, 
            time=form.time.data 
          ) 
          db.session.add(treatment) 
          db.session.commit()  
          
          df = generate_weekly_schedule(form.name.data, form.time.data)  
          
          return f'Treatment schedule generated and saved! Here is your input:<br>{df.to_html()}' 
        else: 
          return "Invalid input. Please try again."  
          
          def generate_weekly_schedule(name, time): 
            data = {"Time": [time], "Treatment": [name]} 
            data.update({day: [""] 
                         for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}) 
            df = pd.DataFrame(data) for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]: 
              df.loc[df.Time == time, day] = name 
              return df  
              
              if __name__ == '__main__': 
                app.run(debug=True)

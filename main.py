# Im category = StringField("Category", validators=[DataRequired()]) port necessary modules
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Y@m@$@k1'

# Configure database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///treatment_schedule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Form class
class TreatmentForm(FlaskForm):
    name = StringField("Treatment Name", validators=[DataRequired()])
    frequency = StringField("Frequency (in hours)", validators=[DataRequired()])
    start_time = StringField("Start Time (HH:MM AM/PM)", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()]) 
    submit = SubmitField("Submit")

# Define the Treatment model
class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)

# Create the tables
with app.app_context():
    db.create_all()

# Define route to handle form submission and generate schedule
@app.route('/', methods=['GET', 'POST'])
def index():
    form = TreatmentForm()
    if form.validate_on_submit():
        # Save data to the database
        treatment = Treatment(
            name=form.name.data,
            frequency=form.frequency.data,
            start_time=form.start_time.data
            category=form.category.data  
        )
        db.session.add(treatment)
        db.session.commit()

        # Retrieve treatment data from the database
        treatments = Treatment.query.all()

        # Process treatment data to create schedule (for simplicity, let's just pass the treatments to the template)
        return render_template('index.html', form=form, treatments=treatments)
    
    # If the form is not submitted, render the form
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, request
import csv

app = Flask(__name__)

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.form
    data = {key: str(value, 'utf-8') for key, value in data.items()}
    
    with open('form_data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([data.get(key, '') for key in data])
    
    return 'Data saved successfully!'

if __name__ == '__main__':
    app.run()

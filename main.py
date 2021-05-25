# Main program file - this file renders the mainpage and connects all routes

# Import Modules
from flask import Flask, render_template

app = Flask(__name__)
app._static_folder = ''

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# Main program file - this file renders the mainpage and connects all routes

# Import modules
from flask import Flask, g, redirect, render_template, request, session, url_for, flash
import pandas
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource



class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='bobatea'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))


######################
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/sak2129/personal_finance/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message=None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username=='sak2129' and password=='chikki':
            user = User.query.filter_by(username=username).first()
            login_user(user)
            return render_template('home.html', message=message)
        else:
            flash('Incorrect credentials - please try again.')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.')
    return render_template('login.html')

@app.route('/currentuser')
@login_required
def currentuser():
    return 'The current user is ' + current_user.username 

@app.route('/homepage')
def homepage():
    return home()


###################
from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account
import google.auth

credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

# Make clients.
bqclient = bigquery.Client(credentials=credentials, project=your_project_id,)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

# Download query results.
query_string = """
SELECT 
timestamp,
actual_expense,
forecast_value,
prediction_interval_lower_bound,
prediction_interval_upper_bound
FROM `sak2129-personal-finance.personal_finance_data.time_series_forecast`
"""
dataframe = (bqclient.query(query_string).result().to_dataframe(bqstorage_client=bqstorageclient))
#print(dataframe.head())
#credentials = service_account.Credentials.from_service_account_file('/sak2129-personal-finance-appdata/sak2129-personal-finance-0888d1628eac.json')
#project_id = 'sak2129-personal-finance'
#client = bigquery.Client(credentials= credentials,project=project_id)

actual_data = dataframe[dataframe['actual_expense'].notnull()][['timestamp','actual_expense']]
forecast_data = dataframe[dataframe['forecast_value'].notnull()][['timestamp','forecast_value']]

@app.route('/machinelearning')
def machinelearning():
    # Create a plot comparing the different sort algorithms
    p = figure(plot_width=900, 
            plot_height=400,
            title='Historical Data',
            x_axis_label = 'Date',
            y_axis_label = 'Amount (USD)')

    p.title.text_color = "black"
    p.title.text_font_size = "15px"

    p.line(actual_data['timestamp'],actual_data['actual_expense'], color='blue', legend_label='Actual Expenses', line_width=3)
    p.line(forecast_data['timestamp'], forecast_data['forecast_value'], color='green', legend_label='Forecasted Expenses', line_width=3)

    p.legend.location = "top_left"
    script, div = components(p)

    return render_template('machinelearning.html', actual_data=actual_data,forecast_data=forecast_data, the_div=div,the_script=script)


if __name__ == '__main__':
    #app.secret_key = os.urandom(12)
    app.run(port=8080, debug=False)

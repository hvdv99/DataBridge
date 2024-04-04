from flask import Flask, render_template, request
import jinja2
from flask_sqlalchemy import SQLAlchemy
import os

from services.querier.querier import DbQuerier

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

# I do not think it is necessary to connect to the database here, but I am not sure, so I did it anyway
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
db_location = os.path.join(basedir, "data/PostNL_SQLite.sqlite")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_location
db = SQLAlchemy(app)
dbquery = DbQuerier(sample_db_loc=db_location)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Basic setup for a flask query application. To include variables in HTML template,
    check the documentation for:
    - Flask: https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
    - Jinja HTML templates: https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance
    """
    if request.method == 'GET':
        return render_template('start_session.html')
    elif request.method == 'POST':
        return render_template('result.html')

@app.route('/vanna_table_view', methods=['GET', 'POST'])
def vanna_table_view():
    """
    Basic setup for a flask query application. To include variables in HTML template,
    check the documentation for:
    - Flask: https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
    - Jinja HTML templates: https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance
    """
    if request.method == 'POST':
        print("request.form: ", request.form)
        question = request.form['session_question']
        email = request.form['session_email']
        subject = request.form['session_subject']
        #sql_code = dbquery.generate_sql(question)
        sql_code = "SELECT month_id, SUM(parcels_home_1st) AS total_first_attempts FROM delivery_facts WHERE month_id LIKE '2023%' GROUP BY month_id ORDER BY total_first_attempts DESC LIMIT 10"
        print("sql_code: ", sql_code)

        df = dbquery.generate_sample_data(sql_query=sql_code)

        return render_template('vanna_table_view.html', tables=[df.to_html(classes='data')], titles=df.columns.values, sql_code = sql_code, question = question, email = email, subject = subject)
    else:
        sql_code = "SELECT month_id, SUM(parcels_home_1st) AS total_first_attempts FROM delivery_facts WHERE month_id LIKE '2023%' GROUP BY month_id ORDER BY total_first_attempts DESC LIMIT 10"
        print("sql_code: ", sql_code)

        df = dbquery.generate_sample_data(sql_query=sql_code)

        return render_template('vanna_table_view.html', tables=[df.to_html(classes='data')], titles=df.columns.values,
                               sql_code=sql_code)

        return render_template('start_session.html')


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import jinja2
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

from services.querier.querier import DbQuerier
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

# I do not think it is necessary to connect to the database here, but I am not sure, so I did it anyway
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
db_sample_data_location = os.path.join(basedir, "data/PostNL_SQLite.sqlite")

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_sample_data_location
#db_sample_data = SQLAlchemy(app)
dbquery = DbQuerier(sample_db_loc=db_sample_data_location)

db_requested_data_location = os.path.join(basedir, "data/PostNL_Requested_Data.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_requested_data_location
db_requested_data = SQLAlchemy(app)


class RequestedDataInit(db_requested_data.Model):
    __tablename__ = 'requested_data'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    email = Column(String)
    subject = Column(String)
    sql_code = Column(String)
    column_description_dict = Column(String)
    date_created = Column(DateTime)
    accepted_bool = Column(Integer)
    date_accepted_or_rejected = Column(DateTime)
    delivered_bool = Column(Integer)

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
        sql_code = dbquery.generate_sql(question)
        #sql_code = "SELECT month_id, SUM(parcels_home_1st) AS total_first_attempts FROM delivery_facts WHERE month_id LIKE '2023%' GROUP BY month_id ORDER BY total_first_attempts DESC LIMIT 10"
        print("sql_code: ", sql_code)

        df = dbquery.generate_sample_data(sql_query=sql_code).head(10)
        column_description_dict = dbquery.get_descriptions_for_given_columns(columns=df.columns.values)


        return render_template('vanna_column_description.html', tables=[df.to_html(classes='data')], titles=df.columns.values, sql_code = sql_code, question = question, email = email, subject = subject, column_description_dict = column_description_dict)
    else:
        sql_code = "SELECT month_id, SUM(parcels_home_1st) AS total_first_attempts FROM delivery_facts WHERE month_id LIKE '2023%' GROUP BY month_id ORDER BY total_first_attempts DESC LIMIT 10"
        print("sql_code: ", sql_code)

        df = dbquery.generate_sample_data(sql_query=sql_code)

        return render_template('vanna_table_view.html', tables=[df.to_html(classes='data')], titles=df.columns.values,
                               sql_code=sql_code)

        return render_template('start_session.html')

@app.route('/vanna_table_view/request_data', methods=['POST'])
def request_data():
    """
    Takes the data from the request object and adds it to the database
    :return:
    """
    question = request.form['session_question']
    email = request.form['session_email']
    subject = request.form['session_subject']
    sql_code = request.form["session_sql"]
    column_description_dict = request.form["column_description_dict"]

    new_requested_data = RequestedDataInit(
        question=question,
        email=email,
        subject=subject,
        sql_code=sql_code,
        column_description_dict=column_description_dict,
        date_created=datetime.now(),
        accepted_bool=0,
        date_accepted_or_rejected=None,
        delivered_bool=0
    )
    db_requested_data.session.add(new_requested_data)
    db_requested_data.session.commit()
    return jsonify({"success": True, "message": "Data request received"})



"""
    class DeliveryPreference(Base):
        __tablename__ = 'delivery_preference'
        account_id_hashed = Column(String, primary_key=True)
        deliverypreference = Column(String)
        datelastupdated = Column(DateTime)
        datecreated = Column(DateTime)
    def __init__(self, email, subject, question, column_description_dict, sql_code):
        self.request = request
        self.session_question = request.form['session_question']
        self.email = request.form['session_email']
        self.subject = request.form['session_subject']
        self.sql_code = request.form["question"]
        self.column_description_dict = request.form["column_description_dict"]

question = request.form['session_question']
    email = request.form['session_email']
    subject = request.form['session_subject']
    sql_code = request.form["question"]
    column_description_dict = request.form["column_description_dict"]"""

if __name__ == "__main__":
    app.run(debug=True)

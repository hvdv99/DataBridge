from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from services.querier.querier import DbQuerier
from sqlalchemy import Column, Integer, String, DateTime
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

#This takes the directory of the project and then goes up 3 directories to get to the root of the project
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
db_sample_data_location = os.path.join(basedir, "data", "PostNL_SQLite.sqlite")

#making the dbquery object for querying the database of PostNL data
dbquery = DbQuerier(sample_db_loc=db_sample_data_location)

# making the database to save and retrieve requested data
db_requested_data_location = os.path.join(basedir, "data", "PostNL_Requested_Data.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_requested_data_location
db_requested_data = SQLAlchemy(app)


class RequestedDataInit(db_requested_data.Model):
    __tablename__ = 'requested_data'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    email = Column(String)
    subject = Column(String)
    sql_code = Column(String)
    columns = Column(String)
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
        pass


@app.route('/vanna_table_view', methods=['GET', 'POST'])
def vanna_table_view():
    """
    This route is what is invoked when the user clicks the submit button on the start_session.html page. Which asks the database
    And then the page will display the first 10 rows of the data that is returned from the database but this happens in a different html file

    The else statement is for testing purposes, this loads an old html file with buttons for viewing the column descriptions
    This also uses a premade SQL query
    It is important to note that you need to give the parameter of the column description dict and the column description json. This is due to parsing not working properly. Else we will get issues with saving it later. So we use one to render in the uI and the json to send to the database to save.
    """
    if request.method == 'POST':
        question = request.form['session_question']
        email = request.form['session_email']
        subject = request.form['session_subject']
        sql_code = dbquery.generate_sql(question)
        #If something goes wrong with generating the SQL if the question does not lead a valid SQL query, then we will return an error message
        try:
            df = dbquery.generate_sample_data(sql_query=sql_code).head(10)

        except Exception as e:
            return render_template('start_session.html', error_message = f"I had an error generating the SQL, please rewrite question \n{str(e)}")
        column_description_dict = dbquery.get_descriptions_for_given_columns(columns=df.columns.values)


        return render_template('vanna_column_description.html', tables=[df.to_html(classes='data')], columns=df.columns.values, sql_code = sql_code, question = question, email = email, subject = subject, column_description_dict = column_description_dict)
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
    Takes the data from the request object and adds it to the database. Then it returns the same page with a success message
    then the script_request_data.js will redirect the user to the page with the button being disabled and a success message is shown
    :return:
    """
    question = request.form['session_question']
    email = request.form['session_email']
    subject = request.form['session_subject']
    sql_code = request.form["session_sql"]
    columns = request.form["columns"]

    new_requested_data = RequestedDataInit(
        question=question,
        email=email,
        subject=subject,
        sql_code=sql_code,
        columns = columns,
        date_created=datetime.now(),
        accepted_bool=0,
        date_accepted_or_rejected=None,
        delivered_bool=0
    )

    db_requested_data.session.add(new_requested_data)
    db_requested_data.session.commit()
    return jsonify({"success": True, "message": "Data request received"})


@app.route('/data_analyst_view', methods=['GET'])
def data_analyst_view():
    """
    This route is for the data analyst to view the requested data. It will show all the data that is requested from the database
    """
    result = RequestedDataInit.query.all()

    return render_template('data_analyst_view.html', requested_data=result)


@app.route('/view_request/<request_id>', methods=['GET'])
def view_request(request_id):
    """
    This route is for the data analyst to view the details of a single row based on the ID of request.
    It will show all the data that is requested with information about the person who requested.
    It gets the information about the request based on the "request_id" parameter that is given throug hthe URL
    """
    result = RequestedDataInit.query.filter_by(id=request_id).first()

    column_list = ast.literal_eval(result.columns)

    column_description_dict = dbquery.get_descriptions_for_given_columns(columns=column_list)
    example_table = dbquery.generate_sample_data(sql_query=result.sql_code).head(10)
    return render_template('view_request.html', requested_data=result,
                           tables = [example_table.to_html(classes='data')],
                           columns=example_table.columns.values,
                           column_description_dict = column_description_dict)



if __name__ == "__main__":
    app.run(debug=True)

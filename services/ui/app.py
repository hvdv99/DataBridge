from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from services.querier.querier import SqlGenerator
from sqlalchemy import Column, Integer, String, Date
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

# This takes the directory of the project and then goes up 3 directories to get to the root of the project
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DB_SAMPLE_DATA_LOCATION = os.path.join(BASEDIR, "data", "PostNL_SQLite.sqlite")

# making the dbquery object for querying the database of PostNL data
dbquery = SqlGenerator(sample_db_loc=DB_SAMPLE_DATA_LOCATION)

# making the database to save and retrieve requested data

DB_REQUESTED_DATA_LOCATION = os.path.join(BASEDIR, "data", "PostNL_Requested_Data.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_REQUESTED_DATA_LOCATION
db_requested_data = SQLAlchemy(app)



class RequestedDataInit(db_requested_data.Model):
    """
    The class for the requested data table in the database. This table is for keeping track of the made requests
    """

    __tablename__ = 'requested_data'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    email = Column(String)
    subject = Column(String)
    sql_code = Column(String)
    columns = Column(String)
    date_created = Column(Date)
    date_accepted_or_rejected = Column(Date)
    delivered_bool = Column(Integer)
    comments = Column(String)


# Creates the database if it does not exist
with app.app_context():
    db_requested_data.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Basic setup for a flask query application. To include variables in HTML template,
    check the documentation for:
    - Flask: https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
    - Jinja HTML templates: https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance
    """

    if request.method == 'GET':
        return render_template('start-session.html')
    elif request.method == 'POST':
        pass


@app.route('/vanna-table-view', methods=['GET', 'POST'])
def vanna_table_view():
    """
    This route is what is invoked when the user clicks the submit button on the start-session.html page. Which asks the
    database, and then the page will display the first 10 rows of the data that is returned from the database but this
    happens in a different html file.

    The else statement is for testing purposes, this loads an old html file with buttons for viewing the column
    descriptions. This also uses a pre-made SQL query. It is important to note that you need to give the parameter of
    the column description dict and the column description json. This is due to parsing not working properly. Else we
    will get issues with saving it later. So we use one to render in the uI and the json to send to the database to
    save.
    """

    if request.method == 'POST':
        question = request.form['session_question']
        email = request.form['session_email']
        subject = request.form['session_subject']
        sql_code = dbquery.generate_sql(question)
        print("sql_code: ", sql_code)
        sql_code = """SELECT DISTINCT account_id_hashed FROM delivery_preference WHERE deliverypreference IS NOT NULL"""

        # If something goes wrong with generating the SQL if the question does not lead a valid SQL query,
        # then we will return an error message
        try:
            df = dbquery.generate_sample_data(sql_query=sql_code).head(10)

        except Exception as e:
            error_text = f"I had an error generating the SQL, please rewrite question \n\n{str(e)}"

            return render_template('start-session.html', error_message=error_text)

        column_description_dict = dbquery.get_descriptions_for_given_columns(columns=df.columns.values)
        print("sql_code: ", sql_code)
        print("df: ", df.head(10))
        print("df.columns.values: ", df.columns.values)
        print("df.columns.values type: ", type(df.columns.values))

        return render_template('vanna-column-description.html',
                               tables=[df.to_html(classes='data')],
                               columns=df.columns.values,
                               sql_code=sql_code,
                               question=question,
                               email=email,
                               subject=subject,
                               column_description_dict=column_description_dict
                               )

    else:
        # This code is executed when the user only runs the url /vanna-table-view without submitting a form
        sql_code = """SELECT month_id, SUM(parcels_home_1st) AS total_first_attempts 
                      FROM delivery_facts WHERE month_id LIKE '2023%' 
                      GROUP BY month_id 
                      ORDER BY total_first_attempts DESC LIMIT 10"""

        df = dbquery.generate_sample_data(sql_query=sql_code)
        print("sql_code: ", sql_code)
        print("sql_code: ", sql_code)
        print("df: ", df.head(10))

        column_description_dict = dbquery.get_descriptions_for_given_columns(columns=df.columns.values)

        return render_template('vanna-table-view.html',
                               tables=[df.to_html(classes='data')],
                               titles=df.columns.values,
                               sql_code=sql_code,
                               columns=df.columns.values,
                               column_description_dict=column_description_dict,
                               email="test@test.nl",
                               subject="test",
                               question="test"
                               )


@app.route('/vanna-table-view/request-data', methods=['POST'])
def request_data():
    """
    Takes the data from the request object and adds it to the database. Then it returns the same page with a success
    message then the script_request_data.js will redirect the user to the page with the button being disabled and a
    success message is shown
    :return json return message:
    """

    question = request.form['session_question']
    email = request.form['session_email']
    subject = request.form['session_subject']
    sql_code = request.form["session_sql"]
    columns = request.form["columns"]
    comments = request.form["session_data_comments"]
    print("comments: ", comments)

    new_requested_data = RequestedDataInit(question=question,
                                           email=email,
                                           subject=subject,
                                           sql_code=sql_code,
                                           columns=columns,
                                           date_created=datetime.now(),
                                           date_accepted_or_rejected=None,
                                           delivered_bool=0,
                                           comments=comments
                                           )

    db_requested_data.session.add(new_requested_data)
    db_requested_data.session.commit()

    return jsonify({"success": True, "message": "Data request received"})


@app.route('/data-analyst-view', methods=['GET', 'POST'])
def data_analyst_view():
    """
    This route is for the data analyst to view the requested data. It will show all the data that is requested from the
    database.
    :return: html template
    """
    if request.method == 'POST':
        RequestedDataInit.query.filter_by(id=request.form['request_id']).update(dict(delivered_bool=1))
        today = datetime.today()
        RequestedDataInit.query.filter_by(id=request.form['request_id'])\
            .update(dict(date_accepted_or_rejected=today))
        db_requested_data.session.commit()



    result = RequestedDataInit.query.all()

    return render_template('data-analyst-view.html', requested_data=result)


@app.route('/view-request/<request_id>', methods=['GET'])
def view_request(request_id):
    """
    This route is for the data analyst to view the details of a single row based on the ID of request.
    It will show all the data that is requested with information about the person who requested.
    It gets the information about the request based on the "request_id" parameter that is given through the URL
    """


    result = RequestedDataInit.query.filter_by(id=request_id).first()
    example_table = dbquery.generate_sample_data(sql_query=result.sql_code).head(10)
    column_list = list(example_table.columns.values)
    column_description_dict = dbquery.get_descriptions_for_given_columns(columns=column_list)

    print("column_description_dict: ", column_description_dict)
    print("column_list", list(example_table.columns.values))

    return render_template('view-request.html',
                           requested_data=result,
                           tables=[example_table.to_html(classes='data')],
                           columns=example_table.columns.values,
                           column_description_dict=column_description_dict,
                           request_id=request_id,
                           sql_code=result.sql_code,
                           comments=result.comments

                           )


if __name__ == "__main__":
    app.run(debug=True)

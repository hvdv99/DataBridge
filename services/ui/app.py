import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

from querier.querier import SqlGenerator

app = Flask(__name__)
app.config["SECRET_KEY"] = "123"

# Get the absolute path to the project directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, "data")

DB_SAMPLE_DATA_LOCATION = os.path.join(DATA_DIR, "PostNL_SQLite.sqlite")
DB_REQUESTED_DATA_LOCATION = os.path.join(DATA_DIR, "PostNL_Requested_Data.sqlite")

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Update the database URI to use the absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_REQUESTED_DATA_LOCATION

# making the dbquery object for querying the database of PostNL data
dbquery = SqlGenerator(sample_db_loc=DB_SAMPLE_DATA_LOCATION)

# removing all training data and training the model
dbquery.remove_all_training_data()
dbquery.train_model(train_on_sql=False)

# making the database to save and retrieve requested data
db_requested_data = SQLAlchemy(app)


class RequestedDataInit(db_requested_data.Model):
    """
    The class for the requested data table in the database. This table is for keeping track of the made requests
    """

    __tablename__ = "requested_data"
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


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template("start-session.html")


@app.route("/vanna-table-view", methods=["GET", "POST"])
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

    if request.method == "POST":
        question = request.form["session_question"]
        email = request.form["session_email"]
        subject = request.form["session_subject"]
        sql_code = dbquery.generate_sql(question)

        # If something goes wrong with generating the SQL if the question does not lead a valid SQL query,
        # then we will return an error message
        try:
            df = dbquery.generate_sample_data(sql_query=sql_code).head(10)

        except Exception as e:
            error_text = "  Ik had een probleem met jouw vraag, probeer opnieuw!"
            print(f"Ik had een probleem met jouw vraag, probeer opnieuw! \n\n{str(e)}")

            return render_template("start-session.html", error_message=error_text)

        column_description_dict = dbquery.get_descriptions_for_given_columns(columns=df.columns.values)

        return render_template("vanna-column-description.html",
                               tables=[df.to_html(classes="data")],
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
                      FROM delivery_facts WHERE month_id LIKE "2023%" 
                      GROUP BY month_id 
                      ORDER BY total_first_attempts DESC LIMIT 10"""

        df = dbquery.generate_sample_data(sql_query=sql_code)

        column_description_dict = dbquery.get_descriptions_for_given_columns(columns=df.columns.values)

        return render_template("vanna-table-view.html",
                               tables=[df.to_html(classes="data")],
                               titles=df.columns.values,
                               sql_code=sql_code,
                               columns=df.columns.values,
                               column_description_dict=column_description_dict,
                               email="test@test.nl",
                               subject="test",
                               question="test"
                               )


@app.route("/vanna-table-view/request-data", methods=["POST"])
def request_data():
    """
    Takes the data from the request object and adds it to the database. Then it returns the same page with a success
    message then the script_request_data.js will redirect the user to the page with the button being disabled and a
    success message is shown
    :return json return message:
    """

    question = request.form["session_question"]
    email = request.form["session_email"]
    subject = request.form["session_subject"]
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


@app.route("/data-analyst-view", methods=["GET", "POST"])
def data_analyst_view():
    """
    This route is for the data analyst to view the requested data. It will show all the data that is requested from the
    database.
    :return: html template
    """
    if request.method == "POST":
        RequestedDataInit.query.filter_by(id=request.form["request_id"]).update(dict(delivered_bool=1))
        today = datetime.today()
        RequestedDataInit.query.filter_by(id=request.form["request_id"])\
            .update(dict(date_accepted_or_rejected=today))
        db_requested_data.session.commit()

    result = RequestedDataInit.query.all()

    return render_template("data-analyst-view.html", requested_data=result)


@app.route("/view-request/<request_id>", methods=["GET"])
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

    return render_template("view-request.html",
                           requested_data=result,
                           tables=[example_table.to_html(classes="data")],
                           columns=example_table.columns.values,
                           column_description_dict=column_description_dict,
                           request_id=request_id,
                           sql_code=result.sql_code,
                           comments=result.comments

                           )


if __name__ == "__main__":
    app.run(debug=True, port=5000)

from flask import Flask, render_template, request

# importing the custom VannaQuerier class
import vanna.VannaQuerier as vq


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Basic setup for a flask query application. To include variables in HTML template,
    check the documentation for:
    - Flask: https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
    - Jinja HTML templates: https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance
    """
    if request.method == 'GET':
        render_template('query.html')
    elif request.method == 'POST':
        render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True)

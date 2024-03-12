# Documentation was really useful: https://vanna.ai/docs/vanna.html
import os

from vanna.remote import VannaDefault

from dotenv import load_dotenv

load_dotenv('.env')  # for getting environment variables

api_key = os.environ.get('VANNA_API_KEY')
vanna_model_name = 'test-vanna'

vn = VannaDefault(model=vanna_model_name, api_key=api_key)

vn.connect_to_sqlite('../data/PostNL_SQLite.sqlite')

# Training the vector db in Vanna with DDL
# What is DDL? See: https://www.techtarget.com/whatis/definition/Data-Definition-Language-DDL
df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
for ddl in df_ddl['sql'].to_list():
    vn.train(ddl=ddl)

# Training the vector db in Vanna with self generated documentation
with open('db-training-docs.txt', 'r') as f:
    docs = f.read()
    vn.train(documentation=docs)

# Training the vector db with small SQL statements to give it some sample data to work with
sample_queries = [
    """SELECT * 
  FROM collo_packages AS cp
  WHERE cp.account_id_hashed IS NOT NULL
  LIMIT 20;
  """,
    """SELECT * 
  FROM delivery_facts AS df
  WHERE df.account_id_hashed IS NOT NULL
  LIMIT 20;
  """,
    """SELECT *
  FROM delivery_preference as dp
  WHERE dp.account_id_hashed IS NOT NULL
  LIMIT 20;
  """
]

for sq in sample_queries:
    sq_result = vn.run_sql(sq)
    vn.train(sql=sq)

# You can remove training data if there's obsolete/incorrect information.
# vn.remove_training_data(id='1-ddl')


# ## Asking the AI
# Whenever you ask a new question, it will find the 10 most relevant pieces of training data and use it as part of the
# LLM prompt to generate the SQL.

# vn.ask(question="what columns are available in my data?")


# ## Launch the User Interface
# ![vanna-flask](https://vanna.ai/blog/img/vanna-flask.gif)


from vanna.flask import VannaFlaskApp

app = VannaFlaskApp(vn)
app.run()

# ## Next Steps
# Using Vanna via Jupyter notebooks is great for getting started but check out additional customizable interfaces like the 
# - [Streamlit app](https://github.com/vanna-ai/vanna-streamlit)
# - [Flask app](https://github.com/vanna-ai/vanna-flask)
# - [Slackbot](https://github.com/vanna-ai/vanna-slack)

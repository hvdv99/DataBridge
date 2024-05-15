import sqlite3
import pandas as pd
import os

# Get the absolute path to the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PostNL_DB = os.path.join(BASE_DIR, '..', '..', 'data', 'PostNL_SQLite.sqlite')


def execute_query(query):
    with sqlite3.connect(PostNL_DB) as conn:
        return pd.read_sql(query, conn)


def answer(correct_query):
    return execute_query(correct_query)


def answer_vanna(vanna_query):
    return execute_query(vanna_query)

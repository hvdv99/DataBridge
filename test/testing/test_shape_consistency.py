import pytest
import os
import json
from test.testing.functions import answer, answer_vanna

# Define paths to locate the JSON files with SQL queries
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_ANSWERS_PATH = os.path.join(BASE_DIR, '..', '..', 'data', 'test_questions.json')
VANNA_ANSWERS_PATH = os.path.join(BASE_DIR, '..', 'vanna_output', 'vanna_output.json')

def load_sql_queries(json_file_path, query_category):
    """
    Load SQL queries based on a category (e.g., 'easy_questions') from a specified JSON file.
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    queries = [item['sql'] for item in data[query_category].values()]
    return queries

# Load queries for both the expected and experimental setups for easy and hard difficulty levels
easy_expected_queries = load_sql_queries(SQL_ANSWERS_PATH, 'easy_questions')
hard_expected_queries = load_sql_queries(SQL_ANSWERS_PATH, 'hard_questions')
easy_experimental_queries = load_sql_queries(VANNA_ANSWERS_PATH, 'easy_questions')
hard_experimental_queries = load_sql_queries(VANNA_ANSWERS_PATH, 'hard_questions')

# Prepare pairs of queries for testing by zipping expected and experimental queries together
easy_query_pairs = list(zip(easy_expected_queries, easy_experimental_queries))
hard_query_pairs = list(zip(hard_expected_queries, hard_experimental_queries))

@pytest.mark.parametrize("expected_sql,experimental_sql", easy_query_pairs + hard_query_pairs)
def test_sql_query_shape_consistency(expected_sql, experimental_sql):
    """
    Test to ensure that SQL queries produce dataframes of the same shape.
    This validates that the structure (number of rows and columns) is consistent between the two dataframes.
    """
    df_expected = answer(expected_sql)
    df_experimental = answer_vanna(experimental_sql)
    assert df_expected.shape == df_experimental.shape, f"DataFrames do not have the same shape: {df_expected.shape} != {df_experimental.shape}"

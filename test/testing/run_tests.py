import pytest
import os
import json
from pathlib import Path

# Ensure this import is correct according to your directory structure
from test.testing.test_shape_consistency import prepared_data

# Define paths to locate the JSON files with SQL queries
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_ANSWERS_PATH = os.path.join(BASE_DIR, '..', 'test_questions', 'test_questions.json')


def load_sql_queries(json_file_path, query_category):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    queries = [item['sql'] for item in data[query_category].values()]
    return queries


def load_nl_questions(json_file_path, query_category):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    questions = [item['question'] for item in data[query_category].values()]
    return questions


def prepare_data(vanna_output_path: str):
    with open(SQL_ANSWERS_PATH, 'r', encoding='utf-8') as file:
        data_true = json.load(file)
    with open(vanna_output_path, 'r', encoding='utf-8') as file:
        data_vanna = json.load(file)

    data = []
    for category in ['easy_questions', 'hard_questions']:
        for number in data_true[category].keys():
            item = (
                category,
                number,
                data_true[category][number]['question'],
                data_true[category][number]['sql'],
                data_vanna[category][number]['sql']
            )
            data.append(item)
    return data


def run_tests(vanna_outputs):
    test_file = 'test_shape_consistency.py'
    for vanna_output in vanna_outputs:
        prepared_data[:] = prepare_data(vanna_output)
        output_filename = Path(vanna_output).stem
        pytest.main([test_file, f'--html=../test_results/{output_filename}.html'])


# List of Vanna output files
vanna_outputs = [
    'path/to/vanna_output.json'
]

if __name__ == "__main__":
    run_tests(vanna_outputs)

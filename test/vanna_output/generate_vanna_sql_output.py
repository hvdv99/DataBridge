from services.querier.querier import SqlGenerator
import os
import json
import re
from datetime import datetime

# Define the paths for the database and JSON files.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '..', '..', 'data', 'PostNL_SQLite.sqlite')
ANSWERS_2_TEST_PATH = os.path.join(BASE_DIR, '..', 'test_questions', 'test_questions.json')

# Create an SqlGenerator object for querying the PostNL database.
dbquery = SqlGenerator(sample_db_loc=DATABASE_PATH)

# Initialize the model training process and remove any prior training data.
dbquery.remove_all_training_data()
dbquery.train_model(train_on_documentation=True, train_on_ddl=True, train_on_sql=False,
                    train_on_question_sql_pairs=False)


def clean_sql(sql_code: str) -> str:
    """
    Clean SQL code by removing unnecessary whitespaces and special sequences.

    Args:
    - sql_code (str): The raw SQL string to be cleaned.

    Returns:
    - str: Cleaned SQL string.
    """
    # Replace multiple spaces with a single space and trim the result.
    return re.sub(r'\s+', ' ', sql_code).strip()


def sql_output_vanna(question: str) -> str:
    """
    Generate and clean SQL output for a given question using the trained SqlGenerator model.

    Args:
    - question (str): The question from which to generate SQL.

    Returns:
    - str: Cleaned SQL code generated from the question.
    """
    sql_code = dbquery.generate_sql(question)
    return clean_sql(sql_code)


def load_json(file_path: str):
    """
    Load JSON data from a specified file path.

    Args:
    - file_path (str): Path to the JSON file.

    Returns:
    - dict: Parsed JSON data as a dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def generate_question_sql_dict(data: dict) -> dict:
    """
    Generate a dictionary mapping questions to their SQL outputs, organized by categories.

    Args:
    - data (dict): Dictionary containing questions categorized by various headers.

    Returns:
    - dict: A dictionary with categories as keys and question-SQL mappings as values.
    """
    output = {}
    for category, questions in data.items():
        output[category] = {qid: {"question": info['question'], "sql": sql_output_vanna(info['question'])}
                            for qid, info in questions.items()}
    return output


# Load the JSON data from the specified file.
data = load_json(ANSWERS_2_TEST_PATH)
model_name = dbquery.config['model']

for _ in range(10):

    # Define and write the output to a JSON file.
    timestamp = datetime.now().strftime("%H%M%S_%d%m%Y")
    output_file_name = f'vanna_output_{model_name}_{timestamp}.json'

    with open(output_file_name, 'w', encoding='utf-8') as json_file:
        # Generate the dictionary mapping questions to their SQL outputs.
        question_sql_output = generate_question_sql_dict(data)
        json.dump(question_sql_output, json_file, indent=4, ensure_ascii=False)

    print(f"Output JSON file created: {output_file_name}")

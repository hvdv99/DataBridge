import os
import logging
import sys
import json

import pandas as pd
from groq import Groq

from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

from services.config import constants as c

logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # sys.stdout = logging messages to console
# level = general info messages


class CustomVanna(ChromaDB_VectorStore, OpenAI_Chat):
    """
    CustomVanna class is used to customize Vanna to our own needs. In this case, the context model (vector db)
    is configured. Also, Groq is used as an LLM.
    """

    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        groq_client = Groq(api_key=c.GROQ_API_KEY)
        OpenAI_Chat.__init__(self, client=groq_client, config=config)


class SqlGenerator:
    """
    The SqlGenerator class generates Sql queries based on a question send by the user. To use this class,
    make sure to install the requirements, get your groq api key and insert it in the personal_constants file.
    You can get your api key here: https://console.groq.com/keys
    ...
    Parameters
    sample_db_loc: string
        The path to the database file
    ...
    Attributes
    ----------
    vanna: CustomVanna
        The customized version of the vanna class, as defined above
    training_data: pd.DataFrame
        In this DataFrame the current collection of training data is kept and will be updated with each
        change.
    ...
    Methods
    -------
    All methods are implementations of the methods of the Base Vanna class. You can check those methods
    by looking at the source code: https://github.com/vanna-ai/vanna/blob/main/src/vanna/base/base.py
    """

    def __init__(self, sample_db_loc: str):
        """
        This function is used to initialize the class and give it its basic variables.
        :param sample_db_loc: the location of where your database is stored. The database can be created if you run
        db_init.py script.
        """

        chromadb_filepath = os.path.join('.', 'services', 'querier', 'chroma-db-files')
        if not os.path.exists(chromadb_filepath):
            os.mkdir(chromadb_filepath)

        config = {
            'model': 'mixtral-8x7b-32768',  # the model used by Groq
            'path': chromadb_filepath  # path where chroma-db-keeps its files
        }

        self.vanna = CustomVanna(config=config)
        self.vanna.connect_to_sqlite(sample_db_loc)  # connecting to the db
        self.training_data_path = os.path.join('services', 'querier', 'training-data')
        self.training_data = self.vanna.get_training_data()  # method from the original vanna class, returns Pandas df
        # this variable will show a pandas dataframe containing all the contextual training data

    def remove_all_training_data(self):
        """
        Method that removes all training data from the model.
        :return: None
        """
        for i in range(len(self.training_data)):
            self.vanna.remove_training_data(id=self.training_data['id'].iloc[i])

        # setting the class training data to empty df
        self.training_data = pd.DataFrame(columns=self.training_data.columns)

        # testing if it worked
        if len(self.vanna.get_training_data()) == 0:
            logging.info("Training data removed")

    def train_model_on_ddl(self):
        """
        Trains the model on Data Definition Language (DDL).
        What is DDL? See: https://www.techtarget.com/whatis/definition/Data-Definition-Language-DDL
        :return: None
        """
        # The query below returns general information
        df_ddl = self.vanna.run_sql("select * from sqlite_master where type = 'table' order by name;")
        for ddl in df_ddl['sql'].to_list():
            self.vanna.train(ddl=ddl)

        logging.info('trained model on ddl')

    def train_model_on_sql(self):
        """
        Trains the vanna remote context model on the query files listed in training-data/train_on_sql-queries
        Important: Vanna actually requires an associated question to a SQL query. This function does not require that,
        Vanna automatically generates an associating question to a sql query using a LLM
        :return: None
        """
        sql_query_file_path = os.path.join('.', 'services', 'querier', 'training-data', 'sql-queries')
        query_files = [f for f in os.listdir(sql_query_file_path) if f.endswith('.train_on_sql')]
        for query in query_files:
            with open(os.path.join(sql_query_file_path, query), 'r') as q:
                self.vanna.train(sql=q.read())

        logging.info('trained model on sql queries')

    def train_model_on_documentation(self):
        """
        Trains the vanna remote context model on the documentation files listed in training-data/documentation
        :return: None
        """
        documentation_files =\
            [f for f in os.listdir(os.path.join(self.training_data_path, 'documentation')) if f.endswith('.txt')]
        for doc_file in documentation_files:
            with open(os.path.join(self.training_data_path, 'documentation', doc_file), 'r') as d:
                file_data = d.read().split('\n\n')  # creating chunks for each line

                for chunk in file_data:
                    self.vanna.add_documentation(chunk)

        logging.info('Trained model on documentation files')

    def train_model_on_question_sql_pairs(self):
        """
        Function to train the model on questions and sql pairs.
        :return: None
        """
        question_sql_pairs_path = os.path.join('.', 'services', 'querier', 'training-data', 'question-sql-pairs',
                                               'question-sql-pairs.json')
        if os.path.exists(question_sql_pairs_path):
            with open(question_sql_pairs_path, 'r') as f:
                question_sql_pairs_file = json.load(f)

                for question, sql in question_sql_pairs_file.items():
                    self.vanna.train(question=question, sql=sql)

            logging.info("Trained on question-sql pairs.")

    def train_model(self, train_on_documentation: bool = True,
                    train_on_sql: bool = True,
                    train_on_ddl: bool = True,
                    train_on_question_sql_pairs: bool = True):
        """
        Wrapper method that allows to train model on various types of input sources.
        :return:
        """
        if train_on_documentation:
            self.train_model_on_documentation()

        if train_on_sql:
            self.train_model_on_sql()

        if train_on_ddl:
            self.train_model_on_ddl()

        if train_on_question_sql_pairs:
            self.train_model_on_question_sql_pairs()

        self.training_data = self.vanna.get_training_data()  # updating the classes training data

        logging.info('training model on all types of data finished')

    def generate_sample_data(self, sql_query: str) -> pd.DataFrame:
        """
        Function that executes a SQL query on the connected sample database.
        :param sql_query: a string with the SQL query
        :return: a pandas dataframe with the database data
        """
        return self.vanna.run_sql(sql_query)

    def generate_sql(self, question: str) -> str:
        """
        Function that generates a sql query based on a question.
        :param question:
        :return: a string with the generated SQL code
        """
        generated_sql = self.vanna.generate_sql(question)
        generated_sql = generated_sql.replace("\\", "")
        return generated_sql

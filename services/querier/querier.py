import os
import logging
import sys

import pandas as pd
from vanna.remote import VannaDefault

from services.config import constants as c


class DbQuerier:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # sys.stdout = logging messages to console
    # level = general info messages.
    training_data_path = '/training-data'

    def __init__(self, sample_db_loc):
        """
        This function is used to initialize the class and give it its basic variables
        :param sample_db_loc: the location of where your database is stored. The database can be created if you run
        Berkays db_init.py script.
        """
        self.vanna = VannaDefault(api_key=c.VANNA_API_KEY, model=c.VANNA_MODEL_NAME)  # using the existing Vanna class
        self.vanna.connect_to_sqlite(sample_db_loc)  # connecting to the db
        self.training_data = self.vanna.get_training_data()  # method from the original vanna class, returns Pandas df
        # this variable will show a pandas dataframe containing all the contextual training data

    def remove_all_training_data(self):
        """
        Method that removes all training data from the model
        :return: None
        """
        for i in range(len(self.training_data)):
            self.vanna.remove_training_data(id=self.training_data['id'].iloc[i])

        if len(self.training_data) == 0:
            logging.info("Training data removed")

        # setting the class training data to empty df
        self.training_data = pd.DataFrame(columns=self.training_data.columns)

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
        :return: None
        """
        sql_query_file_path = './services/querier/training-data/sql-queries'
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
        logging.debug(os.getcwd())
        documentation_file_path = "./services/querier/training-data/documentation"
        documentation_files = [f for f in os.listdir(documentation_file_path) if f.endswith('.txt')]
        for doc_file in documentation_files:
            with open(os.path.join(documentation_file_path, doc_file), 'r') as d:
                self.vanna.train(documentation=d.read())

        logging.info('Trained model on documentation files')

    def train_model_on_question_sql_pairs(self):
        """
        TODO - Function to train the model on questions and resulting sql pairs.
        :return:
        """
        pass

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

        self.training_data = self.vanna.get_training_data()

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
        :return:
        """
        return self.vanna.generate_sql(question)

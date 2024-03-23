import os
import logging, sys

import pandas as pd
from vanna.remote import VannaDefault

from ..config import constants as c


class DBQuerier:

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    training_data_path = '/training-data'

    def __init__(self, sample_db_loc):
        self.vanna = VannaDefault(api_key=c.VANNA_API_KEY, model=c.VANNA_MODEL_NAME)  # using the existing Vanna class
        self.vanna.connect_to_sqlite(sample_db_loc)
        self.training_data = self.vanna.get_training_data()  # method from the original vanna class, returns Pandas df

    def remove_all_training_data(self):
        """
        Method that removes all training data from the model
        :return:
        """
        for i in range(len(self.training_data)):
            self.vanna.remove_training_data(id=self.training_data['id'].iloc[i])
        # setting the class training data to empty df
        self.training_data = pd.DataFrame(columns=self.training_data.columns)

        if len(self.training_data) == 0:
            logging.info("Training data removed")

    def train_model_on_ddl(self):
        pass

    def train_model_on_sql(self):
        pass

    def train_model_on_documentation(self):
        pass

    def train_model_on_question_sql_pairs(self):
        pass

    def train_model(self, documentation: bool = True, sql: bool = True, ddl: bool = True, ):
        """
        Method that will train the model on all types of training data
        :return:
        """
        self.training_data = self.vanna.get_training_data()

    def generate_sample_data(self, sql_query):
        pass

    def generate_sql(self, question):
        pass


    
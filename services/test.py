# Documentation was really useful: https://vanna.ai/docs/vanna.html
import os

from vanna.remote import VannaDefault
from config import constants as c

api_key = c.VANNA_API_KEY

vn = VannaDefault(model=c.VANNA_MODEL_NAME, api_key=c.VANNA_API_KEY)

training_data = vn.get_training_data()

for i in range(len(training_data)):
    vn.remove_training_data(id=training_data['id'].iloc[i])




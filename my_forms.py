import pandas as pd
from wtforms import Form, SelectField

# Load department list; SelectField only accepts tuples of (value, label)
path = './data/dept_list.csv'
dept_list = pd.read_csv(path, sep=',', header=None, squeeze=True)
dept_list = [(dept_name, dept_name) for dept_name in dept_list]

class SkillsForm(Form):
	dept_name = SelectField('Department', choices=dept_list)

cnx = mysql.connector.connect(user='Bob', password='foobar', host='127.0.0.1', database='passwords')
query = ("SELECT * FROM pwds")
cursor = cnx.cursor(dictionary=True)
cursor.execute(query)


import mysql.connector

# Context manager, store password in config
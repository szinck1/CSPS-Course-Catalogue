from wtforms import Form, SelectField

class ChoiceForm(Form, field_name, choices):
	choice = SelectField(field_name, choices=choices)

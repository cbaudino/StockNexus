from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=200)])
    price = DecimalField('Price', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired(), Length(max=100)])
    stock = IntegerField('Stock', validators=[DataRequired()])
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, SubmitField, TextAreaField, DecimalField, IntegerField, SelectField, ValidationError, RadioField
from wtforms.validators import DataRequired, Email, Length, InputRequired 
from models import db, Service 

class Adminprofileform(FlaskForm):
    username = StringField('Name:', validators=[Length(max=100)])
    email = StringField('Email:', validators=[Email(), Length(max=100)])
    submit = SubmitField('Save Changes')

class Editpasswordform(FlaskForm):
    old_password = PasswordField('Old Password:', validators=[InputRequired()])
    new_password = PasswordField('New Password:', validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password:', validators=[InputRequired()])
    submit = SubmitField('Save Changes')

class Loginform(FlaskForm):
    email = StringField('Email:', validators=[Email(), InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    submit = SubmitField('Login')

class Customerregistrationform(FlaskForm):
    username = StringField('Name:', validators=[InputRequired(), Length(max=100)])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8)])
    contact = IntegerField('Contact:', validators=[InputRequired()])
    address = TextAreaField('Address:', validators=[InputRequired()])
    city = StringField('City:', validators=[InputRequired()])
    state = StringField('State:', validators=[InputRequired()])
    pincode = IntegerField('Pincode:', validators=[InputRequired()])
    submit = SubmitField('Register')


class Professionalregistrationform(FlaskForm):
    username = StringField('Name:', validators=[InputRequired(),Length(max=100)])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8)])
    contact = IntegerField('Contact:', validators=[InputRequired()])
    address = StringField('Address:', validators=[InputRequired()])
    city = StringField('City:', validators=[InputRequired()])
    state = StringField('State:', validators=[InputRequired()])
    pincode = IntegerField('Pincode:', validators=[InputRequired()])
    service = SelectField('Service:', choices=[], validators=[InputRequired()])
    resume = FileField('Upload Resume(pdf)', validators=[InputRequired()])
    experience = IntegerField('Experience:(in yrs)', validators=[InputRequired()])
    submit = SubmitField('Register')

    def populate_choices(self):
        distinct_categories = Service.query.with_entities(Service.category).filter_by(deleted=False).distinct().all()
        self.service.choices = [('', 'Choose Service')] + [(category[0], category[0]) for category in distinct_categories]

    def validate_service(form, field):
        if field.data == '':
            raise ValidationError('Please choose a valid service.')
        
class Editprofileform(FlaskForm):
    username = StringField('Name:', validators=[InputRequired()])
    email = StringField('Email:', validators=[Email(), InputRequired()])
    contact = IntegerField('Contact:', validators=[InputRequired()])
    address = StringField('Address:', validators=[InputRequired()])
    city = StringField('City:', validators=[InputRequired()])
    state = StringField('State:', validators=[InputRequired()])
    pincode = IntegerField('Pincode:', validators=[InputRequired()])
    submit = SubmitField('Save Changes')
            

class Addserviceform(FlaskForm):
    service_name = StringField('Service Name:', validators=[InputRequired()])
    category = StringField('Category:', validators=[InputRequired()])
    price = DecimalField('Price:', places=2,validators=[InputRequired()])
    duration = StringField('Duration:', validators=[InputRequired()])
    description = TextAreaField('Description:', validators=[InputRequired()])
    submit = SubmitField('Add Service')

class Editserviceform(FlaskForm):
    service_name = StringField('Service Name:', validators=[InputRequired()])
    category = StringField('Category:', validators=[InputRequired()])
    price = DecimalField('Price:', places=2, validators=[InputRequired()])
    duration = StringField('Duration:', validators=[InputRequired()])
    description = StringField('Description:', validators=[InputRequired()])
    submit = SubmitField('Save Changes')

class Reviewform(FlaskForm):
    remarks = TextAreaField('Remarks', validators=[InputRequired()])
    rating = RadioField('Rating', choices=[
        ('1', '😠'), 
        ('2', '😟'),
        ('3', '😐'),
        ('4', '🙂'),
        ('5', '🙂')
    ], validators=[InputRequired()])
    submit = SubmitField('Submit Review')

class Customerfilterform(FlaskForm):
    category = SelectField('Service Category', validators=[InputRequired()], choices=[])
    search_string = StringField('Search in description', validators=[InputRequired()])
    submit = SubmitField('Search')

    def populate_service_choices(self):
        distinct_categories = Service.query.with_entities(Service.category).distinct().all()
        self.category.choices = [('', 'Choose Category')] + [(category[0], category[0]) for category in distinct_categories]

    def validate_category(self, field):
        if field.data == '':
            raise ValidationError('Please choose a valid category.')




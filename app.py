from datetime import date, datetime
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm, Form
from wtforms.fields import StringField, FieldList, FormField, SubmitField, SelectMultipleField, IntegerField, \
    DateField
from wtforms.validators import ValidationError, DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "Just_app for T3S4"

class A(Form):
    first_name = StringField('first name: ')
    last_name = StringField('last name:')
    b_date = DateField('date: ')
    select_field = SelectMultipleField('Gendre: ', choices=[('male', 'Male'), ('female', 'Female')])
    delete_entry = SubmitField('delete entry')

    def validate_first_name(self, first_name):
        if not first_name.data:
            raise ValidationError('first name should not be empty')

    def validate_last_name(self, last_name):
        if not last_name.data:
            raise ValidationError('last name should not be empty')

    def validate_select_field(self, select_field):
        if set(select_field.data) - {'female', 'male'}:
            raise ValidationError('Invalid choices')


class B(FlaskForm):
    familly = FieldList(FormField(A), validators=[DataRequired()])
    add = SubmitField('Add entry')
    submit = SubmitField('Add')


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    form = B()
    if request.method=="GET":
        form.familly.append_entry({
            'first_name': 'oualid',
            'last_name': 'ouarem',
            'b_date':datetime.utcnow().date()
        })
        return render_template("index.html", form=form, a=A())
    if form.add.data:
        form.familly.append_entry({
            'first_name': '',
            'last_name': '',
            'select_field': [('male', 'Male'), ('female', 'Female')]
        })
        return render_template("index.html", form=form, a=A())
   
    for index, entry in enumerate(form.familly):
        if entry.delete_entry.data:
            print(f'here index={index}')
            del form.familly.entries[index]
            break
    if form.validate_on_submit():
        for entry in form.familly:
            print(f'first_name:{entry.first_name.data}, last_name={entry.last_name.data}, gender={entry.select_field.data}')
    return render_template('index.html', form=form, a=A())


if __name__ == '__main__':
    app.run(debug=True)

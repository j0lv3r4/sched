from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, EqualTo


class AddPostForm(Form):
    title = TextField(
        'Title',
        [Required(message='Must provide a title')]
    )

from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

from jsonparse import jsonReader

class SamlSettings(Form):
	wantMessagesSignedState = jsonReader()
	if wantMessagesSignedState == True:
		wantMessagesSigned = BooleanField('Want Messages Signed?', default=True)
	else:
		wantMessagesSigned = BooleanField('Want Messages Signed?', default=False)
	wantAssertionsSigned = BooleanField('Want Assertions Signed?')
	signMetadata = BooleanField('Sign Metadata?')
	submit = SubmitField('Apply')

       
	print(str(wantMessagesSignedState)) 

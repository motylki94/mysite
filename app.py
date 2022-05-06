from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
# --------- Flask CKEditor  ----------
from flask_ckeditor import CKEditorField
# --------- Flask Bootstrap  ----------
from flask_bootstrap import Bootstrap
# ------- Libraries for sending Email --------
import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
# ------------- Getting password from the environmental variable ----------------
load_dotenv()

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['CSRF_ENABLED'] = True
# ---- Email settings ----
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/cv')
def cv():
    return render_template("curriculum.html")

# ----------- EMAIL FORM -----------
class EmailForm(FlaskForm):
    user_name=StringField(label='Name', validators=[DataRequired()])
    user_lastname=StringField(label='Last name', validators=[DataRequired()])
    user_email=EmailField(label='E-mail', validators=[DataRequired(), Email(message='Invalid email address.', granular_message=False, check_deliverability=True, allow_smtputf8=True, allow_empty_local=False)])
    user_message=CKEditorField(label='Message', validators=[DataRequired()])


# ------------- GMAIL API SETTINGS, SEND EMAIL --------------




# ------------- OPEN EMAIL FORM PAGE --------------
@app.route('/contact', methods=["GET","POST"])
def contact():
    form=EmailForm()
    if form.validate_on_submit():
        message_I_get = f"""
        Nadawca : {form.user_name.data} {form.user_lastname.data}
        Adres Email : {form.user_email.data}
        Wiadomość : \n\n{form.user_message.data}
        """
        msg = Message('Hey', sender=os.getenv('SENDER'), recipients=[os.getenv('RECIPIENTS')])
        msg.body = message_I_get
        mail.send(msg)
        flash('Message successfully sent.', category='success')
        return redirect(url_for('home'))



    return render_template("email.html",form=form)



if __name__ == '__main__':
    app.run()



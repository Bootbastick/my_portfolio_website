from flask import Flask, request
from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import datetime
import smtplib, ssl

port = 587
smtp_server = "smtp-mail.outlook.com"
sender_email = "sender email here"
password = "password here"
receiver_email = "receiver email"
context = ssl.create_default_context()

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "use a secret key here"


class MessageForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(message="Put your First Name here.")])
    email = StringField('Email', validators=[DataRequired(message="Put your email here.")])
    message = TextAreaField('Your Message', validators=[DataRequired(message="Please write your message.")])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html", current_year=datetime.date.today().year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = MessageForm(request.form)
    if form.validate_on_submit():
        message = f"Subject: New Message from Profile site\n\nFrom who: {form.name.data}\nTheir email: {form.email.data}\nTheir message: {form.message.data}"
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return redirect(url_for("home"))
    return render_template("contact.html", current_year=datetime.date.today().year, form=form)


if __name__ == "__main__":
    app.run(debug=True)

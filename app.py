from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

# Uncomment for SendGrid
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure random string
load_dotenv()

# Hardcoded exchange rates (1 foreign unit to NGN, approx. Sep 2025)
exchange_rates = [
    {"currency": "USD (US Dollar)", "rate": 1508},
    {"currency": "CNY (Chinese Yuan)", "rate": 215},
    {"currency": "JPY (Japanese Yen)", "rate": 10.4},
    {"currency": "KRW (South Korean Won)", "rate": 1.1},
    {"currency": "INR (Indian Rupee)", "rate": 17.2},
    {"currency": "SGD (Singapore Dollar)", "rate": 1195},
]


# Form class for contact form
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/why-partner')
def why_partner():
    return render_template('why_partner.html')


@app.route('/strategic-goals')
def strategic_goals():
    return render_template('strategic_goals.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Email content
        email_content = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        # Using smtplib with Gmail
        try:
            msg = MIMEText(email_content)
            msg['Subject'] = 'New Contact Form Submission'
            msg['From'] = os.getenv('EMAIL_ADDRESS')
            msg['To'] = 'afriktradeofficial@gmail.com'

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
                server.sendmail(msg['From'], msg['To'], msg.as_string())

            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact_success'))

        except Exception as e:
            flash(f'Error sending message: {str(e)}', 'danger')
            return redirect(url_for('contact'))

        # Uncomment for SendGrid
        # try:
        #     message = Mail(
        #         from_email=os.getenv('EMAIL_ADDRESS'),
        #         to_emails='michealoyor@gmail.com',
        #         subject='New Contact Form Submission',
        #         plain_text_content=email_content)
        #     sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        #     response = sg.send(message)
        #     flash('Your message has been sent successfully!', 'success')
        #     return redirect(url_for('contact_success'))
        # except Exception as e:
        #     flash(f'Error sending message: {str(e)}', 'danger')
        #     return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


@app.route('/contact_success')
def contact_success():
    return render_template('contact_success.html')


@app.route('/currencies')
def currencies():
    return render_template('currencies.html', rates=exchange_rates)


if __name__ == '__main__':
    app.run(debug=True)
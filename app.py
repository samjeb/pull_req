import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_mail import Message, Mail
from form import ContactForm
from datetime import datetime
import requests


app = Flask(__name__, static_folder='static', static_url_path='/static')

app.config['SECRET_KEY'] = 'c1c2951351a900f6906f857740a0a59f'


EMAIL_SENDER = 'samjebaraj'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = 'samjebaraj2197@gmail.com'
app.config['MAIL_PASSWORD'] = 'qvqbirplkoqaunew'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


EMAIL_RECIPIENT = 'samjebaraj@erssmail.com'

mail = Mail(app)

GOOGLE_RECAPTCHA_SITE_KEY = '6LfHMtomAAAAAImOfjc_YBhTzbh6PDFarc4nvt-o'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LfHMtomAAAAAJ6CjeNBSaFnDhppIddOI82uClar'

GOOGLE_RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'


@app.route('/', methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if request.method == 'GET':
        return render_template('contact.html', form=form, site_key=GOOGLE_RECAPTCHA_SITE_KEY)
    if request.method == 'POST':
        if form.validate_on_submit():
            if "g-recaptcha-response" not in request.form:
                flash(f"Captcha is missing", category='info')
                return render_template('contact.html', form=form, site_key=GOOGLE_RECAPTCHA_SITE_KEY)
                # return {"Status": "SUCCESS", "Output": "Captcha is missing"}
         
            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(
                url=f'{GOOGLE_RECAPTCHA_VERIFY_URL}?secret={GOOGLE_RECAPTCHA_SECRET_KEY}&response={secret_response}').json()

            
            if not verify_response['success'] or verify_response['score'] < 0.5:
                # abort(401)
                flash(f"Authentication error", category='info')
                return render_template('contact.html', form=form, site_key=GOOGLE_RECAPTCHA_SITE_KEY)
                # return {"Status": "ERROR", "Output": "Authentication error"}
            print(verify_response)
            
            
            today = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            message = request.form["message"]

            
            html = f"New form submission received!<br>" \
                f"<br>" \
                f"Date : {today}<br>" \
                f"Name : {name}<br>" \
                f"Email : {email}<br>" \
                f"Phone : {phone}<br>" \
                f"Message : {message}<br><br>"
                
            msg = Message(
                subject='New Contact Form Received',
                html=html,
                sender=('samjebaraj2197', app.config['MAIL_USERNAME']),
                
                recipients=[EMAIL_RECIPIENT]
            )
            mail.send(msg)
            flash(f"Your message was sent successfully", category='info')
            return render_template('contact.html', form=form, site_key=GOOGLE_RECAPTCHA_SITE_KEY)
            # return {"Status": "SUCCESS", "name": request.form["name"], "email": request.form["email"], "phone": request.form["phone"], "message": request.form["message"]}
        else:
            flash(f"Form validation error", category='info')
            return render_template('contact.html', form=form, site_key=GOOGLE_RECAPTCHA_SITE_KEY)
            # return {"Status": "ERROR", "Output": "Form validation error"}


if __name__ == "__main__":
    app.run(debug=True)
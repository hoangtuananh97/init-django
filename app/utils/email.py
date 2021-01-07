import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from app.utils import utils
from config.settings.default import SENDERNAME, RECIPIENT, CONFIGURATION_SET, HOST, PORT, USERNAME_SMTP, PASSWORD_SMTP, \
    SENDER


class CustomActionEmail(BaseEmailMessage):
    template_name = "mail/EmailActivation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["url"] = 'api/v1/user/activate/{uid}/{token}'.format(uid=utils.encode_uid(user.pk),
                                                                     token=default_token_generator.make_token(user))
        return context


class RegisterComplete(BaseEmailMessage):
    template_name = "mail/EmailRegisterSuccess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context


class SendMail(BaseEmailMessage):
    template_name = "mail/password_reset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = "api/v1/user/password-reset/{uid}/{token}".format(**context)
        return context


def send_email_ses():
    # The subject line of the email.
    SUBJECT = 'Amazon SES Test (Python smtplib)'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test\r\n"
                 "This email was sent through the Amazon SES SMTP "
                 "Interface using the Python smtplib package."
                 )

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES SMTP Email Test</h1>
      <p>This email was sent with Amazon SES using the
        <a href='https://www.python.org/'>Python</a>
        <a href='https://docs.python.org/3/library/smtplib.html'>
        smtplib</a> library.</p>
    </body>
    </html>
                """

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    # Comment or delete the next line if you are not using a configuration set
    # msg.add_header('X-SES-CONFIGURATION-SET', CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print("Error: ", e)
    else:
        print("Email sent!")

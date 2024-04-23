import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass

# Prompt the user for connection info
to_email = "kaufen@cmja.de"
servername = "smtp.cmja.de:587"
username = "zeug@cmja.de"
password = "$O4D]'Xxe]x5RmBX>.le<92\[HtpdJ"

# Create the message
msg = MIMEText('Test message from PyMOTW.')
msg.set_unixfrom('author')
msg['To'] = email.utils.formataddr(('Recipient', to_email))
msg['From'] = email.utils.formataddr(('Heizung', 'zeug@cmja.de'))
msg['Subject'] = 'Test from PyMOTW'

server = smtplib.SMTP(servername)
try:
    server.set_debuglevel(True)

    # identify ourselves, prompting server for supported features
    server.ehlo()

    # If we can encrypt this session, do it
    if server.has_extn('STARTTLS'):
        server.starttls()
        server.ehlo() # re-identify ourselves over TLS connection

    server.login(username, password)
    server.sendmail('author@example.com', [to_email], msg.as_string())
finally:
    server.quit()

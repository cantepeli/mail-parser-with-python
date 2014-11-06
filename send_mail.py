import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendMail(host,username,password,TO_MAIL,FROM_MAIL,MESSAGE):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "from surgate messaging gateway"
    msg['From'] = FROM_MAIL
    msg['To'] = TO_MAIL
    
    msg.attach(MIMEText(str(MESSAGE), 'plain'))
    #msg.attach(MIMEText(str(MESSAGE), 'html'))
    mail = smtplib.SMTP(host)
    mail.ehlo()
    mail.starttls()
    mail.login(username,password)
    mail.sendmail(FROM_MAIL, TO_MAIL, msg.as_string())
    mail.quit()
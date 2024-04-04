import smtplib

def send_mail(reciver_mail):
    from_ = "divyalokineni@gmail.com"
    to = reciver_mail
    subject = "Service Request"
    body = "Your service request has been accepted"
    msg = 'Subject: {}\n\n{}'.format(subject, body)
    pwd = 'skrsuhbwxnfndonw'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_, pwd)
    server.sendmail(from_, to, msg)
    server.close()

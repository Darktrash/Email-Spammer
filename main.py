import time
import string
import sys
import random
import smtplib
from threading import Thread
from email.mime.text import MIMEText
from loguru import logger


SMTP_SERVER = 'smtp.rambler.ru', 465
RECIPIENT = 'lol@kek'
PASSES = 5
TIME_INTERVAL = 5, 10

#Enable logging
logger.add(sys.stdout, level=0, format='{message}')


def email_spam(sender_email, sender_password):
    server = smtplib.SMTP_SSL(*SMTP_SERVER)

    for _ in range(PASSES):
        time.sleep(random.randint(*TIME_INTERVAL))

        subject = ''.join(random.choices(string.ascii_letters, k=20))
        message = ''.join(random.choices(string.printable * 10, k=500))

        msg = MIMEText(message)
        msg['Subject'] = subject

        try:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, RECIPIENT, msg.as_string())
            logger.log(0, '[@] The message was sent successfully!')
        
        except Exception as exception:
            logger.log(0, f'[!] {exception}')


def main():
    with open('email_data.txt') as file:
        email_data = dict(map(lambda x: x.split(':'), 
                              set(file.read().split())))

    for email in email_data:
        Thread(target=email_spam,
               args=(email, email_data.get(email))).start()


if __name__ == '__main__':
    main()

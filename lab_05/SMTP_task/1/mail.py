import smtplib
import argparse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


with open('xxx.txt') as f:
    MY_ADDRESS = f.readline().strip()
    MY_PASSWORD = f.readline().strip()


def send_email(to_addr: str, filename: str):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Subject"
    msg['From'] = MY_ADDRESS
    msg['To'] = to_addr

    with open(filename, 'r') as file:
        data = file.read()

    ext = filename.split('.')[-1]
    if ext == "txt":
        body = MIMEText(data, 'plain')
    elif ext == "html":
        body = MIMEText(data, 'html')
    else:
        body = MIMEText("Sorry, it is supported only txt and html formats", 'plain')

    msg.attach(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(MY_ADDRESS, MY_PASSWORD)
        server.sendmail(MY_ADDRESS, to_addr, msg.as_string())
        server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send mail')
    parser.add_argument('to_addr', type=str, help='Destination email')
    parser.add_argument('filename', type=str, help='Name of file with email text')
    args = parser.parse_args()
    send_email(args.to_addr, args.filename)
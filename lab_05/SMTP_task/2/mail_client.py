import argparse

import socket
import base64
import ssl


with open('xxx.txt') as f:
    MY_ADDRESS = f.readline().strip()
    MY_PASSWORD = f.readline().strip()


def send_email(email_from, password, email_to, subject, text_msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('smtp.gmail.com', 587))
    client.recv(1024)

    # start
    hello_cmd = 'HELO Alice\r\n'.encode()
    client.send(hello_cmd)
    client.recv(1024)

    start_tls_cmd = "STARTTLS\r\n".encode()
    client.send(start_tls_cmd)
    client.recv(1024)

    ssl_client = ssl.wrap_socket(client)
    secret_email_from = base64.b64encode(email_from.encode())
    secret_password = base64.b64encode(password.encode())

    # authorization
    auth_cmd = "AUTH LOGIN\r\n"
    ssl_client.send(auth_cmd.encode())
    ssl_client.recv(1024)
    ssl_client.send(secret_email_from + "\r\n".encode())
    ssl_client.recv(1024)
    ssl_client.send(secret_password + "\r\n".encode())
    ssl_client.recv(1024)

    # sender and receiver email addresses
    mail_from = "MAIL FROM: <{}>\r\n".format(email_from)
    ssl_client.send(mail_from.encode())
    ssl_client.recv(1024)
    mail_to = "RCPT TO: <{}>\r\n".format(email_to)
    ssl_client.send(mail_to.encode())
    ssl_client.recv(1024)

    # email content
    data = 'DATA\r\n'
    ssl_client.send(data.encode())
    ssl_client.recv(1024)
    msg = '{}. \r\n'.format(text_msg)
    end_msg = '\r\n.\r\n'
    ssl_client.send('Subject: {}\n\n{}'.format(subject, msg).encode())
    ssl_client.send(end_msg.encode())
    ssl_client.recv(1024)

    # end
    quit_cmd = 'QUIT\r\n'
    ssl_client.send(quit_cmd.encode())
    ssl_client.recv(1024)
    ssl_client.close()
    print('Your email was sent!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mail client')
    parser.add_argument('to_addr', type=str, help='Destination email')
    parser.add_argument('subject', type=str, help='Email subject')
    parser.add_argument('msg_txt', type=str, help='Email text')
    args = parser.parse_args()
    send_email(MY_ADDRESS, MY_PASSWORD, args.to_addr, args.subject, args.msg_txt)

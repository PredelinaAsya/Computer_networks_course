import socket
import argparse


def get_input_args():
    parser = argparse.ArgumentParser(description='Server client')
    parser.add_argument('--host', metavar='host', type=str, nargs='?')
    parser.add_argument('--port', metavar='port', type=int, nargs='?')
    parser.add_argument('--input_filename', metavar='input_filename', type=str, nargs='?', default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_input_args()
    print(f'Start connection to server: {args.host} on port: {args.port}')

    client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_server.connect((args.host, args.port))
        print('Success')
    except Exception as e:
        print(f'Failed connection to host: {args.host} on port: {args.port}, error: {e}')

    request_str = 'GET /' + args.input_filename + ' HTTP/1.1'
    request = request_str.encode('utf-8')
    client_server.send(request)
    request_data = client_server.recv(1024)
    print(f"Response is:\n {request_data.decode('utf-8')}")

import socket

SERVER_PORT = 2048


def load_file_data(request_data):
    HDRS_200 = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = f"./server_files{request_data.split(' ')[1]}"
    print(f'input file path: {path}')
    response = ''
    try:
        with open(path, 'rb') as file:
            response = file.read()
        return HDRS_200.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Page not found').encode('utf-8')


def start_single_threaded_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', SERVER_PORT))
        server_socket.listen(1)
        print('The server is ready to receive request...')
        while True:
            client_socket, address = server_socket.accept()
            request_data = client_socket.recv(1024).decode('utf-8')
            content = load_file_data(request_data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == '__main__':
    start_single_threaded_server()

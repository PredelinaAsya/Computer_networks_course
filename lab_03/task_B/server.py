import socket
from threading import Thread


SERVER_PORT = 2048


def client_process(client_socket, connection):
    ip = connection[0]
    port = connection[1]
    print(f'New client has IP: {ip} and port: {port}')
    request_data = client_socket.recv(1024).decode('utf-8')
    content = load_file_data(request_data)
    client_socket.send(content)
    client_socket.close()
    

def load_file_data(request_data):
    HDRS_200 = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = f"./server_files{request_data.split(' ')[1]}"
    print(f'Input file path: {path}')
    response = ''
    try:
        with open(path, 'rb') as file:
            response = file.read()
        return HDRS_200.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Page not found').encode('utf-8')


def start_multi_threaded_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('', SERVER_PORT))
        server_socket.listen(1)
        print('The server is ready to receive requests...')
        while True:
            client_socket, address = server_socket.accept()
            new_thread = Thread(target=client_process, args=(client_socket, address))
            new_thread.start()
    except KeyboardInterrupt:
        print(f'Close server connection')
        server_socket.close()


if __name__ == '__main__':
    start_multi_threaded_server()

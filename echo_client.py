import socket
import sys

BUFF_SIZE = 16

def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    sock = socket.socket()

    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    sock.connect(server_address)

    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.send(msg.encode('utf8'))

        while True:
            chunk = sock.recv(BUFF_SIZE)
            received_message += chunk.decode('utf8')
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

            if len(chunk) < BUFF_SIZE:
                break
    finally:
        print('closing socket', file=log_buffer)
        sock.close()
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    returned_message = client(msg)
    print("Message returned from server is '{}'".format(returned_message))

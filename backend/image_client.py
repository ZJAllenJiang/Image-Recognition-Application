import socket
import os
import sys
import struct

# set function to make client connected to server
def image_client():
    while True:
        try:
            # client connects to the server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # get server ip
            s.connect(('128.163.233.42', 58005))

        except socket.error as msg:
            print(msg)
            print(sys.exit(1))

        filepath = input('Please input the image file:')

        # preprocess input image and fit for transmission
        processed_file = struct.pack(b'128sq', bytes(os.path.basename(
            filepath), encoding='utf-8'), os.stat(filepath).st_size)
        s.send(processed_file)

        fp = open(filepath, 'rb')
        while True:
            data = fp.read(1024)
            if not data:
                print('{0} sent.'.format(filepath))
                break
            s.send(data)
        s.close()


if __name__ == '__main__':
    image_client()

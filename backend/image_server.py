import socket
import os
import sys
import struct

import api

# define function used to accept connection


def image_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind server ip addr
        s.bind(('', 58005))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection.")

    while True:
        sock, addr = s.accept()
        prediction = handle_image(sock, addr)
        # return result to the client and close socket
        print(prediction)

# define function used to handle transmitted image


def handle_image(sock, addr):
    print("Accept connection from {0}".format(addr))
    pred_list = []
    while True:
        fileinfo_size = struct.calcsize('128sq')
        buf = sock.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.decode().strip('\x00')
            new_filename = os.path.join('./', 'new_' + fn)
            if('jpg' in fn.lower() or 'jpeg' in fn.lower() or 'png' in fn.lower()):
                pass
            else:
                error_msg = "Please submit an image file."
                sock.send(error_msg.encode())
                sock.close()
                break
            # print(type(new_filename))
            # print(new_filename[2:])
            recvd_size = 0
            fp = open(new_filename, 'wb')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = sock.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock.recv(1024)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            file_list = []
            file_list.append(new_filename[2:])
            pred_list = api.recognize(file_list)
            for result in pred_list:
                sock.send(result.encode())
            os.remove(new_filename)
        sock.close()
        if len(pred_list) != 0:
            return pred_list
        break


if __name__ == '__main__':
    image_server()

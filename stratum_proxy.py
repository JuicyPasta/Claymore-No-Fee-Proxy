#!/usr/bin/python2.7

import sys
import socket
import threading
import json
from collections import OrderedDict
import binascii
import datetime
import time


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    # create the server object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # lets see if we can stand up the server
    try:
        print "Daemon is launched, do not close this windows"
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions"
        sys.exit(0)

    # listen with 5 backlogged--queued--connections
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local connection information
        print"[+] Received incomming connections from %s:%d" % (addr[0], addr[1])

        # start a new thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.daemon = False

        proxy_thread.start()


def receive_from(connection):

    buffer = ""

    # We set a 2 second time out depending on your
    # target this may need to be adjusted
    connection.settimeout(0)

    try:
        # keep reading into the buffer until there's no more data
        # or we time out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass

    return buffer


# modify any requests destined for the remote host
def request_handler(socket_buffer):
    worker_name = '0xfeE03fB214Dc0EeDc925687D3DC9cdaa1260e7EF'

    if 'submitLogin' in socket_buffer:
        json_data = json.loads(socket_buffer, object_pairs_hook=OrderedDict)
        print('[+] Auth in progress with address: ' + json_data['params'][0])
        if worker_name not in json_data['params'][0]:
             print('[*] DevFee Detected - Replacing Address - ' + str(datetime.datetime.now()))
             print('[*] OLD: ' + json_data['params'][0])
             json_data['params'][0] = worker_name + '/rekt'
             print('[*] NEW: ' + json_data['params'][0])

        socket_buffer = json.dumps(json_data) + '\n'

    return socket_buffer



# modify any responses destined for the local host
def response_handler(buffer):
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to our local client send it
        if len(remote_buffer):
            #print "[<==] Sending %d bytes to localhost. #A"
            client_socket.send(remote_buffer)


    # now let's loop and reading from local, send to remote, send to local
    # rinse wash repeat
    while True:

        # read from local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            #print "[==>] Received bytes from localhost. #B" + str(datetime.datetime.now())

            # send it to our request handler
            local_buffer = request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            #print "[==>] Sent to remote. #C" + str(datetime.datetime.now())
            time.sleep(0.01)
			
        # receive back the response
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            #print "[<==] Received bytes from remote. #D" + str(datetime.datetime.now())

            # send to our response handler
            remote_buffer = response_handler(remote_buffer)

            # send the response to the local socket
            try:
                 client_socket.send(remote_buffer)
            except:
                 print('[-] Auth Disconnected - Ending Devfee or stopping mining - ' + str(datetime.datetime.now()))
                 break

            #print "[<==] Sent to localhost. #E" + str(datetime.datetime.now())
            time.sleep(0.1)
        time.sleep(0.01)


def main():
    # cursory check of command line args
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [reveive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.11.132.1 9000 True"
        sys.exit(0)

    # set up listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # set up remote targets
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # this tells our proxy to connect and receive data before sending to the remote host
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # now spin up our listening socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()

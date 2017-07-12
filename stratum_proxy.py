#!/usr/bin/python2.7

import sys
import socket
import threading
import json
from collections import OrderedDict
import binascii
import datetime
import time


def server_loop(local_host, local_port, remote_host, remote_port):
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
                                        args=(client_socket, remote_host, remote_port))
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
    #Here is the good part

    #If it is an Auth packet
    if ('submitLogin' in socket_buffer) or ('eth_login' in socket_buffer):
        json_data = json.loads(socket_buffer, object_pairs_hook=OrderedDict)
        print('[+] Auth in progress with address: ' + json_data['params'][0])
        #If the auth contain an other address than our
        if wallet not in json_data['params'][0]:
             print('[*] DevFee Detected - Replacing Address - ' + str(datetime.datetime.now()))
             print('[*] OLD: ' + json_data['params'][0])
             #We replace the address
             json_data['params'][0] = wallet + worker_name
             print('[*] NEW: ' + json_data['params'][0])

        socket_buffer = json.dumps(json_data) + '\n'
        
    #Packet is forged, ready to send.
    return socket_buffer



# modify any responses destined for the local host
def response_handler(buffer):
    return buffer


def proxy_handler(client_socket, remote_host, remote_port):
    # We prepare the connection
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # We will try to connect to the remote pool
    for attempt_pool in range(3):
        try:
            remote_socket.connect((remote_host, remote_port))
        except:
            print "[!] Impossible to connect to the pool. Try again in few seconds "
            time.sleep(2)
        else:
            # Connection OK
            break
    else:
        print "[!] Impossible initiate connection to the pool. Claymore should reconnect. (Check your internet connection) "+ str(datetime.datetime.now())
        
        #Closing connection
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        
        #Exiting Thread
        sys.exit()
        

    # now let's loop and reading from local, send to remote, send to local
    # rinse wash repeat
    while True:

        # read from local host
        local_buffer = receive_from(client_socket)
        
        if len(local_buffer):

            # send it to our request handler
            local_buffer = request_handler(local_buffer)
            
            #print local_buffer
            
            # Try to send off the data to the remote pool
            try:
                remote_socket.send(local_buffer)
            except:
                print "[!] Sending packets to pool failed."
                time.sleep(0.02)
                print "[!] Connection with pool lost. Claymore should reconnect. (May be temporary) "+ str(datetime.datetime.now())
                #Closing connection
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                #Exiting loop
                break
                
            # Adding delay to avoid too much CPU Usage
            time.sleep(0.001)

        # receive back the response
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            
            # send to our response handler
            remote_buffer = response_handler(remote_buffer)
            
            #print local_buffer
            
            # Try to send the response to the local socket
            try:
                 client_socket.send(remote_buffer)
            except:
                 print('[-] Auth Disconnected - Ending Devfee or stopping mining - ' + str(datetime.datetime.now()))
                 client_socket.close()
                 break

            # Adding delay to avoid too much CPU Usage
            time.sleep(0.001)
        time.sleep(0.001)
        
    #Clean exit if we break the loop
    sys.exit()


def main():
    # cursory check of command line args
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [ETH Wallet]"
        print "Example: ./proxy.py 127.0.0.1 9000 eth.realpool.org 9000 0x..."
        sys.exit(0)

    # set up listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # set up remote targets
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # Set the wallet
    global wallet 
    wallet = sys.argv[5]
    
    global worker_name
    worker_name = 'rekt'
    
    #Uncomment if you meet issue with pool or worker name - This will disable the worker name
    #worker_name = ''
    
    pool_slash = ['nanopool.org','dwarfpool.com']
    pool_dot = ['ethpool.org','ethermine.org','alpereum.ch']
    if worker_name:
        if any(s in remote_host for s in pool_slash):
            worker_name = '/' + worker_name
        elif any(d in remote_host for d in pool_dot):
            worker_name = '.' + worker_name
        else:
            #No worker name for compatbility reason
            print "Unknown pool - Worker name is empty"
            worker_name = ''

    print "Wallet set: " + wallet + worker_name

    # now spin up our listening socket
    server_loop(local_host, local_port, remote_host, remote_port)


if __name__ == "__main__":
    main()

# -*- coding: latin-1 -*-
# Adapted from something by Jean-Paul by shane
# Copyright (C) AB Strakt
# Copyright (C) Jean-Paul Calderone
# See LICENSE for details.

"""
Simple SSL client, using blocking I/O
"""

from OpenSSL import SSL
import sys, os, select, socket

def verify_cb(conn, cert, errnum, depth, ok):
    # This obviously has to be updated
    print( 'Got certificate: %s' % cert.get_subject())
    #don't ever do this in production.
    #this force verifies all certs.
    return 1

print(sys.argv)
if len(sys.argv) < 3:
    print( 'Usage: python[2] client.py HOST PORT')
    sys.exit(1)

# Initialize context
ctx = SSL.Context(SSL.SSLv23_METHOD)
#you must choose to verify the peer to get
#the verify callbacks called
ctx.set_verify(SSL.VERIFY_PEER, verify_cb)

# Set up client
sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
sock.connect((sys.argv[1], int(sys.argv[2])))
#send a simple http request
sock.send("""GET / HTTP/1.0 Host: www.google.com """.replace("\n","\r\n"))


while True:
    try:
        buf = sock.recv(4096)
    except SSL.SysCallError:
        break
    if not buf:
        break
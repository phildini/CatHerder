from fabric.api import *
import os
import paramiko
import socket

env.user=['root']

env.warn_only=True

# Code to read env.hosts[] from a file
filename = 'hosts'
try:
    fhosts = open(filename)
except IOError:
    abort('file not found: %s' % filename)

def has_data(line):
    """'line' is not commented out and not just whitespace."""
    return line.strip() and not line.startswith('#')

env.hosts = [line.strip() for line in fhosts if has_data(line)]
    
# Return host type of all hosts
def host_type():
    if _is_host_up(env.host, int(env.port)) is True:
        run('uname -s')

# Shutdown all hosts
def shutdown():
    run('shutdown -h now')

# Copy local SSH-RSA key to all hosts
def key_copy():
    if _is_host_up(env.host, int(env.port)) is True:
        key = open('/Users/phildini/.ssh/id_rsa.pub')
        put(key, 'key')
        run('cat key >> .ssh/authorized_keys')

# Test whether hosts are up by returning TCP banner on port 22
def is_up():
    #print env.host
    command = 'echo "" | nc -v -n -w1 '+ env.host +' 22'
    local(command)

# Test each host to see if its reachable.        
def _is_host_up(host, port):
    # Set the timeout
    original_timeout = socket.getdefaulttimeout()
    new_timeout = 3
    socket.setdefaulttimeout(new_timeout)
    host_status = False
    try:
        transport = paramiko.Transport((host, port))
        host_status = True
    except:
        print('***Warning*** Host {host} on port {port} is down.'.format(
            host=host, port=port)
        )
    socket.setdefaulttimeout(original_timeout)
    return host_status

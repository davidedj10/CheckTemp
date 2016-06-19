import xbmcaddon
import socket
import commands
import subprocess
 

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', 8080))
listen_socket.listen(1)

print 'Serving HTTP on port %s ...' % 8080
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    
    p = subprocess.Popen("cat /sys/class/thermal/thermal_zone0/temp", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    
    print request

    http_response = """\
HTTP/1.1 200 OK

""" + output

    client_connection.sendall(http_response)
    client_connection.close()
 

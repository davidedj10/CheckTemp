import xbmcaddon
import socket
import commands
import subprocess


def httpresp():

    httpresponse = """\
HTTP/1.1 200 OK

"""
    return(httpresponse)

def cpusage():

    usg = commands.getstatusoutput("top -bn1 | awk 'FNR == 2 {print $2}'")
    
    value = usg[1]

    return(str(value))


def coretemp():

    rawtemp = commands.getstatusoutput("cat /sys/class/thermal/thermal_zone0/temp")

    temp = rawtemp[1]

    return(str(temp))

def corevolts(): 

    rawcorevolts = commands.getstatusoutput("vcgencmd measure_volts core | awk '{print substr($1, 6, 6)}'")

    corevolts = rawcorevolts[1]

    return(str(corevolts))

def coreclock():

    rawcoreclock = commands.getstatusoutput("vcgencmd measure_clock arm | awk '{print substr($1, 15)}'")

    coreclock = rawcoreclock[1]

    return(str(coreclock))

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', 8080))
listen_socket.listen(1)

print 'Serving HTTP on port %s ...' % 8080
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)

    print request

    http_response = httpresp() + coretemp() + "\n" + corevolts() + "\n" + coreclock() + "\n" + cpusage()

    client_connection.sendall(http_response)
    client_connection.close()
 


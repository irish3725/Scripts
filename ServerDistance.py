#/urs/bin/python3/


import subprocess
import re
import os 
import sys 
import json 
import math 
 
##  For converting long and lat to radians
#   @param degrees_L is list of (long,lat)
def degreesToRadians(degrees):
    radians = [0,0] 
    radians[0] = degrees[0] * math.pi / 180 
    radians[1] = degrees[1] * math.pi / 180 
    return radians

##  For getting distance between two points on sphere
#   @param coordinates_L  both sets of coordinates as list of lists 
def getDistance(coordinates_L):
    # distance between points
    d = None
    # radius of the Earth
    r = 3959 
    # latitudes and longitudes
    lat_1 = coordinates_L[0][0]
    lon_1 = coordinates_L[0][1]
    lat_2 = coordinates_L[1][0]
    lon_2 = coordinates_L[1][1] 

    # distance over sphere using haversine function
    term_1 = math.pow(math.sin((lat_2 - lat_1)/2), 2)
    term_2 = math.pow(math.cos(lat_1) * math.cos(lat_2) * math.sin((lon_2 - lon_1)/2), 2)
    d = 2 * r * math.asin(math.sqrt(term_1 + term_2))
    
    return d 

def findDistance(address):
    # possible dns servers to querie 
    dns_L = ['8.8.8.8', '9.9.9.9']

    # gets route to server from traceroute
    route_S = subprocess.check_output(['traceroute', address])

    # print route
#    print(route_S, '\n\n')

    # grab (mostly) ips from traceroute output
    ip_list_L = re.findall(r'\d+.\d+.\d+.\d+', str(route_S))

    # create dictionary for ip's and their gps coordinates
    ip_location_D = dict()

    # delete end ip from beginning of list
    del ip_list_L[0]

    # print path ip addresses in order
#    print('IPs:', ip_list_L, '\n\n')

    # for silincing subprocess
    FNULL = open(os.devnull, 'w')

    # for each ip in list, get long and lat
    for ip in ip_list_L:
        get_location_S = 'ip-api.com/json/' + ip
        subprocess.call(['wget',get_location_S], stdout=FNULL, stderr=subprocess.STDOUT) 
        f = open(ip, 'r')
        htmlText = "\n".join(f.readlines())
        ip_stuff_D = json.loads(htmlText)
        f.close()
#        print(htmlText)
        subprocess.call(['rm', ip])
        if ip_stuff_D.items():
            # try except for address that are invalid ip's
            # that we got from poor use of re
            try:
                ip_location_D[ip] = (float(ip_stuff_D["lat"]), float(ip_stuff_D["lon"])) 
    #            print('ip_location_D[ip] =', ip, ':', ip_location_D[ip])
    #            print('IP: %s at (%s,%s)' % (ip, ip_stuff_D["lat"], ip_stuff_D["lon"])) 
            except:
                pass

    # create list of coordinates to get distance between
    coordinates_L = list() 
    # create final distance to add on to in every iteration
    final_distance = 0
    for ip in ip_location_D.keys():
        # if this is the first coordinate
        if not coordinates_L:
            coordinates_L = [None, None] 
            print('coordinates for', ip, ':', ip_location_D[ip]) 
            coordinates_L[1] = degreesToRadians(ip_location_D[ip])
        # if we have more than one coordinate to look at, get distance
        else:
            print('coordinates for', ip, ':', ip_location_D[ip]) 
            coordinates_L[0] = coordinates_L[1]
            coordinates_L[1] = degreesToRadians(ip_location_D[ip])
            final_distance = final_distance + getDistance(coordinates_L) 
            print('new distance:', final_distance)
    print('Final distance between here and Server for %s is %d miles.' % (address, final_distance))

def main():

    # if no arguments, set default address to look at to facebook.com
    if len(sys.argv) == 1:
        address = 'facebook.com'
        print('Finding Distance between this computer and server for %s' % address)
        findDistance(address)
    # if arguments, iterate through each one
    else:
        for i in range(1, len(sys.argv)):   
            address = sys.argv[i]
            print('Finding Distance between this computer and server for %s' % address)
            try:
                findDistance(address)             
            except:
                print('Could not find %s' % address) 
            print()

if __name__ == '__main__':
    main()


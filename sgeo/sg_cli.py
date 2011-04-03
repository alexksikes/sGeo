#! /usr/bin/env python

"""Usage: 

python sg_cli.py [options] place_name'
    
Description:' 
    Use to test and debug sgeo at the command line.'
    
    Options:' 
        -l, --limit  int            : (default is 1)'
        --usa                       : USA geocoding only'
        --nearby  int               : show top nearby places on geonames'
        --listen  host:port         : address to searchd (default localhost:9312)'
        -h, --help                  : this help message'
        
Email bugs/suggestions to Alex Ksikes (alex.ksikes@gmail.com)""" 

import config
import fsphinx
import getopt
import sgeo
import sys

def run(place, listen='', usa=False, limit=1, nearby=0):
    gc = sgeo.GeoCoder(listen=listen, usa_only=usa)
    center = gc.get_locations(place, limit=limit)
    print center
    
    hits = gc.get_hits()
    print 'Found the following locations:'
    print hits
    
    if center and nearby:
        query = '%s %s' % (center.get('state_code'), center.get('country_code'))  
        hits = sgeo.get_nearby_places(center.lat, center.lon, query, exclude=True, limit=nearby)        
        print 'And %s nearby places to "%s, %s" on geonames:' % (hits.total, center.place, center.state_code)
        print hits
        
def usage():
    print >> sys.stderr, __doc__

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ul:x:n:h', 
            ['usa', 'limit=', 'listen=', 'nearby=', 'help'])
    except getopt.GetoptError:
        usage(); sys.exit(2)
    
    listen = 'localhost:9312'
    decode = usa = False
    offset = 0
    limit = 1
    nearby = 0
    for o, a in opts:
        if o in ('-u', '--usa'):
            usa = True
        elif o in ('-l', '--limit'):
            limit = int(a)
        elif o in ('--listen'):
            listen = a
        elif o in ('--nearby'):
            nearby = int(a)
        elif o in ('-h', '--help'):
            usage(); sys.exit()
    
    if len(sys.argv) < 2:
        usage()
    else:
        run(sys.argv[-1], listen, usa, limit, nearby)

if __name__ == "__main__":
    main()
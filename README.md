sGeo
====

1. About
--------

sGeo is a very simple minimalistic geocoder built around [Geonames](http://www.geonames.org/), [zip-codes.com](http://www.zip-codes.com/) and [Sphinx](http://sphinxsearch.com/). You can try to geocode any place in the world or just restrict it to US cities and zip codes. sGeo will not geocode full addresses as they are not available in Geonames. It will only geocode cities, zip codes or places such as national parks, universities, etc ... sGeo was first written in late 2007 to batch geocode the contractor database used in [Chiefmall](http://www.chiefmall.com). 

Feel free to try a [demo](http://sgeo.ksikes.net).

2. Installation
---------------

Read [INSTALL.md](https://github.com/alexksikes/sGeo/blob/master/INSTALL.md) for installation instructions.

3. How to use within your code
------------------------------

    import sgeo
    gc = sgeo.GeoCoder(usa_only=True)
    
    # querying Geonames
    location = 'Newport Beach, CA'
    coords = gc.get_locations(location, limit=5)
    
    # using MaxMind GeoIP
    location = '64.233.160.0'
    coords = gc.get_locations(location)
    
    # using zip-codes.com
    location = '94720'
    coords = gc.get_locations(location)
    
    # using Geonames to find nearby hotels
    hits = gc.get_nearby_places(coords.lat, coords.lon, 'hotels', radius=50*1000, limit=10)
    print hits
    
4. Use command line interface for testing
-----------------------------------------

    python sgeo/sgeo/sg_cli.py --usa-only 'Newport Beach, CA'
    
    Usage:

    python sg_cli.py [options] place_name'

    Description:'
        Use to test and debug sGeo at the command line.'

        Options:'
            -l, --limit  int            : (default is 1)'
            --usa                       : USA geocoding only'
            --nearby  int               : show top nearby places on geonames'
            --listen  host:port         : address to searchd (default localhost:9312)'
            -h, --help                  : this help message'

NOTE: The current directory '.' refers to sgeo/sgeo.

1. Download and extract the latest tar ball
===========================================

    wget http://github.com/alexksikes/sgeo/tarball/master; tar xvzf "the tar ball";

2. Download geo data
====================

* [Geonames](http://download.geonames.org/export/dump/)
* [Zip Codes](http://www.zip-codes.com), purchase a license (~$40) 
* [GeoIP](http://www.maxmind.com/app/geolitecity), get the light version or purchase pro

NOTE: GeoIP is optional.
NOTE: You may want to download Geonames to ./data/geonames and zip-codes to ./data/zipcodesdotcom. 
NOTE: Because Geonames has unprecise zip code geo-information, we had to use of zip-codes.com.

3. Setup and populate your database 
===================================

Create the databases:

    mysql -pe 'create database geonames character set utf8; create database zipcodesdotcom;'</pre>
            
Setup data to be populated:

    Read comments in populate.sql, setup the appropriate paths and perform the formatting.
        
Create the required tables and load the data:

    mysql -p geonames < ./sql/geonames.sql
    mysql -p geonames < ./sql/geonames_more.sql
    mysql -p geonames < ./sql/geonames_postals.sql
    mysql -p zipcodesdotcom < ./sql/zipcodesdotcom.sql

4. Download and install dependecies
===================================

* [Sphinx](http://sphinxsearch.com/downloads/), the search engine
* [webpy](http://webpy.org/download), for the web interface and other tools
* [fsphinx](http://github.com/alexksikes/fsphinx/tarball/master), easy faceted search for sphinx and more
* [GeoIP](http://www.maxmind.com/app/python), IP geolocation (optional)
    
5. Setup Sphinx
================

Go over: 

    ./config/indexer_example.conf and make sure to rename it config/indexer.conf.

Create Sphinx index:

    /path-to-sphinx-bin/indexer -c ./config/indexer.conf --all

Serve Sphinx index:

    /path-to-sphinx-bin/searchd -c ./config/indexer.conf

NOTE: You should run these commands in sgeo/sgeo if you haven't changed your paths in indexer.conf.

7. Further configurations
=========================
    
Go over: 

    ./config/__init__example.py and make sure to rename it __init__.py.

Add sgeo to your PYTHONPATH

8. You're done!
===============

in your code:

    import sgeo
    gc = sgeo.GeoCoder(usa_only=usa)
    sgeo.get_locations('Newport Beach, CA')

or use command line interface to test:

    python sgi.py 'Newport Beach, CA'

Check out the file geo.py for the full API.
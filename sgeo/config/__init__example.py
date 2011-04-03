import web

# connect to database
db = web.database(dbn='mysql', db='geonames', user='user', passwd='passwd')

# show output of mysql statements
db.printing = False

# path to the geoIP library
#geoIP_path = "/usr/local/share/geoip/GeoLiteCity.dat"
geoIP_path = "/usr/local/share/geoip/GeoIPCity.dat"

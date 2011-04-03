import fsphinx
import math
import new
import re
import web

from config.geocoders import geonames_P_US
from config.geocoders import zipcodes_US
from config.geocoders import geonames
from config.geocoders import geonames_postals
from config import nearby_places

try:
    import GeoIP
    from config import geoIP_path
except '':
    GeoIP = None

__all__ = ['GeoCoder', 'get_nearby_places',
           'is_zip_code', 'is_ip_address', 'get_coords_from_ip',
           'radian_to_degree', 'degree_to_radian']

RADIUS = 25 * 1000

class GeoCoder(object):
    def __init__(self, listen='', usa_only=False):
        def make_client(config):
            return fsphinx.make_client_from_config(config)
        if usa_only:
            self.cl_place = make_client(geonames_P_US)
            self.cl_zip = make_client(zipcodes_US)
        else:
            self.cl_place = make_client(geonames)
            self.cl_zip = make_client(geonames_postals)
        if listen:
            self._set_searchd(listen)
        self._hits = fsphinx.Hits()
        
    def _set_searchd(self, listen):
        addr, port = listen.split(':') 
        for cl in [self.cl_zip, self.cl_place]:
            cl.SetServer(addr, int(port))
    
    def _set_limits(self, offset, limit):
        for cl in [self.cl_zip, self.cl_place]:
            cl.SetLimits(offset, limit)
        
    def get_locations(self, q, offset=0, limit=1):
        self._set_limits(offset, limit)
        
        zip_code = is_zip_code(q)
        ip_address = is_ip_address(q)
        if zip_code:
            hits = self.cl_zip.Query(q)
        elif ip_address:
            hits = self.get_hits_from_ip(ip_address)
        else:
            hits = self.cl_place.Query(q)
        
        self._hits = hits
        return self._coords(hits)
    
    def get_hits(self):
        return self._hits
    
    def get_hits_from_ip(self, ip):
        coords = get_coords_from_ip(ip)
        if coords:
            return fsphinx.Hits(dict(total=1, total_found=1, 
                matches=[{'@hit':coords, 'id':0, 'weight':0, 'attrs':{}}]))
        else:
            return fsphinx.Hits()
            
    def _coords(self, hits):
        if hits and hits['matches']:
            return hits['matches'][0]['@hit']

def set_location(cl, lat, lon, radius=RADIUS, exclude=False):
    cl.SetGeoAnchor('lat', 'lon', lat, lon)
    cl.SetFilterFloatRange('@geodist', 0.0, float(radius))
    if exclude:
        cl.SetFilterFloatRange('@geodist', 0.0, 0.0, exclude=True)
    
def get_nearby_places(lat, lon, query, radius=RADIUS, exclude=False, offset=0, limit=10):        
    cl = fsphinx.make_client_from_config(nearby_places)
    cl.SetLimits(offset, limit)
    set_location(cl, lat, lon, radius, exclude)
    return cl.Query(query)

#class GeoQuery(fsphinx.ParsedQuery):
#    _reserved = ['address', 'lat', 'lon']
#    
#    def __init__(self, query):
#        fsphinx.ParsedQuery.__init__(self, query)
#        self.address = self.get_term('address')
#        self.lat = float(self.get_term('lat', 0))
#        self.lon = float(self.get_term('lon', 0))
#    
#    @property
#    def sphinx_query(self):
#        s = [q.sphinx_query for q in self if q.field not in GeoQuery._reserved]
#        return ' '.join(s).strip()
    
def is_zip_code(zip):
    m = re.search('\s*(\d{5}(?:[\-]\d{4})?)\s*', zip, re.I)
    if m:
        return m.group(1)

def is_ip_address(ip):
    m = re.search('\s*((?:\d{1,3}\.){3}\d{1,3})\s*', ip, re.I)
    if m:
        return m.group(1)

def get_coords_from_ip(ip):
    gi = GeoIP.open(geoIP_path, GeoIP.GEOIP_STANDARD)
    try:
        coords = web.storage(gi.record_by_addr(ip))
        coords.lat = degree_to_radian(coords.pop('latitude'))
        coords.lon = degree_to_radian(coords.pop('longitude'))
        coords.place = coords.pop('city')
        coords.state = coords.pop('region')
        coords.state_code = coords.state
        coords.country = coords.pop('country_name')
        return coords
    except:
        pass
    
def radian_to_degree(coord):
    return coord/math.pi*180

def degree_to_radian(coord):
    return coord*math.pi/180

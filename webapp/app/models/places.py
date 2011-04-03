import web
import fsphinx
import sgeo

RADIUS = 25 * 1000

def add_to_recent_queries(query):
    get_recent_queries().insert(0, query)
    
def get_recent_queries(max_size=6):
    def uniq(seq):
        checked = []
        for e in seq:
            if e not in checked:
                checked.append(e)
        return checked
    
    if not web.config.has_key('recents'):
        web.config.recents = []
    web.config.recents = uniq(web.config.recents)[:max_size]
    return web.config.recents

def get_nearby(place, usa_only=False, offset=0, limit=10):
    gc = sgeo.GeoCoder(usa_only=usa_only)
    center = gc.get_locations(place)
    center_hits = gc.get_hits()
    
    if center:
        query = '%s %s' % (center.get('state_code'), center.get('country_code'))  
        nearby_hits = sgeo.get_nearby_places(center.lat, center.lon, query, 
            exclude=True, offset=offset, limit=limit)        
    else:
        nearby_hits = fsphinx.Hits()
        
    add_to_recent_queries(place)
    return place, center_hits, nearby_hits
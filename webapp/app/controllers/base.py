import web
import config

from app.models import places
from app.helpers import paging

from config import view

import sgeo
    
MAX_NEARBY_RESULTS = 100
WINDOW_SIZE = 1
    
class index:
    def GET(self):
        location = web.ctx.get('ip')
        if not sgeo.get_coords_from_ip(location):
            location = 'Palo Alto, CA'
        
        raise web.seeother('/search?q=%s' % location)    
        
class search:
    def GET(self):
        i = web.input(q='', s=0, usa=False)
        if not i.q:
            raise web.seeother('/')
        
        place_query, center_hits, nearby_hits = places.get_nearby(i.q, usa_only=i.usa, 
            offset=int(i.s), limit=MAX_NEARBY_RESULTS)
        pager = paging.get_paging(int(i.s), nearby_hits['total'], 
            results_per_page=MAX_NEARBY_RESULTS, window_size=WINDOW_SIZE)
        recent_queries = places.get_recent_queries()
        
        return view.layout(view.search(place_query, center_hits, nearby_hits, pager, recent_queries))

import fsphinx
import sphinxapi

from sgeo.config import db

# create sphinx client
cl = fsphinx.FSphinxClient()

# connect to searchd
cl.SetServer('localhost', 9312)

# matching mode (faceted client must be SPH_MATCH_EXTENDED2)
cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)

# sorting and possible custom sorting function
cl.SetSortMode(sphinxapi.SPH_SORT_EXTENDED, '@relevance desc')

# some fields could matter more than others
cl.SetFieldWeights(dict(postal_code=40))

# sql query to fetch the hits
db_fetch = fsphinx.DBFetch(db, sql = '''
select
    id,
    "geonames.postals" as source_db,
    postal_code,
    place_name as place,
    admin2 as county,
    admin1 as state_code,
    admin1_name as state,
    p.iso as country_code,
    latitude*PI()/180 as lat,
    longitude*PI()/180 as lon,
    c.country
from postals as p
left join country_info as c on
    p.iso=c.iso
where id in ($id)
order by field(id, $id)'''
)
cl.AttachDBFetch(db_fetch)

# by default only this index will be queried
cl.SetDefaultIndex('geonames_postals')
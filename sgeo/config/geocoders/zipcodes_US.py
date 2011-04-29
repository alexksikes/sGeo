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

## sql query to fetch the hits
db_fetch = fsphinx.DBFetch(db, sql = '''
select 
    id,
    "zipcodesdotcom" as source_db,
    ZipCode as zip,
    City as place, 
    State as state, 
    State as state_code, 
    'United States' as country,
    'us' as country_code,
    Latitude*PI()/180 as lat,
    Longitude*PI()/180 as lon
from zipcodesdotcom.zipcodes
where id in ($id)
order by field(id, $id)'''
)
cl.AttachDBFetch(db_fetch)

# by default only this index will be queried
cl.SetDefaultIndex('zipcodes_US')
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
cl.SetSortMode(sphinxapi.SPH_SORT_EXPR, '@weight * population')

# some fields could matter more than others
cl.SetFieldWeights(dict(place=3))

## sql query to fetch the hits
db_fetch = fsphinx.DBFetch(db, sql = '''
select 
    g.id,
    "geonames" as source_db,
    g.name as place,
    g.ascii_name as place_ascii,
    g.alternate_names as place_alternate,
    a2.name as county,
    a2.name_ascii as county_ascii,
    g.admin1_code as state_code,
    a1.name as state,
    g.country_code,
    c.country,
    g.population,
    g.latitude*PI()/180 as lat,
    g.longitude*PI()/180 as lon,
    g.elevation,
    f.kind,
    f.feature_class,
    f.feature_code
from geoname as g
left join admin1 as a1 on
    g.country_code=a1.country_code and g.admin1_code=a1.admin1_code
left join admin2 as a2 on
    g.country_code=a2.country_code and g.admin1_code=a2.admin1_code and g.admin2_code=a2.admin2_code
left join country_info as c on
    g.country_code=c.iso
left join features as f on
    g.feature_class=f.feature_class and g.feature_code=f.feature_code
where id in ($id)
order by field(id, $id)'''
)
cl.AttachDBFetch(db_fetch)

# by default only this index will be queried
cl.SetDefaultIndex('geonames')
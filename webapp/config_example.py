import web
import app.helpers.template_utils

# in development debug error messages and reloader
web.config.debug = True

# in develpment template caching is set to false
cache = False

# set global base template
view = web.template.render('app/views', cache=cache)

# Google maps API key
google_map_key = ''

#!/usr/bin/env python

import web
import config

urls = (
    '/',                                         'app.controllers.base.index',
    '/search',                                   'app.controllers.base.search',
    
    '/(?:img|js|css)/.*',                        'app.controllers.public.public',
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
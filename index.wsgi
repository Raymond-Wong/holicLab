import sae

from holicLab import wsgi

application = sae.create_wsgi_app(wsgi.application)

import sys
sys.stdout = sys.stderr
sys.path.insert(0, '/var/www/html/ibgdb')

from application import app as application
from paste.exceptions.errormiddleware import ErrorMiddleware

application = ErrorMiddleware(application, debug=True)

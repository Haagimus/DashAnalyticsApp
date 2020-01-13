import sys
import logging
from logging.handlers import RotatingFileHandler

from layout import app

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('err.txt', maxBytes=10000, backupCount=1)
logger.addHandler(handler)
app.logger.addHandler(handler)

# Main application loop
if __name__ == '__main__':

    if len(sys.argv) == 2:
        if sys.argv[1] == 'debug':
            app.title = '(Debug) ForceX Analytics'
            app.run_server(debug=True, host='127.0.0.1', port='8080')
    else:
        app.title = 'ForceX Analytics'
        app.run_server(debug=False, host='166.20.109.188', port='8080')

import argparse
import logging
from logging.handlers import RotatingFileHandler

from app import app

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.WARN)
handler = RotatingFileHandler('log.txt', maxBytes=100000, backupCount=5)
app.logger.addHandler(handler)
site_admin = 'Haag, Gary'
site_admin_email = 'Gary.Haag@L3Harris.com'

# TODO: create a disposable worker thread to handle SQL query requests, this may prevent the errors when tabbing
#  through pages too fast

parser = argparse.ArgumentParser()
parser.add_argument('--debug')
parser.add_argument('--localdb')
args = parser.parse_args()

# Main application loop
if __name__ == '__main__':
    if args.debug:
        app.title = '(Debug) ForceX Analytics'
        app.run_server(debug=True, host='127.0.0.1', port='8080')
    else:
        app.title = 'ForceX Analytics'
        app.run_server(debug=False, host='166.20.109.188', port='8080')

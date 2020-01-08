import sys

from layout import app

# Main application loop
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'debug':
            app.title = '(Debug) ForceX Analytics'
            app.run_server(debug=True, dev_tools_hot_reload=True, host='127.0.0.1', port='8080')
    else:
        app.title = 'ForceX Analytics'
        app.run_server(debug=False, host='166.20.109.188', port='8080')

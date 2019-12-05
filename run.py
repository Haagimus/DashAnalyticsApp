# from app import app
# import sys
import create_app
import os


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


if __name__ == '__main__':
    app.run()

# # Main application loop
# if __name__ == '__main__':
#     if sys.argv[1] == 'debug':
#         app.run_server(debug=True, host='127.0.0.1', port='8080')
#     else:
#         app.run_server(debug=False, host='166.20.109.188', port='8080')

from __init__ import create_flask, create_dash
from layouts import main_layout_header, main_layout_sidebar

# The Flask instance
server = create_flask()

# The Dash instance
app = create_dash(server)

# Push an application context so we can use Flask's 'current_app'
with server.app_context():
    # Load the rest of the Dash app
    import index

    # Configure the Dash instance's layout
    app.layout = main_layout_header()

# Main application loop
# if __name__ == '__main__':
#     # Uncomment this line to run the actual server
#     # app.run_server(debug=False, host='166.20.109.188', port='8080')

#     # Uncomment this line to debug locally
#     app.run_server(debug=True, host='127.0.0.1', port='8080')

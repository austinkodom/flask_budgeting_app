from website import create_app
from waitress import serve

app = create_app()
mode = 'prod'

if __name__ == '__main__':
    if mode == 'dev':
        # Testing Environment
        app.run(debug=True)
    else:
        # Production Environment
        serve(app, host='0.0.0.0', port='50100', threads=2, url_prefix='/my_budget')
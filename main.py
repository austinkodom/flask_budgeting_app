from website import create_app

app = create_app()
mode = 'dev'

if __name__ == '__main__':
    if mode == 'dev':
        # Testing Environment
        app.run(debug=True)

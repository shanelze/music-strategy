from website import create_app

app = create_app ()

if __name__ == 'main':
    app.secret_key = 'BC3415'
    app.run (debug=True)
from app import app

# Expose WSGI application handler
application = app

if __name__ == '__main__':
    app.run()

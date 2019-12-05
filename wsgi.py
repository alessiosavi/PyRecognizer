from main import app

# gunicorn --certfile="conf/ssl/localhost.crt" --keyfile="conf/ssl/localhost.key"  --bind 0.0.0.0:8081 wsgi:app
if __name__ == "__main__":
    app.run()

# hedgedoc-pad-lister

List public [HedgeDoc](https://hedgedoc.org) pads, similar to Etherpad pad-lister

## Setup

### Production

Build and run the Docker container:

```
docker build -t hedgedoc-pad-lister .
docker run -d \
    -e 'FLASK_BASE_URL=http://hedgedoc.example.com' \
    -e 'FLASK_SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host/db' \
    -e 'FLASK_TIME_ZONE=Europe/Berlin' \
    -p 127.0.0.1:8000:8000 \
    hedgedoc-pad-lister
```

### Development

Create a virtual env and install dependencies:

```
python3 -m venv env
env/bin/pip3 install -r requirements.txt
```

Start database and HedgeDoc:

```
docker compose up -d db pad
```

Run app in debug mode:

```
export FLASK_BASE_URL="http://localhost:8000/"
export FLASK_SQLALCHEMY_DATABASE_URI="postgresql://postgres:unsicher123@localhost/postgres"
export FLASK_TIME_ZONE="Europe/Berlin"
env/bin/flask --app hedgedoc_pad_lister run --debug
```

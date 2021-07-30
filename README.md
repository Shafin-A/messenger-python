# Messenger

A one-to-one realtime chat app.

## Initial Setup

Create the PostgreSQL database (these instructions may need to be adapted for your operating system):

```
psql
CREATE DATABASE messenger;
\q
```

Create a `.env` file in the server directory and add the following variables (make any modifications to fit your local installation):
```
SECRET_KEY="YourSecretKey"
ENV="development"
POSTGRES_ENGINE="django.db.backends.postgresql_psycopg2"
POSTGRES_HOST="localhost"
POSTGRES_PORT=5432
POSTGRES_DATABASE="messenger"
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"

```


In the server folder, install dependencies and then seed the database (you may want to use a virtual environment):

```
cd server
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate 

python manage.py shell
from messenger_backend.seed import seed
seed()
exit()

```

In the client folder, install dependencies:

```
cd client
npm install
```

### Running the Application Locally

In one terminal, start the front end:

```
cd client
npm start
```

In a separate terminal, start the back end:

```
cd server
python manage.py runserver
```

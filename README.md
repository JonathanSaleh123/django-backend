# Checklist App Backend Repository

Built with **Django** with **Auth0** JWT-based authentication, **PostgreSQL**  database, and **AWS** S3 Buckets for file storage.

## Getting Started

### 1. Create Virtual Environment and install dependencies
Create a virtual environment with python
```
python -m venv backend
source backend/bin/activate
```
Clone the repository, and install dependencies
```
pip install -r requirements.txt
```
### 2. Env config
Create an ```.env``` file in the same file as ```setttings.py```
Fill it up with AWS information for using the S3 Bucket
```
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_key
export AWS_STORAGE_BUCKET_NAME=your_bucket
export AWS_S3_REGION_NAME=your_location
```

### 3. Set up PostgreSQL
Download postgreSQL and run it. Update the settings in ```setttings.py``` with your specific name, user, and password.
```
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'db_name',
    'USER': 'user', 
    'PASSWORD': 'pass',
    'HOST': 'localhost',
    'PORT': '5432',
  }
}
```

Run the migrations
```
python manage.py makemigrations
python manage.py migrate
```
### 4. Run the server
Run
```
python manage.py runserver
```

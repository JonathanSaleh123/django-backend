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

The list of routes 



## A. Authenticated Routes (Require Auth0 JWT)
Base URL: `http://localhost:8000/api/`

### Checklist Management

| Method | Endpoint                                      | Description                   |
|--------|-----------------------------------------------|-------------------------------|
| GET    | `/checklists/`                                | List checklists for user      |
| POST   | `/checklists/`                                | Create new checklist          |
| GET    | `/checklists/{checklist_id}/`                 | Retrieve a specific checklist |
| PUT    | `/checklists/{checklist_id}/`                 | Update checklist              |
| DELETE | `/checklists/{checklist_id}/`                 | Delete checklist              |
| POST   | `/checklists/{checklist_id}/clone/`           | Clone checklist               |
| POST   | `/checklists/{checklist_id}/share/`           | Create a shareable token link |


### Category Management

| Method | Endpoint                                                   | Description                |
|--------|------------------------------------------------------------|----------------------------|
| GET    | `/checklists/{checklist_id}/categories/`                   | List categories            |
| POST   | `/checklists/{checklist_id}/categories/`                   | Add a category             |
| DELETE | `/checklists/{checklist_id}/categories/{category_id}/`     | Delete a category          |


### Category Files

| Method | Endpoint                                                               | Description             |
|--------|------------------------------------------------------------------------|-------------------------|
| POST   | `/checklists/{checklist_id}/categories/{category_id}/files/`           | Upload file to category |
| DELETE | `/checklists/{checklist_id}/categories/{category_id}/files/{file_id}/` | Delete file             |

### Item Management

| Method | Endpoint                                                               | Description        |
|--------|------------------------------------------------------------------------|--------------------|
| GET    | `/checklists/{checklist_id}/categories/{category_id}/items/`           | List items         |
| POST   | `/checklists/{checklist_id}/categories/{category_id}/items/`           | Add item           |
| DELETE | `/checklists/{checklist_id}/categories/{category_id}/items/{item_id}/` | Delete item        |

### Item Files

| Method | Endpoint                                                                                     | Description         |
|--------|----------------------------------------------------------------------------------------------|---------------------|
| POST   | `/checklists/{checklist_id}/categories/{category_id}/items/{item_id}/files/`                 | Upload file to item |
| DELETE | `/checklists/{checklist_id}/categories/{category_id}/items/{item_id}/files/{file_id}/`       | Delete file         |




## B. Public Shared Routes (No login)

Base URL to get shared checklist: `http://localhost:8000/api/share/{token}/` 

### Shared Category Files

| Method | Endpoint                                     | Description              |
|--------|----------------------------------------------|--------------------------|
| GET    | `/categories/`                               | List categories          |
| POST   | `/categories/{category_id}/files/`           | Upload file to category  |


### Shared Item Files

| Method | Endpoint                                                  | Description            |
|--------|-----------------------------------------------------------|------------------------|
| GET    | `/categories/{category_id}/items/`                        | List items             |
| POST   | `/categories/{category_id}/items/{item_id}/files/`        | Upload file to item    |


### JSON structure of checklist

```json
{
  "id": 1,
  "title": "Checjlist",
  "description": "Checklist description",
  "created_at": "12-03-2025",
  "owner": "owner_id",
  "categories": [
    {
      "id": 1,
      "name": "cat1",
      "files": [
        {
          "id": 12,
          "file": "https://yourdomain.s3.amazonaws.com/category_files/a.pdf"
        }
      ],
      "items": [
        {
          "id": 21,
          "name": "item1",
          "is_completed": false,
          "files": [
            {
              "id": 301,
              "file": "https://yourdomain.s3.amazonaws.com/item_files/b.pdf"
            }
          ]
        },
      ]
    },
  ]
}
```

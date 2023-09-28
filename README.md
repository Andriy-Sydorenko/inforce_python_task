# Lunch Voting API

Django REST API for facilitating lunch place decision-making among company employees, supporting menu uploads from restaurants
## Getting Started

### Prerequisites

Before you begin, make sure you have the following tools and technologies installed:

- Python (>=3.6)
- Django
- Django REST framework

## Installing / Getting started
> A quick introduction of the setup you need to get run a project.

### Using Git
1. Clone the repo:
```shell
git clone https://github.com/Andriy-Sydorenko/inforce_python_task
```
2. You can open project in IDE and configure .env file using [.env.sample](.env.sample) file as an example.
<details>
<summary>Parameters for .env file:</summary>

- **DJANGO_DEBUG**: `Set True if you want debug menu to be on, and False for debug menu to be off`
- **DJANGO_SECRET_KEY**: `Your django secret key, you can generate one on https://djecrety.ir`
- **POSTGRES_DB**: `Name of your DB`
- **POSTGRES_DB_PORT**: `Port of your DB`
- **POSTGRES_USER**: `Name of your user for DB`
- **POSTGRES_PASSWORD**: `Your password in DB`
- **POSTGRES_HOST** `Host of your DB`
</details>

3. Run docker-compose command to build and run containers:
```shell
docker-compose up --build
```


> To access browsable api, use http://localhost:8000/api/v1/
> 
> To get access to the content, visit http://localhost:8000/api/user/token/ to get JWT token.



## Authentication
- The API uses token-based authentication for user access. Users need to obtain an authentication token by logging in.
- Administrators and authenticated users can access all endpoints, but only administrator can change information about restaurants and menus.

## Documentation
- The API is documented using the OpenAPI standard.
- Access the API documentation by running the server and navigating to http://localhost:8000/api/doc/swagger/ or http://localhost:8000/api/doc/redoc/.

## License
This project is licensed under the MIT License.
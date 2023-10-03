# CLOSEDAI FITNESS TRACKER API

## Introduction

API for a fitness tracking web app

## API Endpoints

The API has the following endpoints:

| Endpoint                   | HTTP Method | Description                                                                              | Required Parameters     | Optional Parameters  | Response Type    |
| -------------------------- | ----------- | ---------------------------------------------------------------------------------------- | ----------------------- | -------------------- | ---------------- |
| /                      | **GET**     | Return the API documentation (Swagger UI)                                                  | none                    | none                 | HTML             |
| /redoc                      | **GET**     | Return the API documentation (ReDoc)                                                  | none                    | none                 | HTML             |

## API Error handling

The API uses [FastAPI](https://fastapi.tiangolo.com/) as the framework and [Pydantic](https://pydantic-docs.helpmanual.io/) as the data validation library. FastAPI uses Pydantic to validate the data that is sent to the API and will return a HTTP status code and a JSON containing the error message if the data is invalid.

## API Server Technology

- The API is written in **python _3.11_** using the [FastAPI](https://fastapi.tiangolo.com/) framework.

- The API uses [PostgreSQL](https://www.postgresql.org/) as the database.
- The API is ran using [Uvicorn](https://www.uvicorn.org/).
- The API is deployed using [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).
- The packages in use can be found in the [pyproject.toml](./pyproject.toml) file.

## API Development

- Make sure you follow the [Indmeas API Design Guidelines](https://docs.indmeas.com/static/projects_html/design-guidelines/api-design.html).

### Setup

- Install [Python 3.11](https://www.python.org/downloads/).

- Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).
- Create a virtual environment.
  - Using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

    - ```bash
      conda env create --file environment.yml
      ```

      - Activate the conda environment.

      - ```bash
        conda activate fitness-api-env
        ```

- Install required python packages. (using [poetry](https://python-poetry.org/)) the packages are defined in the [pyproject.toml](./pyproject.toml) file.

```bash
poetry install
```

- Setup pre-commit

```bash
pre-commit install
```

- Run pre-commit

```bash
pre-commit run --all-files
```

### Running the API

- Run the API locally by running the [main.py](./main.py) file.

- Run the API locally with uvicorn.

```bash
uvicorn main:app --reload
```

- Run the API locally with docker-compose (**requires that you have built the image**).

```bash
docker-compose up
```

### Testing the API

- Run the tests.

```bash
pytest
```

### Making changes

- Adding new packages
**Add the new packages to the [pyproject.toml](./pyproject.toml) file.**
After adding the packages run

```bash
poetry lock
```

```bash
poetry install
```

### Building the API (pip package)

**The API pip package is built automatically by the CI/CD pipeline**
However, if you want to build the API locally you can do so by running the following command.

```bash
python setup.py sdist bdist_wheel
```

### Building the API (docker image)

```bash
docker build -t fitness-api .
```

### Environment variables

The API uses environment variables to configure the API.

```yml
FITNESS_API_DB_CONNECTION_STRING=postgresql+psycopg2://username:password@host/dbname
FITNESS_API_DEBUG_LOGGING=True # set to true to enable debug logging (default: false)
FITNESS_API_CORS_ORIGINS=["https://fitnessapp.com"] # sets cors origins defaults to allow all if not given
FITNESS_API_SECRET_KEY="secret"
FITNESS_API_ACCESS_TOKEN_EXPIRE_MINUTES=5
```

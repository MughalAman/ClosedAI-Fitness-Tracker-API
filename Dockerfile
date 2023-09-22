FROM continuumio/miniconda3

SHELL [ "/bin/bash" , "-c" ]

# Add the api folder to the container
ADD fitness_api /app/fitness_api

# Copy the main.py file to the container
COPY main.py /app/

# Copy the environment.yml file to the container
COPY environment.yml /app/

# Copy the poetry.lock file to the container
COPY poetry.lock /app/

# Copy the pyproject.toml file to the container
COPY pyproject.toml /app/

# Copy the README.md file to the container
COPY README.md /app/

# Set the working directory to /app
WORKDIR /app

RUN chmod -R 777 /opt/conda
RUN conda env create -f environment.yml

# Activate the environment and install the dependencies
RUN source activate fitness-api-env && poetry install --without dev

# Start the server with uvicorn
CMD source activate fitness-api-env && uvicorn main:app --host 0.0.0.0 --port 8000

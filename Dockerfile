# Setup base image
FROM python:3.8

# Setup environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
# Sets an environmental variable that ensures output from python is sent straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /opt/app

#FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends

# Install python dependencies in /.venv
COPY Pipfile /opt/app/
COPY Pipfile.lock /opt/app/
RUN pipenv install --dev --system --deploy --ignore-pipfile

# Install application into container
COPY . /opt/app/

EXPOSE 8000

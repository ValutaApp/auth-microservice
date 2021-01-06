import os
from api.core import get_pg_url

class Config:
    """
    Base Configuration
    """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"


class DevelopmentConfig(Config):
    """
    Development Configuration - default config

    This defaults the Database URL that can be created through the docker 
    cmd in the setup instructions. You can change this to environment variable as well. 
    """

    url = get_pg_url()
    SQLALCHEMY_DATABASE_URI = url
    SECRET_KEY = "asdf1234"
    DEBUG = True


class ProductionConfig(Config):
    """
    Production Configuration

    Most deployment options will provide an option to set environment variables.
    Hence, why it defaults to retrieving the value of the env variable `DATABASE_URL`.
    You can update it to use a `creds.ini` file or anything you want.

    Requires the environment variable `FLASK_ENV=prod`
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    )
    DEBUG = False


class DockerDevConfig(Config):
    """
    Docker Development Configuration

    Under the assumption that you are using the provided docker-compose setup, 
    which uses the `Dockerfile-dev` setup. The container will have
    the environment variable `FLASK_ENV=docker` to enable this configuration.
    This will then set up the database with the following hard coded
    credentials. 
    """

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://testusr:password@postgres/testdb"
    )  # hard coded URL, assuming you are using the docker-compose setup
    DEBUG = True


# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig, "prod": ProductionConfig, "docker": DockerDevConfig}

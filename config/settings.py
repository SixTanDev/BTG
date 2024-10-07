"""
This module defines the configuration settings for the application
using Pydantic's BaseSettings. It loads sensitive information
from environment variables specified in the .env file. The settings
include MongoDB credentials, Gmail configuration, and Twilio API keys.

The `Settings` class encapsulates all the environment
variables and provides an easy interface to access
the configuration values.
"""

# pylint: disable=R0903

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to manage and load application configurations
    from environment variables.

    This class includes configurations for MongoDB,
    basic authentication, Gmail, and Twilio.
    All values are loaded from the .env file.
    """

    # MongoDB Config
    ME_CONFIG_MONGODB_ADMINUSERNAME: str
    ME_CONFIG_MONGODB_ADMINPASSWORD: str
    ME_CONFIG_MONGODB_URL: str
    ME_CONFIG_BASICAUTH_USERNAME: str
    ME_CONFIG_BASICAUTH_PASSWORD: str

    # MongoDB InitDB Config
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str

    # Gmail Config
    GMAIL_USER: str
    GMAIL_PASSWORD: str

    # Twilio Config
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    class Config:
        """
        Config class to specify where to load the environment variables from.
        In this case, the .env file located in the root directory is used.
        """

        env_file = ".env"


settings = Settings()

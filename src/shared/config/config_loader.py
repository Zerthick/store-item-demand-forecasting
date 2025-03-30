from functools import lru_cache
import pathlib
from typing import Tuple, Type
from pydantic import BaseModel
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource


class Settings(BaseModel):
    """Settings class for the application.

    Args:
        model_api_url: URL for the MLFlow model API.
    """

    model_api_url: str


class Config(BaseSettings):
    """Config class to load settings from various sources.

    Args:
        default: Default settings.
        dev: Development settings.
        qa: QA settings.
        prod: Production settings.
        model_config: Configuration for the settings model.
    """

    default: Settings
    dev: Settings
    qa: Settings
    prod: Settings
    model_config = SettingsConfigDict(yaml_file=pathlib.Path(__file__).parent.resolve() / 'config.yaml')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )


@lru_cache  # Cache the loaded settings for better performance
def load_config_settings(env: str) -> Settings:
    """Load configuration settings based on the environment.

    Args:
        env: The environment for which to load settings (e.g., 'dev', 'qa', 'prod').

    Returns:
        Settings: The loaded settings for the specified environment.
    """

    appconfig = Config()  # type: ignore
    return getattr(appconfig, env)

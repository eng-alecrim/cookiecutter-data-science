# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from typing import List, Tuple, Type

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from .utils import get_path_project

# =============================================================================
# CONSTANTES
# =============================================================================

PROJECT_DIR = get_path_project()
yaml_file_path = PROJECT_DIR / "config/arquivo.yaml"
log_config_json_path = PROJECT_DIR / "config/log_config.json"

# =============================================================================
# CLASSES
# =============================================================================

# -----------------------------------------------------------------------------
# Variáveis de Ambiente
# -----------------------------------------------------------------------------


class EnvVariables(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    NOME_PROJETO: str


env_variables = EnvVariables()

# -----------------------------------------------------------------------------
# tratamento_texto.py
# -----------------------------------------------------------------------------


class AlgumaConfigYaml(BaseModel):
    algum_parametro: str


class YamlSettings(BaseSettings):
    alguma_config_yaml: AlgumaConfigYaml
    model_config = SettingsConfigDict(yaml_file=yaml_file_path)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


yaml_settings = YamlSettings()

# -----------------------------------------------------------------------------
# Configuração Logger
# -----------------------------------------------------------------------------


class LoggerHandlersBase(BaseModel):
    sink: str
    level: str
    format: str
    colorize: bool | None = None
    backtrace: bool | None = None


class LoggerHandlersToDisk(LoggerHandlersBase):
    rotation: str | None = None
    retention: str | None = None


class LoggerConfig(BaseModel):
    handlers: List[LoggerHandlersBase | LoggerHandlersToDisk]


logger_config = LoggerConfig(
    **JsonConfigSettingsSource(
        settings_cls=BaseSettings,
        json_file=log_config_json_path,
        json_file_encoding="utf-8",
    ).init_kwargs
)

from common.config import logger_config
from loguru import logger

logger.configure(**logger_config.model_dump())


def main() -> None:
    logger.debug("Hello from {{cookiecutter.project_dir}}!")
    return None


if __name__ == "__main__":
    main()

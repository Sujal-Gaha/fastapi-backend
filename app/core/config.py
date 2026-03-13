import os
import sys

from typing import Any, Optional
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class ServerConfig:
    ENVIRONMENT: str
    DATABASE_URL: str
    BASE_API_PATH: str
    PROJECT_NAME: str
    LOG_LEVEL: str
    WHITELISTED_ORIGINS: list[str]

    def validate(self) -> list[str]:
        errors = []

        if not self.ENVIRONMENT:
            errors.append("ENVIRONMENT is not set")

        if self.ENVIRONMENT not in ("dev", "prod"):
            errors.append("ENVIRONMENT must be either 'dev' or 'prod'")

        if not self.DATABASE_URL:
            errors.append("DATABASE_URL is not set")

        if not self.BASE_API_PATH:
            errors.append("BASE_API_PATH is not set")

        if not self.PROJECT_NAME:
            errors.append("PROJECT_NAME is not set")

        if not self.LOG_LEVEL:
            errors.append("LOG_LEVEL is not set")

        log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

        if self.LOG_LEVEL not in log_levels:
            errors.append(
                f"LOG_LEVEL must be one of the following values: {log_levels}"
            )

        if not self.WHITELISTED_ORIGINS:
            errors.append("WHITELISTED_ORIGINS is not set")

        return errors


class Config:
    def __init__(self):
        self.server = ServerConfig(
            ENVIRONMENT=os.getenv("ENVIRONMENT", "dev"),
            DATABASE_URL=os.getenv("DATABASE_URL", ""),
            BASE_API_PATH=os.getenv("BASE_API_PATH", ""),
            PROJECT_NAME=os.getenv("PROJECT_NAME", ""),
            LOG_LEVEL=os.getenv("LOG_LEVEL", ""),
            WHITELISTED_ORIGINS=self._get_list_of_str_env("WHITELISTED_ORIGINS", [""]),
        )

    def _get_list_of_str_env(self, key: str, default: list[str]) -> list[str]:
        values = os.getenv(key)

        if values is None:
            return default

        try:
            return list(values.split(","))
        except ValueError:
            raise ValueError(
                f"{key} must be a string of items separated by a comma (,). Got: {values}"
            )

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate all configuration

        Returns:
            tuple: (is_valid, list_of_errors)
        """
        all_errors = []

        all_errors.extend(self.server.validate())

        return len(all_errors) == 0, all_errors

    def get_summary(self) -> dict[str, Any]:
        return {
            "SERVER": {
                "ENVIRONMENT": self.server.ENVIRONMENT,
                "DATABASE_URL": self.server.DATABASE_URL,
                "BASE_API_PATH": self.server.BASE_API_PATH,
                "PROJECT_NAME": self.server.PROJECT_NAME,
                "LOG_LEVEL": self.server.LOG_LEVEL,
                "WHITELISTED_ORIGINS": self.server.WHITELISTED_ORIGINS,
            }
        }

    def log_summary(self, logger):
        logger.info("=" * 100)
        logger.info("Configuration Summary")
        logger.info("=" * 100)

        logger.info("Server Configurations:")
        logger.info(f"  Environment: {self.server.ENVIRONMENT}")
        logger.info(f"  Database URL: {self.server.DATABASE_URL}")
        logger.info(f"  Base Api Path: {self.server.BASE_API_PATH}")
        logger.info(f"  Project Name: {self.server.PROJECT_NAME}")
        logger.info(f"  Log Level: {self.server.LOG_LEVEL}")
        logger.info(f"  Whitelisted origins: {self.server.WHITELISTED_ORIGINS}")


_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get or create the configuration singleton

    Returns:
        Config: The application configuration
    """

    global _config

    if _config is None:
        _config = Config()

        is_valid, errors = _config.validate()

        if not is_valid:
            print("=" * 100, file=sys.stderr)
            print("CONFIGURATION ERRORS", file=sys.stderr)
            print("=" * 100, file=sys.stderr)

            for error in errors:
                print(f"  x {error}", file=sys.stderr)

            print("=" * 100, file=sys.stderr)

            raise ValueError(
                f"Configuration validation failed with {len(errors)} error(s)"
            )

    return _config


def validate_config() -> tuple[bool, list[str]]:
    """
    Validate configuration without creating singleton

    Returns:
        tuple: (is_valid, list_of_errors)
    """

    config = Config()
    return config.validate()


if __name__ == "__main__":
    """Run configuration validation"""
    print("=" * 100)
    print("Configuration Validation Tool")
    print("=" * 100, end="\n\n")

    try:
        config = get_config()
        print("Configuration is valid!\n")
        config.log_summary(type("Logger", (), {"info": print})())

    except ValueError as e:
        print("Configuration validation failed:")
        print(f"{e}")
        sys.exit(1)

    except Exception as e:
        print("Unexpected error:")
        print(f"{e}")

        import traceback

        traceback.print_exc()
        sys.exit(1)

"""AI Tells: Detect linguistic patterns commonly associated with AI-generated prose."""

from importlib import metadata

__version__ = metadata.version("aitells")
__all__ = ["__version__", "main"]


def main() -> None:  # noqa: D103
    print("Hello from aitells!")  # noqa: T201

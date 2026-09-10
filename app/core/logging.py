import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True
    )

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"atlas.{name}")

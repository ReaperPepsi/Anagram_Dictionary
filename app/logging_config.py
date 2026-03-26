import logging
import sys
from pathlib import Path


def setup_logging():
    Path("Logs").mkdir(exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── ROOT logger ──────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    root = logging.getLogger("app")
    root.setLevel(logging.DEBUG)
    root.addHandler(console_handler)

    # ── AUTH logger ──────────────────────────────────────────────
    auth_file = logging.FileHandler("Logs/auth.log")
    auth_file.setFormatter(formatter)
    auth_file.setLevel(logging.WARNING)

    auth_logger = logging.getLogger("app.auth")
    auth_logger.addHandler(auth_file)

    # ── ANAGRAMS logger ──────────────────────────────────────────
    anagrams_file = logging.FileHandler("Logs/anagrams.log")
    anagrams_file.setFormatter(formatter)
    anagrams_file.setLevel(logging.INFO)

    anagrams_logger = logging.getLogger("app.anagrams")
    anagrams_logger.addHandler(anagrams_file)


logger = logging.getLogger("app")
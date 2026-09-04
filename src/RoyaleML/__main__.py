"""Run the bot: ``python -m RoyaleML`` from ``src/``, or ``python src/RoyaleML/main.py``."""

from pathlib import Path
import sys

_src = Path(__file__).resolve().parent.parent
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from RoyaleML.main import main

if __name__ == "__main__":
    main()

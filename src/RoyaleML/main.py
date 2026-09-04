from pathlib import Path
import sys

for _parent in Path(__file__).resolve().parents:
    if _parent.name == "src" and (_parent / "RoyaleML").is_dir():
        if str(_parent) not in sys.path:
            sys.path.insert(0, str(_parent))
        break

from RoyaleML.computer_vision.capture import capture, run_loop


def main() -> None:
    run_loop(capture)


if __name__ == "__main__":
    main()

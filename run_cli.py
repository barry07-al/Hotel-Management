import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.infrastructure.cli import CLI

if __name__ == "__main__":
    main_class = CLI()
    main_class.run()

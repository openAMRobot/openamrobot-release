"""Validate a pinned source bundle without extracting it."""
import argparse
from pathlib import Path
from build_pinned_release import validate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    validate(parser.parse_args().archive)

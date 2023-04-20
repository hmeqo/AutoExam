from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

CLIENT_DIR = BASE_DIR / 'client'

DIST_DIR = CLIENT_DIR / 'dist'

STATIC_DIR = DIST_DIR / 'assets'

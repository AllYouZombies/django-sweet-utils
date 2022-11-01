import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

DEBUG = False if os.getenv('DJANGO_DEBUG') == 'False' else True

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = BASE_DIR / 'assets'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

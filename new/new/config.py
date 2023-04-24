from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY_FOR_DJANGO = os.environ.get('SECRET_KEY_FOR_DJANGO')
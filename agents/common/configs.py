import os
from dotenv import load_dotenv

load_dotenv()

LITELLM_API_BASE = os.getenv("LITELLM_API_BASE")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY")

REQUESTS_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

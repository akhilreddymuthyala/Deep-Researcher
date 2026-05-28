import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "meta-llama/llama-3.3-8b-instruct:free"  # free model

SEARCH_RESULTS_LIMIT = 5
FINDINGS_DIR = "findings"
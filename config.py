from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploads"
KB_DIR = BASE_DIR / "knowledge_base"
VECTOR_DIR = BASE_DIR / "vector_db"
UPLOAD_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)
VECTOR_DIR.mkdir(exist_ok=True)

# Load Grok/OpenAI-compatible API key from environment for safety.
# Do NOT commit secrets into source control. Put your key into a .env file
# or export it into your shell as GROK_API_KEY.
GROK_API_KEY = os.getenv('GROK_API_KEY')

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# LLM backend configuration: 'transformers' to use local/HuggingFace models (LLama),
# or 'grok' to use Grok/OpenAI-compatible API. Change as needed.
LLM_BACKEND = 'grok'
# Use a 70B Llama chat model hosted by the API provider (Groq). This will route requests
# to the provider instead of trying to run the model locally.
LLM_MODEL = 'llama-3.3-70b-versatile'
# API base URL for Groq/OpenAI-compatible endpoint
LLM_API_BASE = 'https://api.groq.com/openai/v1'

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3

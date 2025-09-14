"""
Simple Configuration for AI Web Scraper
"""
import os
from dotenv import load_dotenv

load_dotenv()

# AI Model Settings
AI_MODEL = os.getenv("AI_MODEL", "llama3.2:1b")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.1"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "6000"))

# Scraping Settings
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Application Settings
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
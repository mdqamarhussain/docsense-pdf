from langchain_ollama import OllamaLLM
from app.core.config import OLLAMA_MODEL, TEMPERATURE

llm = OllamaLLM(
    model=OLLAMA_MODEL,
    temperature=TEMPERATURE
)
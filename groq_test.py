from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    # Get API key
    #api_key=os.environ.get("GROQ_API_KEY"),
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.create(
    input="Explain the importance of fast language models",
    model="llama-3.1-8b-instant"
)
print(response.output_text)

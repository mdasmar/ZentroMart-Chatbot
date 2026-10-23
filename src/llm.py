from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]

llm=ChatOpenAI(
    model=deployment,
    base_url=f"{endpoint}/openai/v1/",
    api_key=api_key
)
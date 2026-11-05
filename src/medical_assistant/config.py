import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm_id = os.getenv("MODEL_ID")

model = ChatGroq(model = llm_id)


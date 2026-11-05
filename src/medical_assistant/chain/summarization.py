from langchain_core.output_parsers import StrOutputParser
from medical_assistant.prompts.summarization import template
from medical_assistant.config import model

parser = StrOutputParser()


summarization_chain = template | model | parser
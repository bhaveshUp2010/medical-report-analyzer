from langchain_core.output_parsers import StrOutputParser
from medical_assistant.prompts.explanation import template
from medical_assistant.config import model


chain = template | model | StrOutputParser()



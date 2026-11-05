from medical_assistant.prompts.extraction import template, parser
from medical_assistant.config import model

extraction_chain = template | model | parser
   
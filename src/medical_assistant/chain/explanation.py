from langchain_core.output_parsers import StrOutputParser
from medical_assistant.prompts.explanation import template
from medical_assistant.config import model


chain = template | model | StrOutputParser()


def understand_terminology(term: str, question: str):
    return chain.invoke({
      "medical_term": term,
      "question": question  
    })
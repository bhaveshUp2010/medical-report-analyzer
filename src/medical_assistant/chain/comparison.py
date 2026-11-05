from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough
)
from medical_assistant.chain.extraction import extraction_chain
from medical_assistant.config import model
from medical_assistant.utils.comparison_utils import compare_reports
from langchain_core.output_parsers import StrOutputParser
from medical_assistant.prompts.comparison import template

test_extractor = RunnableParallel(
    report_1 = RunnableLambda(lambda x : x["report_1"]) | extraction_chain,    
    report_2 = RunnableLambda(lambda x : x["report_2"]) | extraction_chain
)


comparison_chain = RunnableParallel(
    comparison = RunnablePassthrough(),
    summary = template | model | StrOutputParser()
) 


final_chain = test_extractor | RunnableLambda(compare_reports) | comparison_chain

def compare_medical_reports(reports: dict):
    return final_chain.invoke(reports)
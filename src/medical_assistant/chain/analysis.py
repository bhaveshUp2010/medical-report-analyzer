from langchain_core.runnables import (
    RunnableParallel, 
    RunnablePassthrough,
    RunnableLambda,
    RunnableSequence
)
from medical_assistant.config import model
from medical_assistant.chain.extraction import extraction_chain
from medical_assistant.chain.summarization import summarization_chain

analysis_parallel = RunnableParallel(
    original_report = RunnableLambda(lambda x: x["report"]),
    summary = summarization_chain,
    medical_data = extraction_chain
)

def combine_data(data):
    return {
        "report": data["original_report"],
        "summary": data["summary"],
        "medical_data": data["medical_data"]
    }

def analyse_test(data):
    results = []

    for test in data["medical_data"].test_info:

        value = test.value

        ranges = test.reference_range.split("-")

        lower = float(ranges[0].replace(",", "").strip())
        upper = float(ranges[1].replace(",", "").strip())

        if value < lower:
            comparison = "below range"

        elif value > upper:
            comparison = "above range"

        else:
            comparison = "within range"

        results.append({
            "test": test.test_name,
            "value": value,
            "comparison": comparison
        })

    return results  

analysis_chain = (
    analysis_parallel |
    RunnableLambda(combine_data) | 
    RunnablePassthrough.assign(
        analysis = RunnableLambda(analyse_test)
    )
)


def analyse_report(report):
    return analysis_chain.invoke({
        "report": report
    })
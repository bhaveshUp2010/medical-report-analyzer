from medical_assistant.chain.comparison import final_chain as comparison_chain
REPORT_1 = "C:/serious-projects/medical-assistant/data/report001.txt"
REPORT_2 = "C:/serious-projects/medical-assistant/data/report002.txt"

with open(REPORT_1, "r") as file:
    report_1 = file.read()

with open(REPORT_2, "r") as f:
    report_2 = f.read()

input_data = {
    "report_1": report_1,
    "report_2": report_2
}

res = comparison_chain.invoke(input_data)

print(res["summary"])
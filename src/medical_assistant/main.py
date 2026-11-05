from medical_assistant.chain.analysis import analyse_report
from medical_assistant.chain.comparison import compare_medical_reports


print("Choose the feature: ")
print("1. analyze your medical report: ")
print("2. compare medical reports: ")


user_choice = int(input("->"))

if user_choice == 1:

    with open("C:/serious-projects/medical-assistant/data/report002.txt", "r") as f:
        report = f.read()
    report = analyse_report(report)

if user_choice == 2:
    with open("C:/serious-projects/medical-assistant/data/report002.txt", "r") as f:
        report_1 = f.read()
    with open("C:/serious-projects/medical-assistant/data/report001.txt", "r") as f:
        report_2 = f.read()

    reports = {
        "report_1": report_1,
        "report_2": report_2
    }

    comparison = compare_medical_reports(reports= reports)

    print(comparison)
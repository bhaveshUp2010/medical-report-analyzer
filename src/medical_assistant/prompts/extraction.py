from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from medical_assistant.schemas.medical_test import MedicalReport

parser = PydanticOutputParser(pydantic_object=MedicalReport)

template = PromptTemplate(
    template= """You are an expert medical data extraction assistant. Your task is to accurately extract patient information, hematology test parameters, units, reference ranges, and clinical interpretations from the provided medical lab report text into the required structured format.

### Instructions:
1. Extract all metadata accurately (Patient Name, Lab No, Age/Sex, Collection Date,refrencce range with unit , etc.).
2. For each test parameter, capture:
   - Parameter name
   - Result value (as a float or string depending on your schema)
   - Unit
   - Biological reference range
3. Accurately identify and list any inferred clinical conditions or comments mentioned in the report interpretation section.
4. Do not hallucinate or extrapolate values not present in the text. If a value is missing, use null/None.
5. Strictly adhere to the requested output formatting instructions.
### Extraction Rules:

1. test_info must ONLY contain actual laboratory test
   measurements.

2. Every test_info entry should contain:
   test_name, value, unit, reference_range and flag.

3. Do not put clinical interpretations, diagnoses,
   comments or impressions inside test_info.

4. Extract all interpretations from the
   INTERPRETATION & IMPRESSIONS section into
   the interpretation field.

5. Preserve the original interpretation text.
   Do not generate new diagnoses.

6. Extract LOW, HIGH and NORMAL flags exactly
   as provided in the report.

7. Do not confuse the referring doctor with the
   verifying pathologist.

8. If information is unavailable, use null.

### Format Instructions:
{format_instructions}

### Medical Report Text:
---------------------------------------------
{report}
---------------------------------------------

Extract the information now:""",
    input_variables=["report"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
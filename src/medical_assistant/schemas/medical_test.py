from pydantic import BaseModel, Field
from typing import List, Optional


class MedicalTest(BaseModel):
    test_name: str
    value: Optional[float] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    flag: Optional[str] = None


class MedicalReport(BaseModel):
    patient_name: str
    doctor_name: List[str]
    report_date: str
    age_sex: Optional[str] = None
    lab_number: Optional[str] = None
    sample_type: Optional[str] = None

    test_info: List[MedicalTest]

    interpretation: List[str] = Field(default_factory=list)
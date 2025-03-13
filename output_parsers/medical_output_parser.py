# output_parsers/medical_output_parser.py
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from pydantic import BaseModel, Field
from typing import List

class MedicalReport(BaseModel):
    diagnosis: str = Field(description="The patient's diagnosis.")
    treatment: List[str] = Field(description="A list of treatment options.")

response_schemas = [
    ResponseSchema(name="diagnosis", description="The patient's diagnosis."),
    ResponseSchema(name="treatment", description="A list of treatment options."),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

def parse_medical_report(llm_output: str) -> MedicalReport:
    """Parses the LLM's output into a MedicalReport object."""
    try:
        parsed_data = output_parser.parse(llm_output)
        return MedicalReport(**parsed_data)
    except Exception as e:
        return f"Error parsing medical report: {e}"
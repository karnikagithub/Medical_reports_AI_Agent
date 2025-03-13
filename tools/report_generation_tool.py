# tools/report_generation_tool.py
from langchain.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import base64
from chains.report_chain import create_report_chain
from langchain.chains import LLMChain

load_dotenv()

class ReportGenerationTool(BaseTool):
    name: str = "Report Generation"
    description: str = "Useful for generating medical reports in PDF format."
    llm: ChatGoogleGenerativeAI
    report_chain: LLMChain = None

    def __init__(self, llm: ChatGoogleGenerativeAI, **kwargs):
        config = {"llm": llm}
        config.update(kwargs)
        super().__init__(**config)
        self.llm = llm
        self.report_chain = create_report_chain(llm)

    def _run(self, text: str) -> str:
        try:
            response_text = self.report_chain.invoke({'text': text})['text']
            print(f"LLM Response: {response_text}")
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, response_text)
            p.save()

            pdf_bytes = buffer.getvalue()
            print(f"PDF Bytes: {pdf_bytes[:100]}...")

            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            return pdf_base64
        except Exception as e:
            print(f"Error generating PDF report: {e}")
            return f"Error generating PDF report: {e}"

    def _arun(self, text: str):
        raise NotImplementedError("This tool does not support async")
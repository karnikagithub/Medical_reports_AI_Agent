from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

def create_report_chain(llm):
    prompt_template = """Generate a detailed medical report based on the following information:
    "{text}"
    DETAILED MEDICAL REPORT:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain
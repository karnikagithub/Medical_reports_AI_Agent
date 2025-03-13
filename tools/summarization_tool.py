# tools/summarization_tool.py
from langchain.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from chains.summarization_chain import create_summarization_chain

load_dotenv()

class SummarizationTool(BaseTool):
    name: str = "Text Summarization"
    description: str = "Useful for summarizing long texts."
    llm: ChatGoogleGenerativeAI
    summarization_chain:str = None

    def __init__(self, llm: ChatGoogleGenerativeAI, **kwargs):
        config = {"llm": llm}
        config.update(kwargs)
        super().__init__(**config)
        self.llm = llm
        self.summarization_chain = create_summarization_chain(llm)

    def _run(self, text: str) -> str:
        """Use the tool."""
        try:
            summary = self.summarization_chain.invoke({'text': text})['text']
            return summary
        except Exception as e:
            return f"Error during summarization: {e}"

    def _arun(self, text: str):
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")
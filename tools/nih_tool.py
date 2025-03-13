# tools/nih_tool.py
from langchain.tools import BaseTool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class NIHSearchTool(BaseTool):
    name: str = "NIH Search"
    description: str = "Useful for searching the National Institutes of Health (NIH) databases."

    def _run(self, query: str) -> str:
        """Use the tool."""
        try:
            url = f"https://clinicaltrials.gov/api/query/study_fields?expr={query}&fields=BriefTitle,OfficialTitle,BriefSummary,DetailedDescription&min_rnk=1&max_rnk=10&fmt=json"
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            results = data.get("study_fields", [])
            if results:
                return str(results)
            else:
                return "No results found."
        except requests.exceptions.RequestException as e:
            return f"Error during NIH search: {e}"
        except ValueError as e:
            return f"Error parsing JSON: {e}"

    def _arun(self, query: str):
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")
# tools/who_tool.py
from langchain.tools import BaseTool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WHOSearchTool(BaseTool):
    name: str = "WHO Search"
    description: str = "Useful for searching the World Health Organization (WHO) databases."

    def _run(self, query: str) -> str:
        """Use the tool."""
        try:
            url = f"https://apps.who.int/iris/api/search?query={query}&limit=10"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if results:
                return str(results)
            else:
                return "No results found."
        except requests.exceptions.RequestException as e:
            return f"Error during WHO search: {e}"
        except ValueError as e:
            return f"Error parsing JSON: {e}"

    def _arun(self, query: str):
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")
# tools/web_scraping_tool.py
from langchain.tools import BaseTool
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

class WebScrapingTool(BaseTool):
    name: str = "Web Scraping"
    description: str = "Useful for scraping data from websites."

    def _run(self, url: str) -> str:
        """Use the tool."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            return text[:5000]  # Limit to 5000 characters
        except requests.exceptions.RequestException as e:
            return f"Error during web scraping: {e}"
        except Exception as e:
            return f"Error processing web content: {e}"

    def _arun(self, url: str):
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")
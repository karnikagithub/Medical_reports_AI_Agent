# tools/pubmed_tool.py
from langchain.tools import BaseTool
import requests
import xml.etree.ElementTree as ET

class PubMedSearchTool(BaseTool):
    name: str = "PubMed Search"  # Added type annotation
    description: str = "Useful for searching PubMed for medical research articles." # Added type annotation

    def _run(self, query: str) -> str:
        """Use the tool."""
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax=5"  # Limit to 5 results
        try:
            response = requests.get(search_url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            root = ET.fromstring(response.content)
            id_list = [id_elem.text for id_elem in root.find("IdList").findall("Id")]
            if not id_list:
                return "No results found."
            results = []
            for pubmed_id in id_list:
                summary_url = f"{base_url}esummary.fcgi?db=pubmed&id={pubmed_id}"
                summary_response = requests.get(summary_url)
                summary_response.raise_for_status()
                summary_root = ET.fromstring(summary_response.content)
                article_title = summary_root.find(".//Title").text
                results.append(f"Title: {article_title}, PubMed ID: {pubmed_id}")
            return "\n".join(results)
        except requests.exceptions.RequestException as e:
            return f"Error during PubMed search: {e}"
        except ET.ParseError as e:
            return f"Error parsing PubMed response: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def _arun(self, query: str):
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")
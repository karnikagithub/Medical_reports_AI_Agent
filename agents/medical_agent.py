# agents/medical_agent.py
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from tools.pubmed_tool import PubMedSearchTool
from tools.nih_tool import NIHSearchTool
from tools.who_tool import WHOSearchTool
from tools.web_scraping_tool import WebScrapingTool
from tools.summarization_tool import SummarizationTool
from tools.report_generation_tool import ReportGenerationTool
from tools.email_delivery_tool import EmailDeliveryTool
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from output_parsers.medical_output_parser import parse_medical_report
import google.generativeai as genai

load_dotenv()
models = genai.list_models()
for model in models:
    print(model.name,'---------------')

class AgentStartCallbackHandler(BaseCallbackHandler):
    def on_agent_action(self, action, **kwargs):
        print(f"Agent is using tool: {action.tool}")

class AgentFinishCallbackHandler(BaseCallbackHandler):
    def on_agent_finish(self, finish, **kwargs):
        print("Agent finished task.")

def create_medical_agent():
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
    tools = [
        PubMedSearchTool(),
        NIHSearchTool(),
        WHOSearchTool(),
        WebScrapingTool(),
        SummarizationTool(llm=model),
        ReportGenerationTool(llm=model),
        EmailDeliveryTool()
    ]
    summary_prompt = """Answer the following medical questions as best you can. You have access to the following tools:

    When answering questions, please follow these guidelines:
    1. Think step by step. Break down complex questions into smaller, manageable steps.
    2. Use the tools provided to gather information.
    3. Cite your sources whenever possible.
    4. If you are unsure of an answer, state that you do not know.
    5. When using a tool, state the tool that you are using, and the information that you are passing into that tool.
    6. Provide accurate and up-to-date medical information.

    Here is an example of Chain of Thought reasoning.
    Question: What are the side effects of Drug A, and what research has been done on it?
    Thought: First, I will use the PubMed Search tool to find research articles on Drug A.
    Action: PubMed Search: Drug A side effects research
    Observation: (Results from PubMed Search)
    Thought: Now, I will use the Summarization tool to summarize the research articles.
    Action: Summarization: (Results from PubMed Search)
    Observation: (Summary of research articles)
    Final Answer: (Summary of side effects and research)

    Begin! Remember to answer with citations when possible.

    {chat_history}
    Question: {input}
    {agent_scratchpad}"""
    prompt = PromptTemplate(
        template=summary_prompt,
        input_variables=["input", "chat_history", "agent_scratchpad"],
    )
    llm_chain = LLMChain(llm=model, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, callbacks=[AgentStartCallbackHandler(),AgentFinishCallbackHandler()], handle_parsing_errors=True)
    return agent_executor
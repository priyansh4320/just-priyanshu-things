from pprint import pprint
from just_another_agent.langgraphs.graph_with_ollama_llm_node import asistant_tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from just_another_agent.langgraphs.graph_schema import CustomGraphState, StructuredGraphState
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import requests
import os

load_dotenv()

MARKETSTACK_API_KEY = os.getenv("MARKETSTACK_API_KEY")

def get_model():
    """Get the model instance."""
    return ChatOllama(model="llama3.2:latest", temperature="0.0")


async def get_stock_info(CustomGraphState):

    """Get stock information based on the provided GraphState."""
    messages = CustomGraphState['messages']
    stock_symbol = CustomGraphState['structured_response'].stock_symbol
    url = f"http://api.marketstack.com/v2/tickers/{stock_symbol}"
    params = {"access_key": MARKETSTACK_API_KEY}
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    messages.append(str(result))
    return {'messages': messages, "stock_symbol": stock_symbol}


def create_agent(model, tools, prompt):
    """Create an agent with the specified model, tools, and prompt."""
    agent = create_react_agent(model=model, tools=tools, prompt=prompt, state_schema=CustomGraphState, response_format=StructuredGraphState)
    return agent


def llmgraph():
    """Create a state graph with the agent and stock information retrieval."""
    model = get_model()
    prompt = """You are a helpful assistant that only helps in queries related to the stock market."""
    agent = create_agent(model, [asistant_tool], prompt)

    workflow = StateGraph(CustomGraphState)
    workflow.add_node("agent", agent)
    workflow.add_node("get_stock_details", get_stock_info)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", "get_stock_details")
    workflow.add_edge("get_stock_details", END)
    graph = workflow.compile(debug=True)
    return graph



import asyncio
async def run_g():
    """Run the graph with a sample message."""
    message = {"messages": ['what is the stock symbol for Apple inc.?']}
    graph = llmgraph()
    response = await graph.ainvoke(message)
    pprint(response)

asyncio.run(run_g())


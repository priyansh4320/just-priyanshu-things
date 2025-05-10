from just_another_agent.langgraphs.graph_with_ollama_llm_node import asistant_tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from just_another_agent.langgraphs.graph_schema import CustomGraphState, StructuredGraphState
from langgraph.graph import StateGraph, END
from pprint import pprint
from dotenv import load_dotenv
import os

import requests
load_dotenv()

MARKETSTACK_API_KEY = os.getenv("MARKETSTACK_API_KEY")

def get_model():
    """Get the model instance."""
    return ChatOllama(model="llama3.2:latest", temperature="0.0")


def create_agent(model, tools, prompt):
    """Create an agent with the specified model, tools, and prompt."""
    agent = create_react_agent(model=model, tools=tools, prompt=prompt, state_schema=CustomGraphState, response_format=StructuredGraphState)
    return agent


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


async def summaize_information(CustomGraphState):
    """Summarize the information retrieved from the stock API."""
    messages = CustomGraphState['messages']
    last_messages = CustomGraphState['messages'][-1]
    stock_symbol = CustomGraphState['stock_symbol']
    model = get_model()
    prompt = """You are a Helpful Assistant that will Explain and give an Analysis report about the Stock Market.
    You will be given a stock symbol and the information about the stock.
    You will give a summary of the information and also give an analysis report about the stock.
    """
    # model.ainvoke({"messages": [prompt+last_messages], "stock_symbol": stock_symbol})
    summary = await model.ainvoke(prompt+last_messages)
    messages.append(str(summary.content))
    return {'messages': messages, "stock_symbol": stock_symbol}


def llmgraph():
    """Create a state graph with the agent and stock information retrieval."""
    model = get_model()
    prompt = """You are a helpful assistant that only helps in queries related to the stock market."""
    agent = create_agent(model, [asistant_tool], prompt)

    workflow = StateGraph(CustomGraphState)
    workflow.add_node("agent", agent)
    workflow.add_node("get_stock_details", get_stock_info)
    workflow.add_node("summarize_information", summaize_information)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", "get_stock_details")
    workflow.add_edge("get_stock_details", "summarize_information")
    workflow.add_edge("summarize_information", END)
    graph = workflow.compile(debug=True)
    return graph


async def run_g():
    """Run the graph with a sample message."""
    message = {"messages": ['what is the stock symbol for Apple inc.?']}
    graph = llmgraph()
    response = await graph.ainvoke(message)
    pprint(response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_g())
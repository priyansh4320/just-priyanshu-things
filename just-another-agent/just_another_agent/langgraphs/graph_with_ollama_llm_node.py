from pprint import pprint
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from just_another_agent.langgraphs.graph_schema import CustomGraphState ,StructuredGraphState
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool


def get_model():
    return ChatOllama(model="llama3.2:latest",temperature="0.0")


def create_agent(model,tools,prompt):
    agent = create_react_agent(model=model,tools=tools,prompt=prompt,state_schema=CustomGraphState,response_format=StructuredGraphState)
    return agent


@tool
def asistant_tool(input:str):
    """
    This is an Asistant tool. /
    use this tool to perform determine the symbol for a stock , based on given stock name.
    Input to the tool will be the sock name.
    # Example:
        user_query: give me the stock symbol for google.com
        input: 'GOOG'
    # important input will only include the stock symbol nothing else.
    """

    pprint(input)
    return input


def llmgraph():
    model = get_model()
    prompt = """You are a helpful asistant that only helps in queiries related to stock market."""
    agent = create_agent(model,[asistant_tool],prompt)
    
    workflow = StateGraph(CustomGraphState)
    workflow.add_node("agent",agent)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent",END)
    graph = workflow.compile(debug=True)
    return graph


async def run_g():
    message = {"messages":['what is the stock symbol for Apple inc.?']}
    graph = llmgraph()
    response = await graph.ainvoke(message)
    pprint(response)

import asyncio
# asyncio.run(run_g())
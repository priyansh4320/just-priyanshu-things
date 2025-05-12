from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from just_another_agent.langgraphs.graph_with_ollama_llm_node import asistant_tool
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
    print("########################### stock ###########################")

    messages = CustomGraphState['messages']
    stock_symbol = CustomGraphState['structured_response'].stock_symbol
    url = f"http://api.marketstack.com/v2/tickers/{stock_symbol}"
    params = {"access_key": MARKETSTACK_API_KEY}
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    messages.append(str(result))
    return {'messages': messages, "stock_symbol": stock_symbol}


async def summarize_information(CustomGraphState):
    """Summarize the information retrieved from the stock API."""
    print("###########################summary ###########################")

    messages = CustomGraphState['messages']
    last_messages = CustomGraphState['messages'][-1]

    model = get_model()
    prompt = """return a summary on this:  """

    summary = await model.ainvoke(prompt+last_messages)
    # messages.append(str(summary.content))
    new_messages = messages + [str(summary.content)]
    return {'messages': new_messages, "stock_symbol": ""}


async def decision_node(CustomGraphState):
    return CustomGraphState


async def decision(CustomGraphState):
    """Make a decision based on the stock information."""
    print("########################### decision ###########################")
    
    messages = CustomGraphState['messages']
    last_messages = CustomGraphState['messages'][-1]

    model = get_model()
    prompt = """
    analyse the question and return a decision on this:  
                
                # Decision Options:
                     "summary"
                     "stock_info'

                # Strictly return the Decision Option only.
                # Strictly only make the Decision based on the Last Message.
    """
    decision = await model.ainvoke(prompt+last_messages)
    messages.append(str(decision.content))
    print("Decision: ######## ", decision.content)        
    if "summary" in decision.content:
        return "summarize_information"
    else:
        return "agent"
    

def llmgraph():
    """Create a state graph with the agent and stock information retrieval."""
    model = get_model()
    agent = create_agent(model, [asistant_tool], "You are a helpful assistant that only helps in queries related to the stock market.")
    
    workflow = StateGraph(CustomGraphState)

    workflow.add_node("agent", agent)
    workflow.add_node("decision_node", decision_node)
    workflow.add_node("get_stock_details", get_stock_info)
    workflow.add_node("summarize_information", summarize_information)
    
    workflow.set_entry_point("decision_node")
    workflow.add_conditional_edges("decision_node", decision)
    
    workflow.add_edge("decision_node", "agent")
    workflow.add_edge("decision_node", "summarize_information")
    workflow.add_edge("agent","get_stock_details")

    # workflow.add_edge("get_stock_details")
    # workflow.add_edge("summarize_information")

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
 
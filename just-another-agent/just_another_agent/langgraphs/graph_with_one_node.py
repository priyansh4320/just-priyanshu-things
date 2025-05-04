
from just_another_agent.langgraphs.graph_schema import GraphState
from langgraph.graph import StateGraph,END
from dotenv import load_dotenv
import os
import requests
load_dotenv()


MARKETSTACK_API_KEY=os.getenv("MARKETSTACK_API_KEY")


workflow = StateGraph(GraphState)




async def get_stock_info(GraphState):
    messages = GraphState['messages']
    stock_symbol = GraphState['stock_symbol']
    url = f"http://api.marketstack.com/v2/tickers/{stock_symbol}"
    params = {"access_key":MARKETSTACK_API_KEY}
    headers = {"Content-Type":"application/json"}
    response = requests.get(url,params=params,headers=headers)
    
    result = response.json()
    messages.append(str(result))
    return {'messages':messages,"stock_symbol":stock_symbol}




workflow.add_node("get_stock_details",get_stock_info)
workflow.set_entry_point("get_stock_details")
workflow.add_edge("get_stock_details",END)
graph = workflow.compile()

state = {'messages':['hey there, can i get details for apple inc. stock'],'stock_symbol':"GOOG"}

async def run_g():
    message = await graph.ainvoke(state)

    print(message)

import asyncio

asyncio.run(run_g())
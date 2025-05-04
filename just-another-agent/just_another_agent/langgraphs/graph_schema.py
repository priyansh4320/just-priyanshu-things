from typing import TypedDict, List,Dict,Optional
from langgraph.prebuilt.chat_agent_executor import AgentState
from pydantic import BaseModel

class GraphState(TypedDict):
    messages:List[str]
    stock_symbol: str
    pass

class CustomGraphState(AgentState):
    messages:List[str]
    stock_symbol: Optional[str]=" "
    structured_response:Optional[Dict[str,str]] 
    pass

class StructuredGraphState(BaseModel):
    messages:List[str]
    stock_symbol: str
    structured_response:Dict[str,str]
    pass
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from just_another_agent.langgraphs.graph_with_one_node import get_stock_info
from just_another_agent.langgraphs.graph_with_two_nodes import get_model 
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def healthcheck():
    return {"message": "Hello World"}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010,reload=True, debug=True)

import asyncio
from deep_researcher import DeepResearcher, LLMConfig
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY") 
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER")
SERPER_API_KEY  = os.getenv("SERPER_API_KEY")

print(OPENAI_API_KEY)
print(SEARCH_PROVIDER)
print(SERPER_API_KEY)

llm_config = LLMConfig(
    search_provider="serper",
    reasoning_model_provider="openai",
    reasoning_model="gpt-4o",
    main_model_provider="openai",
    main_model="gpt-4o",
    fast_model_provider="openai",
    fast_model="gpt-4o-mini"
)
query = "Provide a comprehensive overview of quantum computing"

researcher = DeepResearcher(max_iterations=3, max_time_minutes=5, config=llm_config)
report = asyncio.run(
    researcher.run(query)
)

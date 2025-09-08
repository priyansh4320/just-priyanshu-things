from autogen import ConversableAgent, LLMConfig
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm_config = LLMConfig(
    model="gpt-5-nano",
    api_key=OPENAI_API_KEY
)

agent = ConversableAgent(name="John",system_message="You are a helpful assistant",llm_config=llm_config)

response = agent.run(messages="hey there, how are you?")
response.process()
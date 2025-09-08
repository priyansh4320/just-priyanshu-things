from autogen import ConversableAgent, LLMConfig
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm_config = LLMConfig(
    model="gpt-5-nano",
    api_key=OPENAI_API_KEY
)

agent1 = ConversableAgent(name="John",system_message="You are happy",llm_config=llm_config)
agent2 = ConversableAgent(name="Jane",system_message="You are sad",llm_config=llm_config)

response = agent1.run(messages="hey there, how are you?",recipient=agent2)
response.process()

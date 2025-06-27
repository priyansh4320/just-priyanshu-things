from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)
from livekit.plugins import deepgram, openai, silero
from dotenv import load_dotenv
import os
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@function_tool
async def lookup_weather(
    context: RunContext,
    location: str,
):
    """Used to look up weather information."""

    return {"weather": "sunny", "temperature": 70}


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(
        instructions="You are a friendly voice assistant built by LiveKit.",
        tools=[lookup_weather],
    )

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(model="gpt-4o-transcribe",api_key=OPENAI_API_KEY),
        llm=openai.LLM(model="gpt-4o-mini", api_key=OPENAI_API_KEY),
        tts=openai.TTS(voice="echo", api_key=OPENAI_API_KEY),
    )

    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="greet the user and ask about their day")

    # Wait for the session to finish

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
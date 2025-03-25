import asyncio
import os
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoicePipelineAgent
from livekit.plugins import silero, openai, cartesia
from api import InterviewFnc
from database import SessionLocal, Candidate, Job
from prompts import INTRODUCTION_PROMPT, TECHNICAL_QUESTION_PROMPT, BEHAVIORAL_QUESTION_PROMPT, CLOSING_PROMPT, GREETING_PROMPT, SYSTEM_PROMPT

# Load environment variables
load_dotenv()

async def speak_response(interviewer, response_text):
    """Ensure AI speaks responses correctly and completely."""
    if response_text:
        await asyncio.sleep(0.2)  # Short pause for natural flow
        #await interviewer.say(response_text, allow_interruptions=False)
        speech_task = asyncio.create_task(interviewer.say(response_text, allow_interruptions=False))
        await speech_task
        #await asyncio.sleep(1.2)  # Extra delay to prevent overlapping responses

async def entrypoint(ctx: JobContext):
    db = SessionLocal()

    # Fetch the first available job and candidate
    candidate = db.query(Candidate).first()
    job = db.query(Job).first()

    if not candidate or not job:
        print("Error: No candidate or job found in the database.")
        return

    # Set up interview system prompt for LLM (NOT spoken aloud)
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=SYSTEM_PROMPT.format(job_title=job.title)
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = InterviewFnc(candidate_id=candidate.id, job_id=job.id)

    interviewer = VoicePipelineAgent(
        vad=silero.VAD.load(),
        stt=openai.STT.with_groq(model="whisper-large-v3", api_key=os.getenv("GROQ_API_KEY")),
        llm=openai.LLM.with_groq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY")),
        tts=cartesia.TTS(model="sonic-english", api_key=os.getenv("CARTESIA_API_KEY")),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )

    interviewer.start(ctx.room)

    # Introduction Phase
    await asyncio.sleep(1)
    await speak_response(interviewer, GREETING_PROMPT.format(candidate_name=candidate.name))
    await asyncio.sleep(1)
    await speak_response(interviewer, INTRODUCTION_PROMPT)

    # Ensure AI listens for responses before asking the next question
    async def process_response():
        while True:
            await asyncio.sleep(3)  # Delay before listening
            user_response = await interviewer.listen()

            if not user_response:
                continue  # Wait until candidate responds

            # Move to the next structured question
            next_question = await fnc_ctx.ask_question()
            
            if next_question == CLOSING_PROMPT:
                await speak_response(interviewer, CLOSING_PROMPT)
                break  # End interview

            await speak_response(interviewer, next_question)

    await process_response()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

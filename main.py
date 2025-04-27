#!/usr/bin/env python
import os

from dulwich.pack import chunks_length
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from pydub import AudioSegment
from pydub.utils import make_chunks
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from crews.gmail_crew.Email_crew import EmailCrew
from google import genai
import datetime
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class MeetingMinutesState(BaseModel):
    transcript: str = ""
    summary: str = ""


class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_audio(self):
        print("Generating transcript")
        SCRIPT_PATH = Path(__file__).parent
        audio_path = str(SCRIPT_PATH / "meeting.wav")
        audio = AudioSegment.from_file(audio_path,format="wav")
        chunk_length = 60000
        chunks = make_chunks(audio, chunk_length)
        prompt = 'Generate a transcript of the speech.'
        for i,chunk in enumerate(chunks):
            chunk_path = f"chunk{i}.wav"
            chunk.export(chunk_path, format="wav")
            my_file = client.files.upload(file=f'chunk{i}.wav')
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, my_file]
            )
            self.state.transcript+=response.text
        print(self.state.transcript)

    @listen(transcribe_audio)
    def meeting_minutes_crew(self):
        print("Generating Meeting Minutes")
        crew = MeetingMinutesCrew()

        inputs = {
            "transcript": self.state.transcript,
            "date":datetime.datetime.now().isoformat(),
        }
        meeting_minutes = crew.crew().kickoff(inputs)
        self.state.summary = str(meeting_minutes)
        print(self.state.summary)
    @listen(meeting_minutes_crew)
    def Emailing(self):
        crew = EmailCrew()
# Inject dynamic task input (bypassing YAML config)
        # Kick off
        crew.crew().kickoff(inputs={'summary': self.state.summary})

def kickoff():
    meeting_minutes_flow = MeetingMinutesFlow()
    meeting_minutes_flow.kickoff()
    meeting_minutes_flow.plot()

if __name__ == "__main__":
    kickoff()

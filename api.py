from livekit.agents import llm
from sqlalchemy.orm import Session
from database import SessionLocal, Job, Candidate, Response
from typing import Annotated
import logging
import csv
from prompts import INTRODUCTION_PROMPT, TECHNICAL_QUESTION_PROMPT, BEHAVIORAL_QUESTION_PROMPT, CLOSING_PROMPT, SYSTEM_PROMPT

logger = logging.getLogger("interviewer")
logger.setLevel(logging.INFO)

class InterviewFnc(llm.FunctionContext):
    def __init__(self, candidate_id: int, job_id: int):
        super().__init__()
        self.db: Session = SessionLocal()
        self.candidate = self.db.query(Candidate).filter(Candidate.id == candidate_id).first()
        self.job = self.db.query(Job).filter(Job.id == job_id).first()
        self.stage = "introduction"

    @llm.ai_callable(description="Ask an interview question based on job and candidate profile")
    def ask_question(self):
        if not self.candidate or not self.job:
            return "Error: Candidate or Job details not found."

        if self.stage == "introduction":
            self.stage = "technical"
            return INTRODUCTION_PROMPT.format()

        elif self.stage == "technical":
            self.stage = "behavioral"
            return TECHNICAL_QUESTION_PROMPT.format(
                experience=self.candidate.experience,
                projects=self.candidate.projects,
                education=self.candidate.education,
                skills=self.candidate.skills,
                job_description=self.job.description,
                job_requirements=self.job.requirements
            )

        elif self.stage == "behavioral":
            self.stage = "closing"
            return BEHAVIORAL_QUESTION_PROMPT.format(
                candidate_name=self.candidate.name,
                experience=self.candidate.experience
            )

        elif self.stage == "closing":
            return CLOSING_PROMPT.format(candidate_name=self.candidate.name)

    @llm.ai_callable(description="Save candidate response and export to CSV")
    def save_response(
        self,
        question: Annotated[str, llm.TypeInfo(description="The interview question asked")],
        response: Annotated[str, llm.TypeInfo(description="The candidate's answer")],
        score: Annotated[int, llm.TypeInfo(description="AI-assigned score (optional)")],
):
        if not self.candidate:
            return "Error: Candidate not found."

    # Save response in the database
        new_response = Response(candidate_id=self.candidate.id, question=question, response=response, score=score)
        self.db.add(new_response)
        self.db.commit()

    # Log the saved response to check if it's working
        print(f"[LOG] Saved response for {self.candidate.name}: {question} → {response} (Score: {score})")

    # Save response in CSV file
        csv_filename = f"interview_results_{self.candidate.name}.csv"
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.candidate.name, question, response, score])

        print(f"[LOG] Response saved to {csv_filename}")  # Log CSV save
        return "Response saved successfully!"

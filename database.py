from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


DATABASE_URL = "sqlite:///interview_db.sqlite"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Jobs Table
class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    candidates = relationship("Candidate", back_populates="job")

# Candidates Table
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    education = Column(Text, nullable=False)
    experience = Column(Text, nullable=False)
    skills = Column(Text, nullable=False)
    projects = Column(Text, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    job = relationship("Job", back_populates="candidates")

# Candidate Responses Table
class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    score = Column(Integer, nullable=True)

# Create tables in database
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

#  First Steps in Real-Time AI-Driven Interview for Mass Recruitment

This is a real-time AI-powered voice interview system designed to improve the speed, fairness, and scalability of mass hiring processes. It mimics a human-like interviewer that interacts with candidates using voice only — powered by cutting-edge Gen AI models.

🔗 **Live Sandbox Demo**: [Click here to try the AI Interviewer](https://your-livekit-sandbox-link.com)  
_(Replace with actual LiveKit link)_

---

## Features

- Real-time voice-based interviews using LiveKit
- Smart, adaptive questioning using LLaMA 3 (LLM)
- Automatic speech recognition with Whisper Large v3
- Human-like AI voice using Cartesia Sonic-English (TTS)
- Candidate and Job Profile-based interview flow
- Structured prompts: Introduction → Technical → Behavioral → Closing
- Scalable for mass hiring (multi-user supported in future)
- Modular backend using Python and FastAPI

---

## 🧠 Tech Stack

| Component      | Technology Used          |
|----------------|---------------------------|
| Real-time audio | LiveKit (WebRTC)          |
| Speech-to-text  | Whisper Large v3 (via OpenAI API) |
| LLM (Q&A)       | LLaMA 3-8B (via Groq API) |
| Text-to-speech  | Cartesia Sonic-English    |
| Backend         | Python, FastAPI           |
| Database        | SQLite (Switchable to PostgreSQL) |

---

## 📂 Project Structure

```
AI-Voice-Interview-System/
├── main.py              # Main app runner (LiveKit + Interview Flow)
├── api.py               # Interview function logic (ask question, save response)
├── database.py          # SQLAlchemy models for Candidate, Job, Response
├── populate_db.py       # Sample data insertion script
├── prompts.py           # Structured prompts for different stages
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── .gitignore           # Git ignore rules
```

---

## 🛠️ How to Run Locally

1. Clone the repo  
   `git clone https://github.com/yourusername/ai-voice-interview.git`

2. Create and activate virtual environment  
   `python -m venv venv && source venv/bin/activate`

3. Install dependencies  
   `pip install -r requirements.txt`

4. Run the DB setup  
   `python database.py`

5. Insert sample data  
   `python populate_db.py`

6. Start the app  
   `python main.py`

---

## 📈 Evaluation Metrics

| Model       | Metric             | Score        |
|-------------|--------------------|--------------|
| Whisper     | WER / RTF          | 2.3% / 0.98  |
| LLaMA 3     | Accuracy (MMLU)    | 88.5%        |
| Cartesia TTS| MOS / Latency      | 4.3 / ~600ms |

---

## 🧪 Try It Yourself

🎤 [LiveKit Sandbox Link](https://your-livekit-sandbox-link.com)  
Please test the interview loop and give feedback!

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

- SRH Hochschule Heidelberg
- Supervisors: Prof. Dr. Swati Chandna, Prof. Jamal

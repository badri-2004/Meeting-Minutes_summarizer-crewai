# Meeting Minutes Summarizer - CrewAI Project

![Built With](https://img.shields.io/badge/Built%20With-CrewAI-blue)

Automate the entire process of transcribing meeting audio, summarizing discussions, analyzing sentiment, writing full meeting minutes, and sending them via email — all powered by CrewAI and Google Gemini API.

---

## Features

- Automatic **audio transcription**
- Intelligent **discussion summarization**
- Extraction of **action items**
- **Sentiment analysis** of meetings
- **Meeting minutes writing**
- **Email delivery** of reports

---

## Project Structure

```
Meeting-Minutes_summarizer-crewai/
├── crews/
│   ├── gmail_crew/
│   └── meeting_minutes_crew/
├── meeting_minutes/ (optional workspace)
├── tools/ (optional workspace)
├── meeting.wav (input audio file)
├── main.py (main execution script)
├── report.md (generated meeting report)
├── README.md
├── .env (environment variables)
```

---

## About `crews/`

The `crews/` folder contains modular CrewAI configurations, where each Crew is a mini team made of specialized Agents.

### 1. `meeting_minutes_crew/`

Handles **meeting processing** tasks with 2 main agents:

| Agent Name                  | Responsibility |
|------------------------------|----------------|
| `meeting_minutes_summarizer` | Summarizes the transcript, extracts action items, and performs sentiment analysis. |
| `meeting_minutes_writer`     | Writes the final meeting minutes by combining summary, action items, and sentiment. |

Flow inside the crew:
- First summarize the entire transcript.
- Then extract key action points.
- Then detect the sentiment (positive, negative, neutral).
- Finally write a polished meeting report.

### 2. `gmail_crew/`

Handles **email delivery**:

| Agent Name | Responsibility |
|------------|-----------------|
| `emailer`  | Formats and sends the final meeting minutes to the configured email address. |

---

## Full Execution Flow (Behind the Scenes)

When you run `main.py`, the following happens:

1. **Audio Transcription**
    - Reads `meeting.wav`.
    - Splits into 60-second chunks.
    - Each chunk is sent to Google Gemini for transcription.
    - Chunks are combined to form the full meeting transcript.

2. **Meeting Minutes Summarization**
    - The transcript is fed to the `meeting_minutes_summarizer`.
    - Generates:
      - A short **summary**.
      - List of **action items**.
      - **Sentiment analysis** result.
    - Each output is saved to a file.

3. **Meeting Minutes Writing**
    - The `meeting_minutes_writer` reads the generated files.
    - Combines them into a **single polished meeting report**.
    - Report saved in `report.md`.

4. **Emailing the Report**
    - `emailer` agent picks up the report.
    - Formats it nicely.
    - Sends it via email automatically.

```markdown
![Flow plotted in crewai](path/to/your/sample-email-screenshot.png)
```
---
## Sample Output:

```markdown
![Sample Email Output](path/to/your/sample-email-screenshot.png)
```
---
 
## Installation

```bash
git clone https://github.com/yourusername/Meeting-Minutes_summarizer-crewai.git
cd Meeting-Minutes_summarizer-crewai
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

## Setup Environment Variables

Create a `.env` file in the root directory like this:

```dotenv
# .example.env
MODEL=Your_required_google_model
GEMINI_API_KEY=YOur_Gemini_api_key
GMAIL_USER=Your_user_name
GMAIL_PASS=authentication_key_from_mail
```

You can also just copy the provided `.example.env`:

```bash
cp .example.env .env
```

---

## Usage

1. Place your meeting audio file as `meeting.wav` in the project root.
2. Run the application:

```bash
python main.py
```
---
3. Outputs:
    - Full meeting transcript
    - Meeting summary
    - Action items
    - Sentiment report
    - Final meeting minutes file
    - Email sent to configured recipient

---


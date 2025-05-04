💇‍♀️ Salon AI Assistant (with Human-in-the-Loop Support)
This is an intelligent assistant for salons that can answer customer questions using predefined knowledge and learned responses. If the AI doesn't know an answer, it escalates the question to a human supervisor in real time. The supervisor's response is stored so the AI improves over time.

✨ Features
🧠 AI Assistant
Answers common questions using predefined knowledge (hours, pricing, stylists, booking policy, etc.)

Learns from supervisor-provided answers for unknown questions

🧑‍💼 Supervisor Dashboard
Real-time display of unanswered customer questions

Option to answer, hide, or delete questions

Newly provided answers are saved for future AI use

🔁 Real-Time Interaction
AI updates the customer with supervisor answers using polling

Flask-SocketIO and AJAX used for dynamic UI updates

🖥️ Dual Modes of Input
Console mode: Type questions and get responses

(Optional) Audio mode with LiveKit (under development/tested)


🚀 How It Works
🤖 When a customer asks a question:
The AI agent checks:

If it's a known question, it replies.

If not, it:

Saves the question to the DB.

Notifies the supervisor UI.

Tells the customer it is checking with a supervisor.

The supervisor UI:

Shows new questions immediately (via real-time updates).

Allows supervisors to:

Answer → Stored for future use by the AI.

Hide → Removes from list without learning.

Delete → Removes permanently.

The AI agent polls the DB to see if the supervisor answered.

Once answered, it responds to the customer.

🛠️ Setup Instructions
1. Clone the repo
bash
Copy
Edit
git clone [https://github.com/HARSHALSSSSS/human-in--loop](https://github.com/HARSHALSSSSS/human-in--loop)
cd salon_ai_assistant

3. Create and activate a virtual environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # on Windows

5. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt\

7. Run the supervisor UI
 
bash
Copy
Edit
cd supervisor_ui
python app.py

8. Run the AI agent (console mode)
bash
Copy
Edit
cd ../ai_agent
python agent.py

🔐 LiveKit Integration (Optional, Audio Mode)
Only needed if you're using the audio-based interaction.

Set your .env in the root or ai_agent/ with:

ini
Copy
Edit
LIVEKIT_API_KEY=your_key

LIVEKIT_API_SECRET=your_secret

LIVEKIT_URL=ws://localhost:7880

Install the LiveKit Python SDK (custom fork or official):

bash
Copy
Edit
pip install livekit-server-sdk
Serve the customer_ui/index.html from a basic HTTP server or integrate into Flask.

output screenshot :  ![Supervisor UI](https://github.com/HARSHALSSSSS/human-in--loop/blob/main/Screenshot%202025-05-04%20234836.png)

![Supervisor UI](https://github.com/HARSHALSSSSS/human-in--loop/blob/main/Screenshot%202025-05-04%20234842.png)

🔮 Future Improvements
✅ Replace polling with WebSocket-based real-time updates (more efficient)

🎙️ Full integration of LiveKit for audio rooms (currently stubbed)

📊 Add analytics for most common queries

✍️ Let supervisors edit or update past answers

🧑‍💻 Add authentication to supervisor dashboard


📷 UI Highlights

Supervisor UI

Live list of pending questions

"Answer", "Hide", and "Delete" buttons


Smooth real-time update experience via polling


Console AI


Clean input-response loop

Learns from human responses over time

🧠 Tech Stack
Component	Technology
Backend	Flask (Python)
Realtime UI	Flask-SocketIO, AJAX
Database	SQLite
AI Agent	Rule-based + Learned

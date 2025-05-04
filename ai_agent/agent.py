import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'supervisor_ui')))
from database import get_learned_answers, save_request, get_pending_requests
import asyncio
import json
from dotenv import load_dotenv
from livekit import rtc, api
from salon_info import SALON_INFO
from knowledge import SalonAgent
import requests  # 🔔 used to notify supervisor UI

load_dotenv()
agent = SalonAgent(SALON_INFO)

async def process_data_channel_message(participant, data_message):
    try:
        message = json.loads(data_message.data.decode('utf-8'))
        question = message.get('question')
        sender_id = message.get('sender')

        if question:
            answer = agent.answer_question(question)
            if answer:
                response = {'type': 'answer', 'text': answer, 'recipient': sender_id}
            else:
                response = {'type': 'request_help', 'question': question, 'recipient': sender_id}
                save_request(sender_id, question)

                # 🔔 Notify supervisor dashboard via HTTP POST
                try:
                    requests.post("http://localhost:5000/notify_new_request", json={
                        "sender": sender_id,
                        "question": question
                    })
                except Exception as e:
                    print(f"Failed to notify supervisor UI: {e}")

                print(f"⚠️ Requesting human assistance for: '{question}'")

            await participant.publish_data(json.dumps(response).encode('utf-8'), topic="salon")
    except Exception as e:
        print(f"Error: {e}")

async def poll_for_supervisor_answer(question):
    """Poll the DB to check if supervisor has answered."""
    print("🤖 AI: Let me check with my supervisor and get back to you...\n")
    for _ in range(30):  # check for up to 30 seconds
        await asyncio.sleep(2)
        pending = get_pending_requests()
        for req in pending:
            if req[2].strip().lower() == question.strip().lower():
                break  # still pending
        else:
            # not pending anymore
            answers = get_learned_answers()
            for q, a in answers:
                if q.strip().lower() == question.strip().lower():
                    return a
    return None

async def handle_console_input(agent):
    print("\n🎤 Type a question to simulate a customer.")
    print("Type 'exit' to quit.\n")

    while True:
        question = await asyncio.to_thread(input, "You: ")
        if question.lower().strip() == 'exit':
            print("👋 Exiting. Goodbye!")
            break

        answer = agent.answer_question(question)
        if answer:
            print(f"\n🤖 AI: {answer}\n")
        else:
            save_request("console_test_user", question)

            # 🔔 Notify supervisor dashboard
            try:
                requests.post("http://localhost:5000/notify_new_request", json={
                    "sender": "console_test_user",
                    "question": question
                })
            except Exception as e:
                print(f"Failed to notify supervisor UI: {e}")

            supervisor_response = await poll_for_supervisor_answer(question)
            if supervisor_response:
                print(f"\n🧑‍💼 Supervisor: {supervisor_response}\n")
            else:
                print("\n⚠️ Still waiting for a supervisor response...\n")

async def main():
    api_key = os.environ["LIVEKIT_API_KEY"]
    api_secret = os.environ["LIVEKIT_API_SECRET"]

    token = api.AccessToken(api_key, api_secret) \
        .with_identity("salon-ai-agent") \
        .with_name("Salon AI Assistant") \
        .with_grants(api.VideoGrants(room_join=True, room="salon-virtual-reception")) \
        .to_jwt()

    room = rtc.Room()

    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        print(f"Customer connected: {participant.identity}")
        @participant.on("data_received")
        def on_data_received(data):
            asyncio.create_task(process_data_channel_message(participant, data))

    await room.connect(os.getenv("LIVEKIT_URL"), token)
    print("✅ Salon AI Agent is online and ready!\n")

    # Start console input
    await handle_console_input(agent)

if __name__ == "__main__":
    asyncio.run(main())

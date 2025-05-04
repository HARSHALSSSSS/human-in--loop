
from salon_info import SALON_INFO
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'supervisor_ui'))

from database import get_learned_answers, save_learned_answer


class SalonAgent:
    def __init__(self, salon_info):
        self.salon_info = salon_info

    def answer_question(self, question):
        question = question.lower()
        learned = get_learned_answers()
        for q, a in learned:
            if q.lower() in question:
                return a

        if "hour" in question or "open" in question:
            return "\n".join([f"{day}: {hours}" for day, hours in self.salon_info['hours'].items()])
        elif "price" in question or "cost" in question or "service" in question:
            resp = ""
            for stype, opts in self.salon_info['services'].items():
                resp += f"{stype}:\n"
                for opt, val in opts.items():
                    resp += f" - {opt}: {val}\n"
            return resp
        elif "stylist" in question:
            return "\n".join([f"{s['name']} ({', '.join(s['specialties'])}) - {s['availability']}" for s in self.salon_info['stylists']])
        elif "book" in question or "cancel" in question:
            return self.salon_info["booking_policy"]
        elif "phone" in question or "address" in question:
            return f"{self.salon_info['phone']}, {self.salon_info['address']}"
        elif "about" in question:
            return f"{self.salon_info['name']}, located at {self.salon_info['address']}"
        return None

    def learn_answer(self, question, answer):
        save_learned_answer(question, answer)

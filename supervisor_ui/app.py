import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request, redirect
from database import get_pending_requests, resolve_request, get_resolved_requests
from database import save_learned_answer
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")  # 🟢 Use eventlet here

@app.route("/")
def index():
    requests = get_pending_requests()
    return render_template("index.html", requests=requests)


@app.route("/history")
def history():
    requests = get_resolved_requests()
    return render_template("index.html", requests=requests, view="resolved")


@app.post("/resolve")
def resolve():
    req_id_str = request.form["request_id"]
    answer = request.form["answer"]
    question = request.form["question"]

    if req_id_str == "new":
        # This is a new request not yet saved to DB, so we just save the answer
        save_learned_answer(question, answer)
    else:
        req_id = int(req_id_str)
        resolve_request(req_id, answer)
        save_learned_answer(question, answer)

    return redirect("/")


# Function to emit new request to supervisors
from flask import request

@app.route('/notify_new_request', methods=['POST'])
def notify_new_request():
    data = request.json
    question = data.get('question')
    if question:
        socketio.emit('new_request', {'question': question})
        return {'status': 'ok'}, 200
    return {'error': 'Missing question'}, 400

@app.post("/hide")
def hide():
    req_id = int(request.form["request_id"])
    from database import hide_request
    hide_request(req_id)
    return redirect("/history")

@app.post("/delete")
def delete():
    req_id = int(request.form["request_id"])
    from database import delete_request
    delete_request(req_id)
    return redirect("/history")

@app.post("/modify_request")
def modify_request():
    req_id = int(request.form["request_id"])
    action = request.form["action"]

    if action == "hide":
        from database import hide_request
        hide_request(req_id)
    elif action == "delete":
        from database import delete_request
        delete_request(req_id)

    return redirect("/history")




if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    eventlet.monkey_patch()
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)


import time
from ssh_handler import SshHandler
from timing import Timing
from flask import Flask, render_template, request

app = Flask(__name__)

def send_wol(timing):
    pass

def shutdown():
    pass


def get_server_minutes():
    #TODO the problem is that this is inside a container!
    #If this is a problem, it might be useful to change the base docker img
    cmd = "cat /run/systemd/shutdown/scheduled | head -n1"
    out, err = SshHandler.run_ssh_cmd("127.0.0.1", "", "", cmd)
    shutdown_time=str(out).split('=')[1][:-6] #TODO handle possible errors

# 0 OFF - 1 ON
def get_state_from_minutes(minutes):
    return 0 if minutes <= 0 else 1

@app.route("/")
def index():
    server_minutes = get_server_minutes()
    state = get_state_from_minutes(server_minutes)
    return render_template("index.html", state=state, minutes=server_minutes)


@app.route("/", methods=["POST"])
def command():
    action=request.form.get("action")
    print(f"Ricevuta: {action}", flush=True)
    timing = Timing()
    if action == "ON":
        timing = Timing(request.form.get("giorni"), request.form.get("ore"), request.form.get("minuti"))
        send_wol(timing)
    elif action == "OFF":
        shutdown()
    elif action == "KEEP_ON":
        timing = Timing(100, 0, 0)
        send_wol(timing)
    else:
        print("Action not found!", flush=True)

    minutes = timing.get_minutes()
    state = get_state_from_minutes(minutes)
    return render_template("index.html", state=state, minutes=minutes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

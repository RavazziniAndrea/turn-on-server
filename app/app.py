import time
from ssh_handler import SshHandler
from timing import Timing
from flask import Flask, render_template, request

app = Flask(__name__)

def send_wol(timing):
#TODO
# - if cannot connect 
#   - send wol
#   - wait until can ssh
# - set shutdown
    minutes = timing.get_minutes()
    print(f"mintuui: {minutes}", flush=True)
    cmd = "ls"
    out, err = SshHandler.run_ssh_cmd("", "", cmd)


def shutdown(timing):
    minutes = timing.get_minutes()
    print(f"mintuui: {minutes}", flush=True)
    cmd = "ls"
    out, err = SshHandler.run_ssh_cmd("", "", cmd)


def get_server_minutes():
    cmd = "cat /run/systemd/shutdown/scheduled | head -n1"
    out, err = SshHandler.run_ssh_cmd("", "", cmd)
    print(out, flush=True)
    print(err, flush=True)
    shutdown_time = 0
    if err == "":
        shutdown_time=out.split('=')[1][:-6] #TODO handle possible errors
        pritnt(f"shut time: {shutdown_time}")
    else:
        print(err)
    return shutdown_time

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
        shutdown(timing)
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

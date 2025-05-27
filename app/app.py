import time
import socket
from ssh_handler import SshHandler
from timing import Timing
from flask import Flask, render_template, request

app = Flask(__name__)

def wake_and_set(timing, keep_on=False):
#TODO
# - if cannot connect 
#   - send wol
#   - wait until can ssh
# - set shutdown
    if not keep_on:
        shutdown(timing)

def shutdown_now():
    shutdown(Timing())

def shutdown(timing):
    minutes = timing.get_minutes()
    cmd = f"sudo shutdown +{minutes}"
    out, err = SshHandler.run_ssh_cmd("10.0.42.250", "ravazz", cmd)


def get_server_shutdown_str() -> str:
    #TODO se non reaggiungibile, tornare "0"
    cmd = "sudo shutdown --show 2>&1"
    out, err = SshHandler.run_ssh_cmd("10.0.42.250", "ravazz", cmd)
    print(out, flush=True)
    print(err, flush=True)
    if out.startswith("No"): #No scheduled shutdown
        shutdown_str = "MAI"
    elif out == "OFF": #OFF (from run_ssh_cmd)
        shutdown_str = "OFF"
    else:
        shutdown_str = out[23:46]
        print(f"shut time: {shutdown_str}", flush=True)
    return shutdown_str


def render_page():
    shutdown_str = get_server_shutdown_str()
    return render_template("index.html", shutdown_str=shutdown_str)

@app.route("/")
def index():
    return render_page()

@app.route("/", methods=["POST"])
def command():
    action=request.form.get("action")
    print(f"Ricevuta: {action}", flush=True)
    timing = Timing()
    if action == "ON":
        timing = Timing(request.form.get("giorni"), request.form.get("ore"), request.form.get("minuti"))
        wake_and_set(timing)
    elif action == "OFF":
        shutdown_now()
    elif action == "KEEP_ON":
        wake_and_set(timing, True)
    else:
        print("Action not found!", flush=True)
    return render_page()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

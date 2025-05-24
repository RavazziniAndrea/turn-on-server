import time
from flask import Flask, render_template, request

app = Flask(__name__)

class Timing:
    def __init__(self, days=0, hours=0, minutes=0):
        self.days = int(days)
        self.hours = int(hours)
        self.minutes = int(minutes)
    
    def get_minutes(self):
        return self.days*24*60 + self.hours*60 + self.minutes

def turn_on(timing):
    send_wol()
    #TODO wait ma rimani in attesa che qualcuno possa spegnere
    #Magari continuare a pingare per vedere se ancora on 
    shutdown()

def send_wol():
    pass

def shutdown():
    pass

# 0 OFF - 1 ON
def get_server_state():
    return 0 

def get_server_minutes():
    return 200

@app.route("/")
def index():
    server_minutes = get_server_minutes()
    state = 0 if server_minutes <= 0 else 1
    return render_template("index.html", state=state, minutes=server_minutes)


@app.route("/", methods=["POST"])
def command():
    action=request.form.get("action")
    print(f"Ricevuta: {action}", flush=True)
    timing = Timing()
    if action == "ON":
        timing = Timing(request.form.get("giorni"), request.form.get("ore"), request.form.get("minuti"))
        turn_on(timing)
    elif action == "OFF":
        shutdown()
    elif action == "KEEP_ON":
        timing = Timing(100, 0, 0)
    else:
        print("Action not found!", flush=True)

    state = 0 if timing.get_minutes() <= 0 else 1
    return render_template("index.html", state=state, minutes=timing.get_minutes())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

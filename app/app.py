import time
from flask import Flask, render_template, request

app = Flask(__name__)

class Timing:
    def __init__(self, days=0, hours=0, minutes=0):
        self.days = days
        self.hours = hours
        self.minutes = minutes
    
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

@app.route("/")
def index():
    return render_template("index.html", message="OK")


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
        send_wol()
    else:
        print("Action not found!", flush=True)
    return render_template("index.html", days=timing.days, hours=timing.hours, minutes=timing.minutes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

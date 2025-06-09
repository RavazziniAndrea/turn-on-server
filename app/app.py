import time
import socket
from ssh_handler import SshHandler
from flask import Flask, render_template, request

app = Flask(__name__)



@app.route("/")
def index():
    out, err = SshHandler.run_ssh_cmd("uptime -p")
    is_on = "true" if out != "OFF" else "false"
    return render_template("index.html", status=is_on, time_on=out)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7001)

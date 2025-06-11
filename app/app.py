import time
import socket
from ssh_handler import SshHandler
import file_handler as fh
import gpio_handler as gh
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "ACCENDI":
            gh.turn_on_via_gpio()
            fh.write_status(fh.Status.OFF)
        else 
            SshHandler.shutdown_via_ssh()
            fh.write_status(fh.Status.OFF)

    out, err = SshHandler.run_ssh_cmd("uptime -p")
    is_on = "true" if out != "OFF" else "false"
    status = fh.get_status_from_file()
    if status == fh.Status.EMPTY:
        fh.write_status(fh.Status.ON.value if is_on else fh.Status.OFF.value)

    print(f"daje {status.value}")

    return render_template("index.html", status=is_on, time_on=out.strip())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7001)

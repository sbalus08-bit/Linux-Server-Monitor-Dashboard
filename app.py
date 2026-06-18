from flask import Flask, render_template
import psutil
import socket
import subprocess

app = Flask(__name__)

def check_service(service):

	result = subprocess.run(
		["systemctl", "is-active", service],
		capture_output=True, 
		text=True
		)

	return result.stdout.strip()

@app.route("/")
def dashboard():

	hostname = socket.gethostname()

	cpu = psutil.cpu_percent(interval=1)

	memory = psutil.virtual_memory().percent

	disk = psutil.disk_usage('/').percent

	uptime = psutil.boot_time()

	ssh_status = check_service("ssh")

	return render_template(
	"index.html",
	hostname=hostname,
	cpu=cpu,
	memory=memory,
	disk=disk,
	uptime=uptime
)

if __name__ == "__main__":
	app.run(debug=True)

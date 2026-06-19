from flask import Flask, render_template
import psutil
import socket
import subprocess
import time

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

	services = {
	"SSH": check_service("ssh"),
	"Docker": check_service("docker"),
	"Firewalld": check_service("firewalld"),
	"Cron": check_service("crond")
	}

	uptime_seconds = time.time() - psutil.boot_time()

	uptime_hours = round(uptime_seconds / 3600, 1)

	return render_template(
	"index.html",
	hostname=hostname,
	cpu=cpu,
	memory=memory,
	disk=disk,
	uptime=uptime_hours,
	services=services
)

@app.route("/api/system")
def api_system():

	services = {
		"ssh": check_service("ssh"),
		"docker": check_service("docker"),
		"firewalld": check_service("firewalld"),
		"crond": check_service("crond")
	}
	return {
		"cpu": psutil.cpu_percent(interval=1),
		"memory": psutil.virtual_memory().percent,
		"disk": psutil.disk_usage('/').percent,
		"services": services
	}

if __name__ == "__main__":
	app.run(debug=True)

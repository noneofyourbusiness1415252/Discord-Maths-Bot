from flask import Flask
from threading import Thread

app = Flask("Umar's Maths Bot")


@app.route("/")
def main():
	while True:
		pr = ""
		with open("discord.log", "r") as o:
			return o.read()


@app.route("/favicon.ico")
def ico():
	return render_template("favicon.ico")


def run():
	app.run(host="0.0.0.0", port=4040)


def keep_alive():
	server = Thread(target=run)
	server.start()

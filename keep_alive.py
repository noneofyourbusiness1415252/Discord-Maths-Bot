from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def main():
	while True:
		pr = ''
		with open('discord.log','r') as o:
			r = o.read()
		if r != pr:
			return r
			pr = r
def run():
	app.run(host="0.0.0.0", port=4040)
def keep_alive():
	server = Thread(target=run)
	server.start()
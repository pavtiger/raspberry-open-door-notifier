from threading import Thread
import json
import time
import os

import eventlet
from flask import Flask, send_from_directory, render_template

from ip import ip_address, port


# Init app
async_mode = None
app = Flask(__name__, static_url_path='')

door_status = None


# Return main page with door status
@app.route('/')
def root():
	global door_status
	
	return json.dumps({'success': True, 'door_status': door_status}), 200, {'ContentType': 'application/json'}
	

@app.route('/opened')
def open():
	global door_status
	
	print("Door open")
	door_status = "open"
	os.system("slock")
	return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/closed')
def close():
	global door_status
	
	door_status = "closed"
	print("Door closed")
	return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}



# Get files from server (e.g libs)
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


# We start a parallel thread for game logics. This loop is constantly running 
def game_loop(name):
    while True:
        # Process game logic here if you need to

        time.sleep(0.01)


if __name__ == "__main__":
    # This code and game_loop() are needed if you want to do wome tasks in background of the app (e.g. collision check)
    
    # eventlet.monkey_patch()
    # x = Thread(target=game_loop, args=(1,))
    # x.start()
    
    app.run(host=ip_address, port=port)


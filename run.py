from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pyautogui

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
pyautogui.FAILSAFE = True


# Serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


class ControlledComputer():
    # Global variables to store screen size
    website_screen_width, website_screen_height = 0, 0
    backend_screen_width, backend_screen_height = 0, 0
    x_scale, y_scale = 0, 0

    @socketio.on('screensize')
    def handle_mousemove(self, data):
        self.website_screen_width = data['width']
        self.website_screen_height = data['height']
        self.backend_screen_width, self.backend_screen_height = pyautogui.size()

        self.y_scale = self.backend_screen_width / self.website_screen_width
        self.x_scale = self.backend_screen_height / self.website_screen_height

def simulate_mousemove(x, y):
    c = ControlledComputer()
    # Simulate mouse movement to (x, y) coordinates
    x = x * c.x_scale
    y = y * c.y_scale
    pyautogui.moveTo(x, y)

def simulate_click(x, y):
    c = ControlledComputer()
    x = x * c.x_scale
    y = y * c.y_scale
    # Simulate mouse click at (x, y) coordinates
    pyautogui.click(x, y)    

@socketio.on('mousemove')
def handle_mousemove(data):
    #x = data['x']
    #y = data['y']
    simulate_mousemove(data['x'], data['y'])
    #print(f'Mousemove: x={x}, y={y}')

@socketio.on('click')
def handle_click(data):
    #x = data['x']
    #y = data['y']
    simulate_click(data['x'], data['y'])
    #print(f'Click: x={x}, y={y}')

def simulate_keydown(key):
    # Simulate keyboard key press
    pyautogui.keyDown(key)

def simulate_keyup(key):
    # Simulate keyboard key release
    pyautogui.keyUp(key)

@socketio.on('keydown')
def handle_keydown(data):
    #key = data['key']
    simulate_keydown(data['key'])
    #print(f'Keydown: key={key}')
    
@socketio.on('keyup')
def handle_keyup(data):
    #key = data['key']
    simulate_keyup(data['key'])
    #print(f'keyup: key={key}')

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

from m1 import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=False, port=2500)

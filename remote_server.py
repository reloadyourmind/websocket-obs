import asyncio
import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
from obs_controller import OBSController

app = Flask(__name__, static_folder='static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global OBS controller instance
obs_controller = None
logger = logging.getLogger(__name__)

def init_obs_controller(host="localhost", port=4455, password=""):
    global obs_controller
    obs_controller = OBSController(host, port, password)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Get all input devices from OBS"""
    if not obs_controller:
        return jsonify({"error": "OBS controller not initialized"}), 500
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        devices = loop.run_until_complete(obs_controller.get_input_devices())
        loop.close()
        
        devices_data = []
        for device in devices:
            devices_data.append({
                "name": device.name,
                "input_kind": device.input_kind,
                "volume_db": device.volume_db,
                "muted": device.muted
            })
        
        return jsonify({"devices": devices_data})
    except Exception as e:
        logger.error(f"Error getting devices: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/toggle/<input_name>', methods=['POST'])
def toggle_device(input_name):
    """Toggle input device on/off"""
    if not obs_controller:
        return jsonify({"error": "OBS controller not initialized"}), 500
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(obs_controller.toggle_input(input_name))
        loop.close()
        
        if success:
            return jsonify({"success": True, "message": f"Toggled {input_name}"})
        else:
            return jsonify({"error": f"Failed to toggle {input_name}"}), 500
    except Exception as e:
        logger.error(f"Error toggling device: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/volume/<input_name>', methods=['POST'])
def set_volume(input_name):
    """Set input device volume"""
    if not obs_controller:
        return jsonify({"error": "OBS controller not initialized"}), 500
    
    try:
        data = request.get_json()
        volume_db = data.get('volume_db', 0.0)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(obs_controller.set_volume(input_name, volume_db))
        loop.close()
        
        if success:
            return jsonify({"success": True, "message": f"Set {input_name} volume to {volume_db} dB"})
        else:
            return jsonify({"error": f"Failed to set volume for {input_name}"}), 500
    except Exception as e:
        logger.error(f"Error setting volume: {e}")
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected")
    emit('status', {'message': 'Connected to OBS Remote Control'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected")

@socketio.on('get_devices')
def handle_get_devices():
    """WebSocket handler for getting devices"""
    if not obs_controller:
        emit('error', {'message': 'OBS controller not initialized'})
        return
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        devices = loop.run_until_complete(obs_controller.get_input_devices())
        loop.close()
        
        devices_data = []
        for device in devices:
            devices_data.append({
                "name": device.name,
                "input_kind": device.input_kind,
                "volume_db": device.volume_db,
                "muted": device.muted
            })
        
        emit('devices', {'devices': devices_data})
    except Exception as e:
        logger.error(f"Error getting devices via WebSocket: {e}")
        emit('error', {'message': str(e)})

@socketio.on('toggle_device')
def handle_toggle_device(data):
    """WebSocket handler for toggling devices"""
    if not obs_controller:
        emit('error', {'message': 'OBS controller not initialized'})
        return
    
    input_name = data.get('input_name')
    if not input_name:
        emit('error', {'message': 'Input name required'})
        return
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(obs_controller.toggle_input(input_name))
        loop.close()
        
        if success:
            emit('device_toggled', {'input_name': input_name, 'success': True})
        else:
            emit('error', {'message': f'Failed to toggle {input_name}'})
    except Exception as e:
        logger.error(f"Error toggling device via WebSocket: {e}")
        emit('error', {'message': str(e)})

@socketio.on('set_volume')
def handle_set_volume(data):
    """WebSocket handler for setting volume"""
    if not obs_controller:
        emit('error', {'message': 'OBS controller not initialized'})
        return
    
    input_name = data.get('input_name')
    volume_db = data.get('volume_db', 0.0)
    
    if not input_name:
        emit('error', {'message': 'Input name required'})
        return
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(obs_controller.set_volume(input_name, volume_db))
        loop.close()
        
        if success:
            emit('volume_set', {'input_name': input_name, 'volume_db': volume_db, 'success': True})
        else:
            emit('error', {'message': f'Failed to set volume for {input_name}'})
    except Exception as e:
        logger.error(f"Error setting volume via WebSocket: {e}")
        emit('error', {'message': str(e)})

@app.route('/')
def index():
    """Serve the main web interface"""
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Initialize OBS controller
    init_obs_controller()
    
    # Run the server
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
#!/usr/bin/env python3
"""
OBS Remote Control Server Startup Script
This script starts the OBS remote control server with proper configuration.
"""

import sys
import logging
from config import *
from remote_server import app, socketio, init_obs_controller

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('obs_remote_control.log')
        ]
    )

def main():
    """Main startup function"""
    print("🎙️  OBS Remote Control Server")
    print("=" * 40)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize OBS controller
    logger.info(f"Initializing OBS controller for {OBS_HOST}:{OBS_PORT}")
    init_obs_controller(OBS_HOST, OBS_PORT, OBS_PASSWORD)
    
    # Start the server
    logger.info(f"Starting server on {SERVER_HOST}:{SERVER_PORT}")
    print(f"🌐 Web interface: http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"🔌 WebSocket: ws://{SERVER_HOST}:{SERVER_PORT}")
    print("Press Ctrl+C to stop the server")
    
    try:
        socketio.run(
            app, 
            host=SERVER_HOST, 
            port=SERVER_PORT, 
            debug=SERVER_DEBUG,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
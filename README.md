# OBS Remote Control System

A comprehensive remote control system for OBS Studio that allows you to manage input devices, adjust volume, and control OBS from remote PCs in your local network. Perfect for integration with Reaper and other DAWs.

## Features

- 🎙️ **Input Device Management**: Get information about all OBS input devices
- 🔊 **Volume Control**: Adjust volume levels for individual input devices
- 🔇 **Mute/Unmute**: Toggle input devices on/off
- 🌐 **Web Interface**: Beautiful, responsive web UI for remote control
- 🔌 **WebSocket Support**: Real-time communication with OBS
- 🎛️ **Reaper Integration**: Lua script for Reaper DAW integration
- 📱 **Network Access**: Control OBS from any device on your local network

## System Architecture

```
┌─────────────────┐    HTTP/WebSocket    ┌─────────────────┐
│   Remote PC     │ ◄──────────────────► │   OBS PC        │
│                 │                      │                 │
│ • Web Browser   │                      │ • OBS Studio    │
│ • Reaper        │                      │ • Remote Server │
│ • Mobile App    │                      │ • WebSocket     │
└─────────────────┘                      └─────────────────┘
```

## Installation

### Prerequisites

- Python 3.7+
- OBS Studio with WebSocket plugin enabled
- Network access between devices

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd websocket-obs
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OBS WebSocket**:
   - Open OBS Studio
   - Go to Tools → WebSocket Server Settings
   - Enable WebSocket server
   - Set port to 4455 (default)
   - Set password if desired

4. **Configure the remote control server**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Start the server**:
   ```bash
   python start_server.py
   ```

## Configuration

### Environment Variables (.env file)

```env
# OBS WebSocket Configuration
OBS_HOST=localhost
OBS_PORT=4455
OBS_PASSWORD=your_password_here

# Remote Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
SERVER_DEBUG=True

# Network Configuration
ALLOWED_ORIGINS=*

# Logging Configuration
LOG_LEVEL=INFO
```

### Network Setup

1. **Find your OBS PC's IP address**:
   ```bash
   # On Windows
   ipconfig
   
   # On Linux/Mac
   ifconfig
   ```

2. **Configure firewall** (if needed):
   - Allow incoming connections on port 5000
   - Allow OBS WebSocket on port 4455

## Usage

### Web Interface

1. Start the server on your OBS PC
2. Open a web browser on any device in your network
3. Navigate to `http://[OBS_PC_IP]:5000`
4. Use the web interface to control OBS input devices

### Reaper Integration

1. Copy `reaper_integration.lua` to your Reaper Scripts folder
2. Edit the script to set your OBS server IP address
3. Run the script from Reaper's Actions menu
4. Use the menu interface to control OBS devices

### API Endpoints

#### REST API

- `GET /api/devices` - Get all input devices
- `POST /api/toggle/<input_name>` - Toggle device mute state
- `POST /api/volume/<input_name>` - Set device volume

#### WebSocket Events

- `get_devices` - Request device list
- `toggle_device` - Toggle device
- `set_volume` - Set device volume

## File Structure

```
websocket-obs/
├── obs_controller.py      # OBS WebSocket controller
├── remote_server.py       # Flask server with WebSocket support
├── start_server.py        # Server startup script
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── reaper_integration.lua # Reaper DAW integration
├── static/
│   └── index.html        # Web interface
├── .env.example          # Environment variables template
└── README.md            # This file
```

## Troubleshooting

### Common Issues

1. **Connection refused**:
   - Check if OBS WebSocket is enabled
   - Verify port 4455 is not blocked
   - Check firewall settings

2. **No devices found**:
   - Ensure OBS has input devices configured
   - Check OBS WebSocket permissions
   - Verify OBS is running

3. **Network access issues**:
   - Check IP address configuration
   - Verify firewall settings
   - Test network connectivity

### Debug Mode

Enable debug mode by setting `SERVER_DEBUG=True` in your `.env` file for detailed logging.

## Security Considerations

- Change default passwords
- Use HTTPS in production
- Restrict network access as needed
- Keep OBS and dependencies updated

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review OBS WebSocket documentation
- Open an issue on GitHub
#!/usr/bin/env python3
"""
Test script to verify OBS WebSocket connection and get device information
"""

import asyncio
import sys
from obs_controller import OBSController

async def test_obs_connection():
    """Test OBS WebSocket connection and get device information"""
    print("🔍 Testing OBS WebSocket Connection")
    print("=" * 40)
    
    # Create OBS controller
    controller = OBSController()
    
    # Test connection
    print("Connecting to OBS...")
    connected = await controller.connect()
    
    if not connected:
        print("❌ Failed to connect to OBS")
        print("Please check:")
        print("1. OBS Studio is running")
        print("2. WebSocket server is enabled in OBS")
        print("3. Port 4455 is not blocked")
        return False
    
    print("✅ Connected to OBS successfully!")
    
    # Get input devices
    print("\n📋 Getting input devices...")
    devices = await controller.get_input_devices()
    
    if not devices:
        print("❌ No input devices found")
        print("Please check:")
        print("1. OBS has input devices configured")
        print("2. WebSocket permissions are correct")
        return False
    
    print(f"✅ Found {len(devices)} input device(s):")
    print("-" * 40)
    
    for i, device in enumerate(devices, 1):
        status = "🔇 MUTED" if device.muted else "🔊 ACTIVE"
        print(f"{i}. {device.name}")
        print(f"   Type: {device.input_kind}")
        print(f"   Volume: {device.volume_db:.1f} dB")
        print(f"   Status: {status}")
        print()
    
    # Test device control
    if devices:
        test_device = devices[0]
        print(f"🧪 Testing device control with '{test_device.name}'...")
        
        # Test volume control
        print(f"Setting volume to -10 dB...")
        success = await controller.set_volume(test_device.name, -10.0)
        if success:
            print("✅ Volume control test passed")
        else:
            print("❌ Volume control test failed")
        
        # Test mute toggle
        print("Toggling mute state...")
        success = await controller.toggle_input(test_device.name)
        if success:
            print("✅ Mute toggle test passed")
        else:
            print("❌ Mute toggle test failed")
    
    # Disconnect
    await controller.disconnect()
    print("\n✅ Test completed successfully!")
    return True

def main():
    """Main test function"""
    try:
        success = asyncio.run(test_obs_connection())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
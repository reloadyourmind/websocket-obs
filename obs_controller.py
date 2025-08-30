import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from obswebsocket import obsws, requests

@dataclass
class InputDevice:
    name: str
    input_kind: str
    volume_db: float
    muted: bool

class OBSController:
    def __init__(self, host="localhost", port=4455, password=""):
        self.host = host
        self.port = port
        self.password = password
        self.ws = None
        self.connected = False
        self.logger = logging.getLogger(__name__)
    
    async def connect(self):
        try:
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            self.connected = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return False
    
    async def get_input_devices(self) -> List[InputDevice]:
        if not self.connected:
            await self.connect()
        
        try:
            inputs_response = self.ws.call(requests.GetInputList())
            devices = []
            
            for input_info in inputs_response.datain['inputs']:
                name = input_info['inputName']
                kind = input_info['inputKind']
                
                volume_response = self.ws.call(requests.GetInputVolume(inputName=name))
                volume_db = volume_response.datain.get('inputVolumeDb', 0.0)
                
                mute_response = self.ws.call(requests.GetInputMute(inputName=name))
                muted = mute_response.datain['inputMuted']
                
                devices.append(InputDevice(name, kind, volume_db, muted))
            
            return devices
        except Exception as e:
            self.logger.error(f"Error getting devices: {e}")
            return []
    
    async def toggle_input(self, input_name: str) -> bool:
        if not self.connected:
            await self.connect()
        
        try:
            mute_response = self.ws.call(requests.GetInputMute(inputName=input_name))
            current_muted = mute_response.datain['inputMuted']
            
            self.ws.call(requests.SetInputMute(
                inputName=input_name, 
                inputMuted=not current_muted
            ))
            return True
        except Exception as e:
            self.logger.error(f"Error toggling {input_name}: {e}")
            return False
    
    async def set_volume(self, input_name: str, volume_db: float) -> bool:
        if not self.connected:
            await self.connect()
        
        try:
            self.ws.call(requests.SetInputVolume(
                inputName=input_name,
                inputVolumeDb=volume_db
            ))
            return True
        except Exception as e:
            self.logger.error(f"Error setting volume: {e}")
            return False
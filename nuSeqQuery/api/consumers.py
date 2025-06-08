from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import services

from asgiref.sync import sync_to_async


class SeqConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"action":"connection_status","message": "Connection established","status": "1"}))
        # You can add more logic here if needed when the connection is established

    async def disconnect(self, close_code):
        # Handle disconnection logic if necessary
        #print(f"Disconnected with code: {close_code}")
        pass;

    async def receive(self, text_data):
        data = json.loads(text_data)
        action= data.get("action", None);
        
        if action == "fetch_sequence":
            db_name = data.get('dataSource', None);
            queryid = data.get('queryId', None);
            rettype = data.get('rettype', None);
            
            if not db_name or not queryid or not rettype:
                response = {"action":action,"status": "0", "message": "Missing required parameters: dataSource, queryId, or rettype."}
                await self.send(text_data=json.dumps(response))
                return
            

            result = await sync_to_async(services.sequence_fetch)(db_name, rettype, queryid,self.channel_name);
            result.update({"action":action})
            await self.send(text_data=json.dumps(result));
            


        elif action == "sequence_analysis":
            pass;
        else:
            # If the action is not recognized, you can handle it accordingly
            response = {"error": "Invalid action specified"}
            await self.send(text_data=json.dumps(response))
            return
        
    async def task_update(self, text_data):
        
        text_data = text_data["content"]
        
        await self.send(text_data=json.dumps(text_data))  # Send a response back to the client
        
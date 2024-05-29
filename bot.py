# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import httpx
import json


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    # access_token =
    API_URL = "https://30b1-2405-201-4034-707e-383b-1866-9f37-4343.ngrok-free.app/api/messages"
    API_NEIO_URL = "https://zealert-api.westus2.cloudapp.azure.com/neiogpt/api/workspace/new-workspace-97693134/stream-chat"

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        async with httpx.AsyncClient() as client:
            response = await client.post(self.API_NEIO_URL, json={"message": user_message, "mode": "chat", "filter": None})
            response_text = response.text
            chunks = response_text.strip().split("data: ")

            if response.status_code == 200:
                # Process each chunk to find the desired response
                merge_result = ""
                for chunk in chunks:
                    if '"workspaceChat"' in chunk:
                        data = json.loads(chunk)
                        response_json = json.loads(
                            data["workspaceChat"]["chat"]["response"])
                        result_text = response_json["text"]
                        merge_result = result_text
                reply_text = merge_result
                # reply_text = api_response.get(
                #     "message", "No response from API")
            else:
                reply_text = "Error communicating with API"

        await turn_context.send_activity(reply_text)

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome to neio chat!")

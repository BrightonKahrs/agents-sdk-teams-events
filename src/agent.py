# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os.path as path
import re
import sys
import traceback
from dotenv import load_dotenv

from os import environ
from microsoft_agents.hosting.aiohttp import CloudAdapter
from microsoft_agents.hosting.core import (
    Authorization,
    AgentApplication,
    TurnState,
    TurnContext,
    MemoryStorage,
)
from microsoft_agents.authentication.msal import MsalConnectionManager
from microsoft_agents.activity import load_configuration_from_env
from microsoft_agents.activity import Activity
from microsoft_agents.hosting.teams import TeamsActivityHandler
from microsoft_agents.activity.teams import (
    MeetingStartEventDetails,
    MeetingEndEventDetails,
    MeetingParticipantsEventDetails,
)


load_dotenv()
agents_sdk_config = load_configuration_from_env(environ)

STORAGE = MemoryStorage()
CONNECTION_MANAGER = MsalConnectionManager(**agents_sdk_config)
ADAPTER = CloudAdapter(connection_manager=CONNECTION_MANAGER)
AUTHORIZATION = Authorization(STORAGE, CONNECTION_MANAGER, **agents_sdk_config)


AGENT_APP = AgentApplication[TurnState](
    storage=STORAGE, adapter=ADAPTER, authorization=AUTHORIZATION, **agents_sdk_config
)


@AGENT_APP.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, _state: TurnState):
    await context.send_activity(
        "Welcome to the empty agent! "
        "This agent is designed to be a starting point for your own agent development."
    )
    return True


@AGENT_APP.message(re.compile(r"^hello$"))
async def on_hello(context: TurnContext, _state: TurnState):
    await context.send_activity("Hello!")


@AGENT_APP.message(re.compile(r"^leave$"))
async def on_hello(context: TurnContext, _state: TurnState):
    await context.send_activity("Leaving call now. Thank you!")


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _state: TurnState):
    # Add logging for all message activities
    activity = context.activity
    print(f"\n📨 Message Activity:")
    print(f"  - Type: {activity.type}")
    print(f"  - Text: {activity.text}")
    print(f"  - Channel ID: {activity.channel_id}")

    await context.send_activity(f"you said: {context.activity.text}")


# Register event handlers directly with AgentApplication
@AGENT_APP.activity("event")
async def on_event_activity(context: TurnContext, _state: TurnState):
    """
    Handle Teams event activities including meeting events
    """
    activity = context.activity
    print(f"🔍 Event Activity Debug:")
    print(f"  - Activity Type: {activity.type}")
    print(f"  - Activity Name: {activity.name}")
    print(f"  - Channel ID: {activity.channel_id}")
    print(f"  - Activity Value: {activity.value}")

    # Handle meeting start events
    if activity.name == "application/vnd.microsoft.meetingStart":
        print("🚀 MEETING START EVENT RECEIVED!")
        await handle_meeting_start(context, activity.value)
        return True

    # Handle meeting end events
    elif activity.name == "application/vnd.microsoft.meetingEnd":
        print("� MEETING END EVENT RECEIVED!")
        await handle_meeting_end(context, activity.value)
        return True

    # Handle participant join events
    elif activity.name == "application/vnd.microsoft.meetingParticipantJoin":
        print("👥 PARTICIPANTS JOINED EVENT RECEIVED!")
        await handle_participants_join(context, activity.value)
        return True

    # Handle participant leave events
    elif activity.name == "application/vnd.microsoft.meetingParticipantLeave":
        print("👋 PARTICIPANTS LEFT EVENT RECEIVED!")
        await handle_participants_leave(context, activity.value)
        return True

    print(f"⚠️ Unhandled event activity: {activity.name}")
    return True


async def handle_meeting_start(context: TurnContext, meeting_data):
    """Handle meeting start event"""
    print(f"Meeting start data: {meeting_data}")

    # Send a message when the meeting starts
    await context.send_activity(
        "� Meeting has started! Welcome everyone to the meeting. "
        "I'm here to assist during your session."
    )


async def handle_meeting_end(context: TurnContext, meeting_data):
    """Handle meeting end event"""
    print(f"Meeting end data: {meeting_data}")

    # Send a message when the meeting ends
    await context.send_activity(
        "� Meeting has ended! Thank you for participating. Have a great day!"
    )


async def handle_participants_join(context: TurnContext, meeting_data):
    """Handle participants join event"""
    print(f"Participants join data: {meeting_data}")

    # Send a message when participants join
    await context.send_activity("� New participants joined the meeting!")


async def handle_participants_leave(context: TurnContext, meeting_data):
    """Handle participants leave event"""
    print(f"Participants leave data: {meeting_data}")

    # Send a message when participants leave
    await context.send_activity("👋 Participants left the meeting.")


@AGENT_APP.error
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")

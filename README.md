# Quickstart Agent

This is a sample of a simple Agent that is hosted on a Python web service. This Agent is configured to accept a request and echo the text of the request back to the caller.

This Agent Sample is intended to introduce you to the basic operation of the Microsoft 365 Agents SDK messaging loop. It can also be used as the base for a custom Agent you choose to develop.

## Prerequisites

- [Python](https://www.python.org/) version 3.9 or higher
- [ngrok](https://ngrok.com/) (for local development)

## Local Setup

### Configuration

1. [Create an Azure Bot](https://aka.ms/AgentsSDK-CreateBot)

   - Record the Application ID, the Tenant ID, and the Client Secret for use below

1. Configuring the token connection in the Agent settings

   1. Open the `env.TEMPLATE` file in the root of the sample project, rename it to `.env` and configure the following values:
   1. Set the **CONNECTIONS**SERVICE_CONNECTION**SETTINGS\_\_CLIENTID** to the AppId of the bot identity.
   1. Set the **CONNECTIONS**SERVICE*CONNECTION**SETTINGS\_\_CLIENTSECRET** to the Secret that was created for your identity. \_This is the `Secret Value` shown in the AppRegistration*.
   1. Set the **CONNECTIONS**SERVICE_CONNECTION**SETTINGS\_\_TENANTID** to the Tenant Id where your application is registered.

1. Configure the app manifest within the teams-bot-manifest.example folder

   1. Make sure to replace {YOUR_BOT_OR_SERVICE_PRINCIPAL_ID} and {YOUR_NGROK_DOMAIN} in the manifest example with your values

1. Run `ngrok` to create a secure tunnel to your local server:

   ```bash
   ngrok http 3978
   ```

1. Take note of the HTTPS forwarding URL (e.g., `https://abc123.ngrok.io`)

1. On the Azure Bot, select **Settings**, then **Configuration**, and update the **Messaging endpoint** to `{ngrok-url}/api/messages`

### Running the Agent

1. Start the Agent using `python -m src.main`

1. Open this folder from your IDE or Terminal of preference
1. (Optional but recommended) Set up virtual environment and activate it.
1. Install dependencies

```sh
pip install -r requirements.txt
```

### Run in localhost, anonymous mode

1. Start the application

```sh
python -m src.main
```

At this point you should see the message

```text
======== Running on http://localhost:3978 ========
```

The agent is ready to accept messages.

## Accessing the Agent

### Accessing app on teams

1. Upload the manifest through teams app developer portal (https://dev.teams.microsoft.com/apps) or directly as a sidecar in your teams environment.
2. Then create a teams meeting and wait for the meeting chat to load
3. From the meeting chat attendants list you will be able to add this bot to the meeting

## Further reading

To learn more about building Bots and Agents, see our [Microsoft 365 Agents SDK](https://github.com/microsoft/agents) repo.

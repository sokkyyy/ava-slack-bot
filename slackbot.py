from slackeventsapi import SlackEventAdapter
import slack
import os
from flask import Flask

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ.get('SLACK_SIGNING_SECRET'), '/slack/events', app)
client =  slack.WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))

@slack_events_adapter.on("message")
def handle_message(event_data):
    print('-' * 50)
    print(event_data)

    

    if 'subtype' in event_data["event"] and event_data["event"]["subtype"] == 'channel_join':\
        client.chat_postMessage(
			channel=event_data["event"]["channel"],
			blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hi, i am ava",
                    }
                }
            ]
		)

    message = event_data["event"]
    if message.get("subtype") is None and "BOT TEST" in message.get('text'):
        channel = message["channel"]
        send_message = "Responding to `BOT TEST` message sent by user <@%s>" % message["user"]
        client.chat_postMessage(channel=channel, text=send_message)

@slack_events_adapter.on('app_mention')
def handle_mention(event_data):
    print(event_data)
    client.chat_postMessage(
        channel=event_data["event"]["channel"],
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Someone mentioned my name :smiley:"
                }
            }
        ]
    )

@slack_events_adapter.on('im_created')
def im_created(event_data):
    print('x' * 20)
    print('im_created triggered')
    print(event_data)
    print('x' * 20)


@slack_events_adapter.on('im_close')
def im_close(event_data):
    print('x' * 20)
    print('im_close triggered')
    print(event_data)
    print('x' * 20)


@slack_events_adapter.on('im_open')
def im_open(event_data):
    print('x' * 20)
    print('im_open triggered')
    print(event_data)
    print('x' * 20)


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

if __name__ == "__main__":
    app.run(port=3000, debug=True)

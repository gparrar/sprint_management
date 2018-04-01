from slackclient import SlackClient
from constants import SLACK_TOKEN

def send_slack_message(message, channel):
    sc = SlackClient(SLACK_TOKEN)
    sc.api_call(
      "chat.postMessage",
      channel=channel,
      text=message
    )

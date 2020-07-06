"""
    Basic Slack Bot
    Date: 7/5/20
    Author: RJ Smith
    Use: Learning Python through building a slack application.
    Repo: https://github.com/tupleHunden/basic-slack-bot
    Resources Used: https://slack.dev/python-slackclient/
                    https://api.slack.com/start/overview/
"""

import os
import sys
import requests
from slack import WebClient
from slack.errors import SlackApiError
from dotenv import load_dotenv

# This will configure the dotenv file to read sensitive tokens for the slack bot
load_dotenv()

# The below will read the sensitive tokens from the dotenv file and assign them for use here.
SLACK_APP_ID = os.getenv("SLACK_APP_ID")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")
SLACK_CHANNEL_PROJECT = os.getenv("SLACK_CHANNEL_PROJECT")
SLACK_OAUTH_TOKEN = os.getenv("SLACK_OAUTH_TOKEN")

# This will create an instance of the slack bot, authenticated based off the auth token.
SLACK_BOT = WebClient(token=SLACK_OAUTH_TOKEN)


def get_member():
    """
        This function will pull the user names of the slack channel: Project
    """
    members = SLACK_BOT.conversations_members(channel=SLACK_CHANNEL_PROJECT)
    user_ids = members["members"]

    user_id_specific = user_ids[1]
    user_info_api = requests.get(f"https://slack.com/api/users.info?token="
                                 f"{SLACK_OAUTH_TOKEN}&user={user_id_specific}&pretty=1")

    if user_info_api.status_code != 200:
        sys.exit(f"Status Code Error on {user_info_api}")

    user_api_data = user_info_api.json()
    user_json = user_api_data["user"]
    user_name_json = user_json["name"].upper()

    try:
        SLACK_BOT.chat_postMessage(
            channel=SLACK_CHANNEL_PROJECT,
            text=f"Current non-bot Users: {user_name_json}"
        )
    except SlackApiError as slack_api_auth_error:
        sys.exit(slack_api_auth_error)


def get_taco():
    """
        This function will get a random taco recipe.
    """
    taco_api = requests.get("http://taco-randomizer.herokuapp.com/random/?full-taco=true")

    if taco_api.status_code != 200:
        sys.exit(f"Status Code Error on {taco_api}")

    return taco_api


def send_taco(taco_api):
    """
        This function will send the taco recipe to slack.
    """
    taco_data = taco_api.json()
    taco_url = taco_data["url"]
    taco_name = taco_data["name"].title()

    try:
        SLACK_BOT.chat_postMessage(
            channel=SLACK_CHANNEL_PROJECT,
            text=f"*Taco Name:* {taco_name}\n"
                 f"*Recipe URL:* {taco_url}",
        )
    except SlackApiError as slack_api_auth_error:
        sys.exit(slack_api_auth_error)


send_taco(taco_api=get_taco())

#!/usr/bin/env python
import sys
import requests
import secrets
import twitter


def main():
    api = initialize_bot()
    url, title = get_spell()
    message = build_message(url, title)
    post_status(api, message)


def initialize_bot():
    api = twitter.Api(
        consumer_key=secrets.consumer_key,
        consumer_secret=secrets.consumer_secret,
        access_token_key=secrets.access_token_key,
        access_token_secret=secrets.access_token_secret
    )
    return api


def post_status(api, message):
    try:
        status = api.PostUpdate(message)
    except UnicodeDecodeError:
        print("Your message could not be encoded. Perhaps it contains "
              "non-ASCII characters? Try explicitly specifying the encoding "
              "with the --encoding flag")
        sys.exit()
    print("{} just posted {}".format(status.user.name, status.text))


def get_spell():
    domain = "http://www.pjmcnally.net"
    payload = {"track": False, "key": secrets.twitterbot_key}

    r = requests.post(domain + "/spellbook/random_json", data=payload)
    data = r.json()

    url = domain + data["url"]
    name = data["name"]

    return url, name


def build_message(url, title):
    hashtags = "#DnD #DungeonsAndDragons"
    message = "Check out my #DnD5e Spell of the Day:\n\n{} at {}\n\n{}".format(
        title, url, hashtags)

    return message


if __name__ == '__main__':
    main()

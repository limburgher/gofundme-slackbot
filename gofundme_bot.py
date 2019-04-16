#!/usr/bin/python3
""" A simple script to post GoFundMe progress in a Slack channel """

# Copyright (C) 2017 Gwyn Ciesla

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import configparser
import requests
from slackclient import SlackClient

CONFIGFILENAME = 'config.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIGFILENAME)
SECTIONS = CONFIG.sections()

URL = str(CONFIG.get("Options", "url"))
GOAL = str(CONFIG.get("Options", "goal"))
SLACK_TOKEN = str(CONFIG.get("Options", "token"))
CHANNEL = str(CONFIG.get("Options", "channel"))

OUTPUT = requests.get(URL)
LINES = OUTPUT.text.split('\n')
COUNT = 0
TOTAL = "0"
for line in LINES:
    if 'of ' + GOAL + ' goal' in line:
        result = re.search('<strong>(.*)</strong>', LINES[COUNT-1])
        TOTAL = result.group(1)
        break
    COUNT = COUNT + 1

STATUS = TOTAL + ' of ' + GOAL + ' raised'

SLACK = SlackClient(SLACK_TOKEN)

SLACK.api_call(
    "chat.postMessage",
    channel=CHANNEL,
    text=STATUS
)

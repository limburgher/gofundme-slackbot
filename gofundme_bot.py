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

import requests
import sys
import re
from slackclient import SlackClient

GOAL = '$10,000'
URL = 'https://www.gofundme.com/aurorapride2018'

OUTPUT = requests.get(URL) 
LINES = OUTPUT.text.split('\n')
COUNT = 0
for line in LINES:
	if 'of ' + GOAL + ' goal' in line:
		result = re.search('<strong>(.*)</strong>', LINES[COUNT-1])
		TOTAL = result.group(1)
		break
	COUNT = COUNT + 1

STATUS = TOTAL + ' of ' + GOAL + ' raised'

with open('slack_token_gofundme.txt', 'r') as myfile:
	slack_token = myfile.read().replace('\n', '')

sc = SlackClient(slack_token)

sc.api_call(
	"chat.postMessage",
	channel="#lgbtq",
	text=STATUS
)
#	mmcli - Minimalist Mattermost command line client
#	Copyright (C) 2020-2020 Johannes Bauer
#
#	This file is part of mmcli.
#
#	mmcli is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	mmcli is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with mmcli; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import time
import json
import requests
import urllib.parse

class Mattermost():
	def __init__(self, base_uri):
		self._uri = base_uri
		self._sess = requests.Session()
		self._login_token = None

	def _request(self, uri, query = None, method = "GET", data = None):
		uri = self._uri + uri
		if query is not None:
			uri = uri + "?" + urllib.parse.urlencode(query)
		if data is not None:
			data = json.dumps(data)
		else:
			data = None
		headers = { }
		if self._login_token is not None:
			headers["Authorization"] = "Bearer %s" % (self._login_token)
		response = self._sess.request(method, url = uri, data = data, headers = headers)
		return response

	def set_login_token(self, token):
		self._login_token = token

	def login(self, username, password):
		data = {
			"login_id":		username,
			"password":		password,
		}
		response = self._request(method = "POST", uri = "/api/v4/users/login", data = data)
		user_object = response.json()
		user_object["token"] = response.headers["Token"]
		self._login_token = user_object["token"]
		return user_object

	def get_user(self, userid):
		response = self._request(uri = "/api/v4/users/%s" % (userid))
		return response.json()

	def get_teams(self, userid):
		response = self._request(uri = "/api/v4/users/%s/teams" % (userid))
		return response.json()

	def get_channels(self, teamid):
		response = self._request(uri = "/api/v4/teams/%s/channels" % (teamid))
		return response.json()

	def get_messages(self, channelid, after_postid = None, default_age_secs = 86400):
		query = { }
		if after_postid is not None:
			query["after"] = after_postid
		else:
			since = time.time() - default_age_secs
			query["since"] = str(round(since * 1000))

		response = self._request(uri = "/api/v4/channels/%s/posts" % (channelid), query = query)
		messages = response.json()

		return [ messages["posts"][postid] for postid in reversed(messages["order"]) ]

	def post_message(self, channelid, text):
		data = {
			"channel_id": channelid,
			"message": text,
		}
		response = self._request(uri = "/api/v4/posts", method = "POST", data = data)
		return response.json()

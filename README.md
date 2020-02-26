# mmcli
mmcli is a very minimalist Mattermost command line client. The idea is that it
enables you to chat on the command line using your Mattermost server, caching
as much data as possible. That means all fancy features such as editing posts
(or retrieval of changed posts) are intentionally omitted in order to keep
traffic as low as possible. This enables using Mattermost on a really low
bandwidth connection like an airplane, when the sheer traffic of all JavaScript
garbage that comes with the web version would just kill any possibility of ever
doing that.

## Usage
Configure your channel in config.json (the template is config_template.json),
then run the command line app. It shows messages and allows you to enter new
posts. Hit return after your last message and all will be sent in bulk. Note
that the password will need to be obfuscated, for that simply run `python3
Obfuscator.py` and enter it. Note that the passphrase is *not* encrypted, it is
merely obfuscated, i.e., it is trivial to get the password from that obfuscated
string. The idea is that if you accidentally `cat` your JSON file, it's not
blantly obvious what the passphrase is.

## License
GNU GPL-3.

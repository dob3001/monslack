# Monslack #

This application is a simple python script that checks for 4 conditions..

1. Does X appear in LOGS Y (logs, errorstrings)
2. Is the CPU load average above N threshold (usually 6, cpuwarnlevel)
3. How much free memory is left (memoryfree)
4. How much free disk space is left on partition X (diskwarnlvl, diskpaths)

I have expanded the basic checks so you can also directly poll the machine via a bot, the current propsed syntax is..

* BOTNAME SERVERNAME load
* BOTNAME SERVERNAME df
* BOTNAME SERVERNAME mem
* BOTNAME rollcall

You need to enable a bot and don't forget to invite the bot into the channel you wish it to listen to...

When installing I usually recommend on the host...

* mkdir -p /etc/monslack/
* Create your config.json in this folder (example below!)

To install you need to pass in the config.json, the volumes (maybe not root if your docker volumes reside on it) your monitoring and the log folders, so something like this..

LATEST DOCKER IMAGE: dob3001/monslack:0.4, https://hub.docker.com/r/dob3001/monslack/

```javascript
docker run -d -v /etc/monslack/config.json:/etc/monslack/config.json -v /var/lib/postgresql:/var/lib/postgresql -v /var/log/:/var/log/ --name monslack dob3001/monslack:0.4
```

```javascript
docker start monslack
```

## Example config.json ##

```javascript
{
  "hostname": "jamesbrain",
  "cpuwarnlevel": 6,
  "diskwarnlvl": 102400,
  "diskpaths": [ "/", "/var/lib/postgres" ],
  "logs": ["/var/log/somelog.log","/var/log/someother.log"],
  "memoryfree": 4096,
  "errorstrings": ["someError","SomeOtherError"],
  "webhookurl": "https://hooks.slack.com/services/1234556/ABCED/e367YYT90Tavy4stqnw3DF",
  "interval": 30,
  "webhook": {
    "username": "monkey-bot",
    "text": "PLACEHOLDER",
    "icon_emoji": ":monkey_face:",
    "channel": "#monitor"
  }
  "checks": {
    "disk": true,
    "cpu": true,
    "memory": true,
    "log": true
  }
  "bot": {
    "name": "monbot",
    "enabled": true,
    "channel": "somechannel",
    "token": "XXXXXXXXXX"
  }
}
```

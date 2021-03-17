AWsb clubhouse tiny tool for checking members

# Deploy
[heroku deploy doc](https://devcenter.heroku.com/articles/getting-started-with-python)

To get user_id,  token and device, by entering phone's sms code
```sh
CLUBHOUSE_PHONENUMBER=+12344456789 python tool.py
```
you will get config:set xxxx from commond above

```sh
heroku create
heroku config:set CLUBHOUSE_USER_ID=12343 CLUBHOUSE_USER_TOKEN=51279ece00ef0ebd8fa2d076752c9856af941dce CLUBHOUSE_USER_DEVICE=449E6094-D7CC-4EE4-AD51-01972695E081 
git push heroku main
heroku ps:scale web=1

heroku open
heroku logs --tail
```

# Heroku local

```sh
heroku local web
```

# Example
```
> curl --header "Content-Type: application/json" \
	--request POST \
	--data '["michael0o0", "bugfree", "amy", "michael1"]'\
	'http://127.0.0.1:5000/validate'
{
"data": {
	"members": ["bugfree", "michael0o0"],
	"no_members": ["amy", "michael1"]
	},
"ok": true
}
```

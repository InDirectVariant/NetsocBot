# NetsocBot
The official Discord bot for the Netsoc OT - Official Discord

## Features
* User verification based on Email
* Enforce naming rule - Determines first name and last initial on the email address provided
* Assigns grad year role based on provided value
* Confirms users have read the rules of the server before accepting their application
* More coming soon...

## Contributing
Do you have an idea for the bot? Want to clean up some messy code?

To contribute to the development of the Netsoc Bot you can fork and clone the master branch, make your changes, push your changes, then open a pull request to the master branch here

### Testing your code
You'll need your own bot token and owner ID. 

To obtain a bot token visit https://developer.discord.com then create an application, then a bot. From there you can find your token. Repalce `cfg["token"]` on Line 9 with your token

To obtain an owner ID you'll need to enable developer mode in Discord. Once done, right click your user in any server and click `Copy ID`. Replace `cfg["owner-id"]` on Line 13 with your ID

If you have any issues with the above please reach out to me on the Discord -> IDVariant#5643

## License
GNU GPLv3

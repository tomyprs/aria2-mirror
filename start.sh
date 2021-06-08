#!/bin/bash

# Check if bot is deployed to heroku
if [[ -n $DYNO ]]; then

	if [[ -n $CREDS_REPO && -n $GIT_TOKEN ]]; then
		git clone https://"$GIT_TOKEN"@"$CREDS_REPO" tmp;
		echo "Copy All token pickle to working Dir"
		mv -v tmp/*.pickle credentials.json /app/;
		echo "Copy Sa accounts to working Dir"
		mv -v tmp/accounts /app/accounts;
		echo " Cheking config.env is There or not, if three let's move"
		config="tmp/config.env"
		if [ -f "$config" ]
		then
			mv -v tmp/config.env /app/ && echo "Seting up config file.."
		else
			echo "$config not found.. skip process"
		fi
		rm -rf tmp
	else
		echo "Provide CREDS_REPO & GIT_TOKEN to Run the bot. Exiting..."
		exit 0
	fi
fi
echo " Starting Bot..."
./aria.sh; python3 -m bot

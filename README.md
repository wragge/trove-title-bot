# Trove Title Bot

Create a Twitter bot that tweets articles from selected [Trove](https://trove.nla.gov.au/) newspaper titles. For example, [@TroveTribuneBot](https://twitter.com/TroveTribuneBot) tweets items from the [Sydney Tribune](https://trove.nla.gov.au/newspaper/title/1002).

The bot tweets randomly-selected items.

For background information on this and other Trove bots see [Trove bots for all](http://101dhhacks.net/2018/01/21/trove-bots-for-all/).

## Getting prepared

There's a few things you need before you can set up your own bot.

* The numeric identifiers for the newspapers you want to tweet from
* A Trove API Key
* A Twitter account to send your tweets from
* A set of authorisation keys to use with your Twitter account

#### Identify your newspapers

The easiest place to get the id numbers of newspapers is from the [About digitised newspapers](http://trove.nla.gov.au/newspaper/about) page on Trove. If you click on a title, you'll open a new page which has the id of the newspaper at the end of the url. For example the page for the Sydney Tribune is:

``` http
http://trove.nla.gov.au/newspaper/title/1002
```

So the id number of the *Tribune* is `1002`.

#### Trove API Key

If you don't already have one, [sign up](https://trove.nla.gov.au/signup) for a Trove user account. Then just [follow the instructions](http://help.nla.gov.au/trove/building-with-trove/api) under 'How do I get an API key'. It's easy and takes just seconds.

Once your key has been assigned, you'll can find it again under the 'For developers' tab in your user profile.

#### Twitter account

You probably want to set up a brand new account for your bot to tweet from. If you already have an account you want to use then just skip this step.

Note that Twitter expects a unique email address for every account. So if you're already using your own email address to verify another Twitter account, you'll first need to set up a new email address for your bot. Just got to Google, or the provider of your choice and create a new email account.

You'll probably also need a mobile phone number to verify your new Twitter account. Fortunately, you can use one phone number across multiple accounts!

Once you've got your email and phone number ready, just click on the [sign up](https://twitter.com/signup) link on the Twitter home page and follow the instructions.

#### Twitter authorisation keys

To authorise your bot's tweets you need a set of application keys. Make sure you're logged into your new Twitter account, then go to [apps.twitter.com](https://apps.twitter.com/).

Click on the 'Create New App' button. Fill in the required fields. Just use a placeholder url like `http://example.com` for now -- you can update it later, once your bot is running. Check the TOC box and submit the form.

You've created an app -- now we just need the keys. Click on the 'Keys and Access Tokens' tab.

We need 4 keys or secret tokens:

* the Consumer Key
* the Consumer Secret
* the Access Token
* the Access Token Secret

The `Consumer Key` and `Consumer Secret` should be listed at the top of the page. Click on the 'Create my access token' button to generate the other two keys.

Keep this page open so you can cut and paste the keys into your application.

## Create your bot

Ok, that's all the boring set up stuff done. Now comes the fun part -- let's make a bot!

The process is simple, you just:

* Make your own copy of this app
* Add your own configuration values to the `.env` file

#### Copy this app

If you haven't already, now would be a good time to sign into Glitch so you can keep track of your projects. You can use a GitHub or Facebook account to sign in.

Just click on the huge 'Remix This' button below to create your very own copy of the `trove-title-bot` code. Easy!

<a href="https://glitch.com/edit/#!/remix/trove-title-bot">
  <img src="https://cdn.glitch.com/2bdfb3f8-05ef-4035-a06e-2043962a3a13%2Fremix%402x.png?1513093958726" alt="remix button" aria-label="remix" height="33">
</a>

#### Configure your bot

Glitch will automatically generate a new unique project name. If you want to change it, just click on the project name and enter a new value.

To get your bot up and going, all you need to fill is to fill in some values in the `.env` file. Click on the `.env` file in the side bar to open it for editing. You'll see something like this:

```
FLASK_APP=
FLASK_DEBUG=
TITLES=
APP_KEY=
TROVE_API_KEY=
CONSUMER_KEY=
CONSUMER_SECRET=
ACCESS_TOKEN=
ACCESS_TOKEN_SECRET=
```

You've already obtained your Trove API key and the 4 Twitter application keys, so it's just a matter of cutting and pasting them into the appropriate spots. Note there should be **no spaces** around the equals sign. It's also safest to put double quotes around your configuration values. So you should have something like:

```
CONSUMER_KEY="sTR@ngeC0mbinat10nofLetter5&number5"
```

The `APP_KEY` is used as a simple but not very secure way of controlling who can make your bot tweet. Tweets are triggered by visiting a particular url. The `APP_KEY` is added as a parameter to the url. Without it, the bot will just return an 'unauthorised' message. Set the `APP_KEY` to a string of your choice (just letters or numbers, no spaces). I'll explain how to use it later.

```
APP_KEY="magpiegoose"
```

`TITLES` is just the ids for one or more newspaper titles, separated by commas (no spaces!). So for @TroveTribuneBot it's just:

```
TITLES="1002"
```

If I wanted to tweet from both the *Tung Wah News* (id 1185) and the *Tung Wah Times* (id 1184), I'd put:

```
TITLES="1185,1184"
```

The other two configuration variables, `FLASK_APP` and `FLASK_DEBUG`, are only really necessary if you're setting up a bot to run in your local development environment. So you can safely ignore them.

## Test your bot

You bot should now be ready to start tweeting! Click on the 'Show' button at the top of the page. A new page will open with the message 'hello, I'm ready to tweet'. Your Trove title bot has one type of tweet:

* Tweet a random item from your newspaper/s


#### Random items

To tweet a random item from your newspaper/s just add `random/?key=[YOUR APP KEY]` to the url of the page that opens when you click 'Show'. So if my app's name was `loopy-lorax` and my app key was `magpiegoose`, I'd use the url:

``` http
https://loopy-lorax.glitch.me/random/?key=magpiegoose
```

If all goes well, you'll see a message saying 'ok, I tweeted something random'.

Check your Twitter account for your tweet!

#### Not working?

If your tweets don't appear, it could be that they're duplicates or longer that 280 characters. To check for other problems, click on the 'Logs' button in the sidebar and look for error messages

## Automate your bot

Yay, your bot is tweeting! But of course you don't want to have to manually load a url everytime you want to generate a new tweet. To automate your bot's behaviour you can use a 'web cron' service. You give these services a url, tell them how often to visit it, and they'll load the url automatically. For @TroveTribuneBot I'm using a free service called [cron-job.org](https://cron-job.org/en/). Search for 'web cron' if you want to explore the alternatives.

Just create an account with cron-job.org, or the service of your choice, and tell it to visit your bot's `random` url at a suitable frequency. 

## Potential problems

Unfortunately the Trove API is not as reliable or consistent as it should be. This means that some of the search requests made by the bot can take a long, long time (or die completely). If they take more than 30 seconds, Glitch will give up and close the connection. Web cron services impose a similar sort of time limit. This means that sometimes your tweets will fail. Until the Trove API gets a much-needed overhaul, there's not much that can be done about this. The good news is that no permanent damage is done to your bot, and it really doesn't matter much if it skips a tweet or two.

Your web cron service should report any errors so you can keep an eye on things. The Glitch logs will also note any recent timeouts.

## Hack this bot!

For some suggestions on how you can modify the code of this bot to customise its behaviour see [Trove bots for all](http://101dhhacks.net/2018/01/21/trove-bots-for-all/).

## Do you want more?

If you find this useful or interesting you might like to [support me on Patreon](https://www.patreon.com/timsherratt). The more supporters I get, the more time I can spend on making things like this!
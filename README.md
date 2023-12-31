### Classical Music Trivia Bot
This Twitter bot tweets a classical music related titbit.

It can be deployed as a Google cloud function. The tweet is currently derived based on the day, and Twitter won't let
you publish the same tweet again - so ensure that the periodicity is 24 hours at least if you are deploying on GCF.

### Development
The bot uses Tweepy to interact with the Twitter API. Firebase is the data store, and you can use the Firebase emulator
to try it locally.

### Getting your credentials
- Set up your Twitter developer account, create a Project and an App inside it
- Note down your consumer key and secret
- Create another Twitter account which will act as the bot. There are other approaches possible but this is the cleanest.
- Use Twurl https://github.com/twitter/twurl to authorize your app to be able to publish on behalf of the Bot account.
  Good instructions are in https://medium.com/@ponyenanu/how-to-associate-your-twitter-bot-with-a-dedicated-account-bbc1b154ba4e

Setup the following env vars. The first 2 you will get from your developer account. The last 2 from the output of twurl - usually
stored in ~/.twurlrc

export CONSUMER_KEY=\
export CONSUMER_SECRET=\
export ACCESS_TOKEN=\
export ACCESS_SECRET=

### Loading the data in Firebase
Add a line to invoke the fuction write(db) inside the main.py and run

```
GOOGLE_APPLICATION_CREDENTIALS=key.json python3 main.py
```
where key.json is your GCP service account JSON key with permissions for writing to Firebase.

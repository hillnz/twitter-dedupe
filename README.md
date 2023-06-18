twitter-dedupe
==============

Python library to retweet unique links from noisy Twitter accounts.

## Killed by Twitter

This project doesn't work due to Twitter's API changes. Original README follows.

## Acknowledgement

This is a fork of [cmheisel/twitter-dedupe](https://github.com/cmheisel/twitter-dedupe) with minimal changes to update for Python 3 and with updated dependencies.

Why this is needed
------------------------
Say you follow a news outlet that tweets the same link multiple times in a day, or a week. Maybe they provide different images or headlines, but it's the same story, over and over again.

I'd rather follow @{newsoutlet}-light and have a link show up there only once every 7 days or so.


How to use
-------------
1. Set up a Twitter account, say @{newsoutlet}lite
2. As @{newsoutlet}lite Follow @newsoutlet
3. Get your Twitter Consumer Key, Consumer Key Secret, Access Key and Access Key Secret from http://dev.twitter.com
4. Set up some environment variables
```
    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET
    # Only one of Redis/DynamoDB is needed. Redis will take precedence.
    REDISTOGO_URL=redis://{user}:{pass}@{domain}:{port}
    DYNAMODB_TABLE_NAME={some_table_name} # see notes below
    TWITTER_SCREEN_NAME={newsoutlet}lite
    WAIT_INTERVAL=300 # Time to wait between polls, in seconds
    LOG_LEVEL=WARN # Or INFO, OR DEBUG, etc.
```
5. python bin/logonly.py
6. Now you have a deamon running that'll examine @{newsoutlet}lites home timeline, and log any tweets it would retweet as @{newsoutlet}lite
7. If you're happy quit bin/logonly.py
8. Now run python bin/retweet.py

## DynamoDB

The table you specify must already exist. It must have a string partition key named "key".
Optionally, you should set "expires" as the field for TTL (time to live) support so that unused cache items are deleted.

For example, you can create a table with:
```
aws dynamodb create-table \
    --table-name {some_table_name} \
    --attribute-definitions AttributeName=key,AttributeType=S \
    --key-schema AttributeName=key,KeyType=HASH
```
And enable TTL with:
```
aws dynamodb update-time-to-live \
    --table-name {some_table_name} \
    --time-to-live-specification \
        AttributeName=expires,Enabled=true
```

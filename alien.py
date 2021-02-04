from __future__ import print_function

import uuid, json, logging, praw, time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate_feed(title, content, date, link):
    return {
        "uid": str(uuid.uuid4()),
        "updateDate": time.strftime("%Y-%m-%dT%H:%M:%S.0Z", time.gmtime(date)),
        "titleText": title,
        "mainText": title + " " + content,
        "redirectionURL": link,
    }

    
def lambda_handler(event, context):
    logger.info("before request")
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         password='',
                         user_agent='',
                         username='')
    logger.info("got reddit client")
    user = reddit.user.me()
    logger.info("authenticated as {}".format(user))
    if 'sub' not in event["queryStringParameters"]:
        return {
            "statusCode": 400
        }

    sub = event["queryStringParameters"]['sub']

    for submission in reddit.subreddit(sub).hot(limit=10):
        if not submission.stickied and not submission.pinned:
            break

    feed = generate_feed(submission.title,
                         submission.selftext,
                         submission.created_utc,
                         submission.url)

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
        },
        "body": json.dumps(feed)
    }


if __name__ == '__main__':
    print(lambda_handler(None,None))

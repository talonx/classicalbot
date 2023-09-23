import datetime
import json
import os.path
from datetime import date
from os import getenv

import functions_framework
import tweepy
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.Client(project="twitter-classical-bot")

GLOBAL_TAGS = '#ClassicalMusic'
# TODO remove this after dataset is complete
PADDING = 263


def read_json(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    return data


def write(db):
    """
    Loads the data into Firebase
    """
    data = read_json(os.path.join('data', 'data.json'))
    # print(data)

    composers = db.collection("composers")
    for d in data:
        ref = composers.document(d['id']).set(d)
        print(f'Added with {ref}')


def read(tid):
    tid = str(tid - PADDING)
    log(tid)
    coll = db.collection("composers")
    docs = coll.where(filter=FieldFilter("id", "==", tid)).stream()

    for r in docs:
        data = r.to_dict()
        return data


def todays_id():
    """
    Returns the number of the day today - e.g. Jan 3rd is 3
    """
    return date.today().timetuple().tm_yday


def log(param):
    print(f"{datetime.datetime.now()} : {param}")


def publish():
    tid = todays_id()
    data = read(tid)
    if data is None:
        log(f"No entry found for {tid}")
        return
    else:
        log(data)

    consumer_key = getenv("CONSUMER_KEY")
    consumer_secret = getenv("CONSUMER_SECRET")
    access_token = getenv("ACCESS_TOKEN")
    access_secret = getenv("ACCESS_SECRET")

    client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token,
                           access_token_secret=access_secret)

    tags = GLOBAL_TAGS
    for t in data['t']:
        tags = tags + ' #' + t
    try:
        response = client.create_tweet(text=data['d'] + tags)
        log(response)
    except Exception as e:
        log(e)


@functions_framework.http
def gcf_entrypoint(request):
    """
    Configure this entrypoint in GCF
    """
    publish()
    return 'OK'

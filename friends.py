from pymongo import MongoClient
import bson
from data import data
import simplejson as json

client = MongoClient('localhost', 27017)
db = client.script
posts = db.locationPosts_raw.find()

#Function to insert the location posts per user
def cleanLocationPosts(tagged_posts):
    try:
        result = {}
        result['user_id'] = tagged_posts['user_id']
        result['locations'] = []
        for item in tagged_posts['locations']:
            details = {}
            details['post_id'] = item['id']
            details['story'] = item['story']
            details['created_time'] = item['created_time']
            details['type'] = item['type']
            if ('place' in item):
                details['place'] = {}
                details['place']['id'] = item['place']['id']
                details['place']['location'] = item['place']['location']
                details['place']['name'] = (item['place']['name']).encode('utf8')

            if ('reactions' in item):
                details['reactions'] = []
                for react in item['reactions']['data']:
                    this_reaction = {}
                    this_reaction['name'] = (react['name']).encode('utf8')
                    this_reaction['id'] = react['id']
                    this_reaction['type'] = react['type']
                    details['reactions'].append(this_reaction)

            if ('comments' in item):
                details['comments'] = []
                for react in item['comments']['data']:
                    this_reaction = {}
                    this_reaction['message'] = (react['message']).encode('utf8')
                    this_reaction['from'] = {}
                    this_reaction['from']['id'] = react['from']['id']
                    this_reaction['from']['name'] = (react['from']['name']).encode('utf8')
                    this_reaction['id'] = react['id']
                    this_reaction['created_time'] = react['created_time']
                    details['comments'].append(this_reaction)

            if ('with_tags' in item):
                details['with_tags'] = []
                for react in item['with_tags']['data']:
                    this_reaction = {}
                    this_reaction['id'] = react['id']
                    this_reaction['name'] = (react['name']).encode('utf8')
                    details['with_tags'].append(this_reaction)

            if ('likes' in item):
                details['likes'] = []
                for react in item['likes']['data']:
                    this_reaction = {}
                    this_reaction['id'] = react['id']
                    this_reaction['name'] = (react['name']).encode('utf8')
                    details['likes'].append(this_reaction)

            if ('message' in item):
                details['message'] = (item['message']).encode('utf8')

            result['locations'].append(details)

        return result
    except KeyError:
        return 0


all_users = []
for item in posts:
    x = cleanLocationPosts(item)
    all_users.append(x)

with open('locationPosts.json', 'w') as f:
    json.dump(all_users, f)

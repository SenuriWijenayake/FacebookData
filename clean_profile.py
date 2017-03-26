from pymongo import MongoClient
import datetime

now = datetime.datetime.now()
client = MongoClient('localhost', 27017)
db = client.script

users_raw = db.users_raw
friends_raw = db.friends_raw

users = db.users
friends = db.friends

user_raw_collection = users_raw.find()
friends_raw_collection = friends_raw.find()

#function to clean the user profiles
def cleanProfile(user):
    profile = {}
    profile['id'] = user['id']
    profile['name'] = user['name']
    profile['birthday'] = user['birthday']
    profile['age'] = int(now.year) - int(user['birthday'][6:])
    profile['hometown'] = user['hometown']['name']
    education = []
    for item in user['education']:
        education.append(item['school']['name'])
    profile['education'] = education

    work = []
    if ('work' in user):
        for item in user['work']:
            work.append(item['employer']['name'])
        profile['work'] = work
    return profile

#Function to clean friends
def cleanFriends(friendlist):
    result = {}
    result['id'] = friendlist['user_id']
    result['total_count'] = friendlist['total_count']
    result['friends'] = []
    for friend in friendlist['friends']:
        result['friends'].append(friend['id'])
    return result

#Function to clean the location tagged posts
def cleanratings(ratings):
    result = {}
    result['user_id'] = ratings['user_id']
    result['prefs'] = []
    for rate in ratings['ratings']:
        result['prefs'].append({
            "post_id": rate['post_id'],
            "rating": float(rate['rating']),
            "place_id": rate['place_id'],
            "name": rate['name']
        })
    return result

#Function to insert the location posts per user
def cleanLocationPosts(tagged_posts):
    result = {}
    result['user_id'] = tagged_posts['user_id']
    result['locations'] = []
    for item in tagged_posts['locations']:
        details = {}
        details['post_id'] = item['id']
        details['place'] = item['place']
        details['story'] = item['story']
        details['created_time'] = item['created_time']
        details['type'] = item['type']

        if ('reactions' in item):
            details['reactions'] = item['reactions']['data']
        if ('comments' in item):
            details['comments'] = item['comments']['data']
        if ('with_tags' in item):
            details['with_tags'] = item['with_tags']['data']
        if ('likes' in item):
            details['likes'] = item['likes']['data']
        if ('message' in item):
            details['message'] = item['message']
        result['locations'].append(details)

    return result

#Function to insert the posts in the user feed
def cleanUserFeed(feed):
    result = {}
    result['user_id'] = feed['user_id']
    result['feed'] = []
    for item in feed['feed']:
        details = {}
        details['post_id'] = item['id']
        details['created_time'] = item['created_time']
        details['type'] = item['type']

        if ('reactions' in item):
            details['reactions'] = item['reactions']['data']
        if ('story' in item):
            details['story'] = item['story']
        if ('place' in item):
            details['place'] = item['place']
        if ('comments' in item):
            details['comments'] = item['comments']['data']
        if ('with_tags' in item):
            details['with_tags'] = item['with_tags']['data']
        if ('likes' in item):
            details['likes'] = item['likes']['data']
        if ('message' in item):
            details['message'] = item['message']
        result['feed'].append(details)

    return result

for user in user_raw_collection:
    profile = cleanProfile(user)
    users.insert(profile)

for friendlist in friends_raw_collection:
    result = cleanFriends(friendlist)
    friends.insert(result)



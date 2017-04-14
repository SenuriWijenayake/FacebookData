from pymongo import MongoClient
import datetime

now = datetime.datetime.now()
client = MongoClient('localhost', 27017)
db = client.script

users_raw = db.users_raw
friends_raw = db.friends_raw
users = db.users
users_coll = users.find()
friends = db.friends
user_raw_collection = users_raw.find()
friends_raw_collection = friends_raw.find()

my_list = ['158166681197693', '215316428921518', '338630779623841', '360967734276457', '493756514088788', '513289528839108', '597739390412259', '759906994089981', '833875256656786', '835185656506141', '844424082283172', '912365158899147', '1092144847486370', '1405712699730541', '1521301744793023', '1552234955028497', '1694166527479154', '1774500396108984']

#function to clean the user profiles
def cleanProfile(user):
    profile = {}
    profile['id'] = user['id']
    profile['name'] = user['name']
    if ('birthday' in user):
        profile['birthday'] = user['birthday']
        profile['age'] = int(now.year) - int(user['birthday'][6:])
    if ('hometown' in user):
        x = user['hometown']['name']
        y = x.split(',')
        profile['hometown'] = y[0]
    if ('gender' in user):
        profile['gender'] = user['gender']
    if ('religion' in user):
        profile['religion'] = user['religion']
    if ('education' in user):
        #Extract the most recent education
        final = len(user['education'])
        profile['education'] = user['education'][final-1]['school']['name']

    return profile

#Function to clean friends
def cleanFriends(friendlist):
    result = {}
    result['id'] = friendlist['user_id']
    result['total_count'] = friendlist['total_count']
    result['friends'] = []
    for friend in my_list:
        if(friendlist['user_id'] != friend):
            result['friends'].append(friend)
    return result

#Function to clean the location tagged posts
def cleanratings(ratings):
    result = {}
    result['user_id'] = ratings['user_id']
    result['prefs'] = []
    for rate in ratings['prefs']:
        rating = float(rate['rating'])
        result['prefs'].append({
            "post_id": rate['post_id'],
            "rating": rating,
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

preferences_raw = db.preferences_raw.find()
preferences = db.preferences

for user in preferences_raw:
    result = cleanratings(user)
    preferences.insert(result)

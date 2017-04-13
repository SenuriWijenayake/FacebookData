from pymongo import MongoClient
import datetime

now = datetime.datetime.now()
client = MongoClient('localhost', 27017)

db = client.script

users = db.users
feeds = db.feeds
friends = db.friends

active = '1665852693730402'
other = '223342168056157'

#Function to calculate the number of active user initiated posts on the friend
#Input Parameters : Active user id, Other user id
#Output : number of wall posts
def getWallPostsByActive(active,other):
    #Access the feed of the active user
    active_feed = feeds.find_one({'user_id': active},{'_id':0})
    other_posts = []

    for item in active_feed['feed']:
        if (item['from']['id'] == other):
            other_posts.append(item)
    return ({'posts' : other_posts,
             'length' : other_posts.__len__()})

#Function to calculate the total number of wall words (wall posts only)
#Input Parameters : Active user id, Other user id
#Output : number of wall words
def getWallWords(active,other):
    #Get wall posts initiated by the two users on each other
    x = ""
    y = ""
    other_on_active = getWallPostsByActive(active,other)
    active_on_other = getWallPostsByActive(other,active)

    for item in other_on_active['posts']:
        if('message' in item):
            x += x + item['message']
        if ('comments' in item):
            for com in item['comments']['data']:
                if ((com['from'] == other) or (com['from'] == active)):
                    x += x + com['message']

    for item in active_on_other['posts']:
        if('message' in item):
            y += y + item['message']
        if ('comments' in item):
            for com in item['comments']['data']:
                if ((com['from'] == other) or (com['from'] == active)):
                    y += y + com['message']


    return (len(x.split()) + len(y.split()))

#Function to calcalate the number of likes and comments between the two users
#Input Paramters : Two user ids
#Output : Number of times the users have liked and commented on each other
def getLikesAndComments(active,other):
    like_count = 0
    comm_count = 0
    active_feed = feeds.find_one({'user_id': active},{'_id':0})
    other_feed = feeds.find_one({'user_id': other},{'_id':0})

    for item in active_feed['feed']:
        if('likes' in item):
            for like in item['likes']['data']:
                if (like['id'] == other):
                    like_count += 1
        if('comments' in item):
            for comm in item['comments']['data']:
                if (comm['from']['id'] == other):
                    comm_count += 1

    for item in other_feed['feed']:
        if('likes' in item):
            for like in item['likes']['data']:
                if (like['id'] == active):
                    like_count += 1
    if('comments' in item):
            for comm in item['comments']['data']:
                if (comm['from']['id'] == active):
                    comm_count += 1

    return ({'like_count' : like_count, 'comment_count' : comm_count})

#Function to get the number of friends of a user
#Input : user id
#Outpt : number of friends
def getFriendCount(user):
    count = friends.find_one({'id' : user},{'_id':0,'total_count':1})
    return (count['total_count'])

#Function to get the last day since communication
#Input : two user ids
#Output : Number of days since last communications
def getLastCommunication (active,other):
    active_feed = feeds.find_one({'user_id': active},{'_id':0})
    other_feed = feeds.find_one({'user_id': other},{'_id':0})


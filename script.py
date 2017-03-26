import facebook
import requests
import simplejson as json

access_token = 'EAACEdEose0cBAPHd0tXuGMhJuZBPwLer6XCZCbrFmZC0RGcP1SrLZCLlWWbBYpzh3LRMhA5WRTGq4jcQpi6goS7M1ZA6ZB9bEXvcVnm2fOsZBHfCVOt4ozOlIoVSaKuut0qHuSfVhh67SUh8ZCk1qRqJiZCYTaVe2dZBNFt0HN31RQfTTRrqubMoEm1UBJl8Tn4TkZD'
user = '1665852693730402'
graph = facebook.GraphAPI(access_token)

profile = graph.get_object(user)
feed = graph.get_connections(profile['id'], 'feed')
my_feed = graph.get_connections(profile['id'], 'feed', **{'with':'location'})
friends = graph.get_connections(id='me', connection_name='friends')

loc_posts = []
all_friends = []
full_feed = []
location_ratings = []

print ("Downloading the user's public profile")
with open('profile.json', 'w') as f:
    json.dump(profile, f)

#Get all location tagged posts
while True:
    try:

        for post in my_feed['data']:
            loc_posts.append(post['id'])
            location_ratings.append({'id' : post['id'], 'name' : post['place']['name'], 'rating' : ''})
        my_feed = requests.get(my_feed['paging']['next']).json()

    except KeyError:
        break

posts = graph.get_objects(ids=loc_posts)
print ("You have " + str(posts.__len__()) + " location tagged posts")
with open('posts.json', 'w') as f:
    json.dump(posts, f)

print ("Lets now rate the locations you have visited! Please enter a rating between 1-5")
print ("1 : Poor")
print ("2 : Fair")
print ("3 : Good")
print ("4 : Very Good")
print ("5 : Excellent")

#Get the user's explicit rating for each location
for location in location_ratings:
     name = location['name']
     value = input("Rate (1-5) your experience at " + name + " : ")
     location['rating'] = value

with open('ratings.json', 'w') as f:
    json.dump(location_ratings, f)


#Get the friend list of the user
while True:
    try:
        for friend in friends['data']:
            all_friends.append(friend)
        friends = requests.get(friends['paging']['cursor']['next']).json()

    except KeyError:
        break

print ("You have " + str(posts.__len__()) + " friends using the application")
with open('friends.json', 'w') as f:
    json.dump(friends, f)

print ("Accessing the public feed")
#Get the feed of the user
while True:
    try:
        for post in feed['data']:
            full_feed.append(post['id'])
        feed = requests.get(feed['paging']['next']).json()

    except KeyError:
        break

len = full_feed.__len__()
print ("You have " + str(len) + " number of feed posts. Please be patient until the posts are collected")
if (len >= 1000):
    full_feed = full_feed[:50]

feed_arr = []
count = 0

for id in full_feed:
    try:
        feed_arr.append(graph.get_object(id))
        count += 1
        print ("Progress : " + str(count/50*100))

    except facebook.GraphAPIError:
        continue

with open('feed.json', 'w') as f:
    json.dump(feed_arr, f)
print ("Posts were successfully collected")




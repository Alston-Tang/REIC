from pymongo import MongoClient
import os

client = MongoClient()
db = client.reic

activities = db.activities
users = db.users

activity_list = activities.find()
user_list = users.find()

activity_inf = {}
activity_count = {}
work_dir = "/home/ubuntu/work_dir"
if not os.path.exists(work_dir):
    os.mkdir(work_dir);

for user in user_list:
    print_list = []
    if 'activity' in user:
        for activity in user['activity']:
            print_list.append(activity)
            if not activity in activity_count:
                activity_count[activity] = 0
            activity_count[activity] += 1
        if print_list:
            print ('user email: {0:30}  user name: {1:15} college: {2:15} year: {3:2} member: {4:2}').format(user['email'], user['username'], user['college'], user['year'], user['member'])
            print ('activity: '+ str(print_list))
            print ("=================================================================================================================")
print (activity_count)
                 
    

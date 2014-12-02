from pymongo import MongoClient
import sys

client = MongoClient()
db = client.reic

activities = db.activities
users = db.users

activity_list = activities.find()
user_list = users.find()

activity_inf = {}
activity_count = {}

for user in user_list:
    print_list = []
    cv = None
    if 'activity' in user:
        for activity in user['activity']:
            print_list.append(activity)
            print_list.append(user['activity'][activity]['time_slot'])
            cv = user['activity'][activity]['cv']
            if not activity in activity_count:
                activity_count[activity] = 0
            activity_count[activity] += 1
        if print_list:
            output = ('{0:30},{1:15},{2:15},{3:2},{4:2},{5},http://www.reichk.com/{6}').format(user['email'], user['username'], user['college'], user['year'], user['member'],user['tel'], cv)
            for item in print_list:
                output += (',' + item)
            print (output)
                 
    

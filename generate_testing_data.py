'''
This module is the main module, it will generate many data for sql performance 
study and testing :)
And it will do these things:
1. create 10000 users
2. the first 50 users create 300 channels
3. join random 1000 users to 50 channels
4. for each user create 10 consume type
5. and then create 100 consume plan
6. for each consume type, create 1000 consume items
'''
import random
import datetime

from app.database import init_db, db_session
from app.models.user import User
from app.models.channel import Channel

def generate_testing_data():
    name = "user_{0}"
    min_age = 17
    max_age = 70
    address = "address_{0}"
    job = "job_{0}"

    channel = "channel_{0}"
    channel_desc = "desc_{0}"
    min_level = 1
    max_level = 10

    print("create user and channel....")
    for i in range(10000):
        user = User.create_user(name=name.format(i),
                                age=random.randint(min_age, max_age),
                                address=address.format(i),
                                password="password",
                                job=job.format(i))
        if i < 50:
            user.create_channel(name=channel.format(i),
                                level=random.randint(min_level, max_level),
                                comment=channel_desc.format(i))
    
    print('make user join channel...')
    # join 1000 users to 50 channels
    for i in range(50):
        channel = Channel.get_channel(i+1)
        for j in range(i * 3 + 600, i * 3 + 1600):
            user = User.get_user(j)
            user.join_channel(i+1)

    # for 1000 user create 10 consume type
    # and then create 100 consume plan
    print('create consume type for 1000 users...')
    print('create 100 consume plan for each user')
    print('create 100 item for each user')

    type_name = 'type_{0}'
    comment = 'comment_{0}'
    plan_title = 'plan_title_{0}'
    item_title = 'item_title_{0}'

    for i in range(1000):
        user = User.get_user(i+1)
        for j in range(10):
            user.create_consume_type(type_name.format(j+1),
                                     comment.format(j+1))
            for k in range(j * 100, (j + 1) * 100):
                tmp_year = random.randint(2014, 2016)
                tmp_month = random.randint(1, 5)
                tmp_day = 1
                user.create_consume_plan(start_date=datetime.datetime(tmp_year, tmp_month, tmp_day),
                                         end_date=datetime.datetime(tmp_year, tmp_month + 3, tmp_day),
                                         money=random.randint(100, 500),
                                         title=plan_title.format(k),
                                         comment=comment.format(k),
                                         type_id=j+1
                                         )
            for l in range(j * 100, (j + 1) * 100):
                tmp_year = random.randint(2014, 2016)
                tmp_month = random.randint(1, 5)
                tmp_day = 1
                user.create_consume_item(datetime.datetime(tmp_year, tmp_month, tmp_day),
                                         money=random.randint(100, 500),
                                         title=item_title.format(l),
                                         comment=comment.format(l),
                                         type_id=j+1)

if __name__ == '__main__':
    init_db()
    generate_testing_data()    

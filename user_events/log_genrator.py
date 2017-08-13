"""
Generate Random user event documents by date 
Generate user event documents by size in each file
"""

import random
import string
from datetime import datetime,timedelta
import json
import os

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def randon_string_generator(size, type=None):
    if type == "char":
        chars = string.ascii_uppercase
    elif type == "string":
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    elif type == "number":
        chars = string.digits
        if chars[0] == '0':
            chars = chars[1:]
    return ''.join(random.choice(chars) for _ in range(size))

def main(**kwrags):
    try:
        for each in kwrags.get('list_of_log_entries'):
            file_name = each['log_name']
            try:
                log_dir = os.path.join('logs',file_name)
                f = open(log_dir, 'w')
                user_dict = {}
                for i in range(each['no_of_entries']):
                    event_name = random.choice(['view_product','add_to_cart','buy_now'])
                    product = randon_string_generator(2,'char')
                    price = randon_string_generator(3,'number')
                    event_date = random_date(kwrags.get('start_date'), kwrags.get('end_date'))
                    event_dict = {'event' :event_name,'product' :product, 'price' :price,'date' :event_date.strftime('%Y-%m-%d')}
                    user_dict = {
                    "uid" : int(randon_string_generator(3,'number')),
                    "name" : randon_string_generator(6,'char'),
                    "mobile" : randon_string_generator(10,'number'),
                    "age" : randon_string_generator(2,'number'),
                    "gender" : random.choice(['M','F']),
                    "events" : [event_dict]
                    }
                    f.write(json.dumps(user_dict)+'\n')
                f.close()
            except OSError as e:
                print (e)
                pass
    except KeyError as e:
        print (e)
        pass

if __name__ == "__main__":
    start_date = datetime.strptime('2017-08-01', '%Y-%m-%d')
    end_date = datetime.strptime('2017-08-14', '%Y-%m-%d')
    list_of_log_entries = [
        {"log_name" : "user_log1.log", "no_of_entries" : 10},
        {"log_name" : "user_log2.log", "no_of_entries" : 2000},
        {"log_name" : "user_log3.log", "no_of_entries" : 3000},
        {"log_name" : "user_log4.log", "no_of_entries" : 10000},
        {"log_name" : "user_log5.log", "no_of_entries" : 50000},
        {"log_name" : "user_log6.log", "no_of_entries" : 1000}
    ]
    main(start_date=start_date, end_date=end_date, list_of_log_entries=list_of_log_entries)
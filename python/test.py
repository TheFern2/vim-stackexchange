import requests
import secrets
import os
import errno
import json
import time
import sys

main_url = 'http://api.stackexchange.com/2.2'
main_site = 'stackoverflow'
client_id = '17697'
key = 'BptNntl7JkmV6xrE3tLaEA(('
data_dir = '../test_data'
access_token = secrets.access_token


def fetch_question_answers(site, id):
    answers_url = '/questions/%d/answers?order=desc&sort=activity&site=%s&filter=!nKzQURF6Y5' % (id, site)
    
    try:
        answers = requests.get(main_url + answers_url)
        answers_json = answers.json()
        print('hello')
        for item in answers_json['items']:
            print(item)
    except Exception:
        print("Failed to fetch question {}".format(id))
        sys.exit()
    print('How many answers {}'.format(len(answers_json)))

    items = answers_json['items']
    for index, item in enumerate(items):
        print('A{}. {}\n'.format(index, item['body']))

def fetch_favorites(site=main_site):
    # fetch if has_more is true then append items to file
    data = {}
    data['items'] = []
    has_more = 'True'
    page = 1
    
    while has_more:
        site_path = "{}/{}/".format(data_dir, site)

        if not os.path.exists(os.path.dirname(site_path)):
            try:
                os.makedirs(os.path.dirname(site_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        f=open("{}/{}/page{}.json".format(data_dir, site, page), "w+")
        # filter is to retrieve body of question too.
        favorites_url = '/me/favorites?page=%d&pagesize=100&order=desc&sort=activity&site=%s&access_token=%s&key=%s&filter=!9Z(-wwYGT' % (page, site, access_token, key)
        try:
            favorites = requests.get(main_url + favorites_url)
            favorites_json = favorites.json()
        except Exception as e:
            print("I dunno what's happening")
            sys.exit()
        
        has_more = favorites_json['has_more']
        json.dump(favorites_json, f)
        f.close()
        print("Has More {}, Number of Items {}".format(has_more, len(favorites_json['items'])))
        page += 1
        time.sleep(1) #


#fetch_favorites()
fetch_question_answers('askubuntu', 229589)
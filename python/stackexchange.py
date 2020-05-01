import requests
import secrets
import json
import time
from os.path import normpath, join
import imp
import os
#import vim

# need this to be able to test with vim and without vim
# though we don't want an error, is expected not to find vim
# when running python by itself, is a bit of a hack I suppose
# vim isn't really a module in sites folder
found = False
vim_test = True
try:
    imp.find_module('vim')
    found = True
except ImportError:
    pass

if found or vim_test:
    import vim
    plugin_root_dir = vim.eval('s:plugin_root_dir')
    data_dir = normpath(join(plugin_root_dir, '..', 'data'))
else:
    data_dir = '../data'

# test data
# /home/kodaman/git/vim-stackexchange/plugin/data/fav.json
# data_dir + '/data/fav.json'
# if not found:
#     try:
#         with open(data_dir + '/stackoverflow/page1.json') as f:
#             fav_data = json.load(f)
#     except:
#         pass

main_url = 'http://api.stackexchange.com/2.2'
main_site = 'stackoverflow'
client_id = '17697'
key = 'BptNntl7JkmV6xrE3tLaEA(('

access_token = secrets.access_token

def search(query, site=main_site):
    search_url = '/search/excerpts?order=desc&sort=activity&q=%s&site=%s' % (query, site) 
    questions = requests.get(main_url + search_url)
    return questions

def favorites(query=None, site=main_site):
    favorites_url = '/me/favorites?order=desc&sort=activity&site=%s&access_token=%s&key=%s' % (site, access_token, key)
    favorites = requests.get(main_url + favorites_url)
    favorites_query(query, favorites.json())
    return favorites

'''
    Filter favorites based on a query, search on tags, and title.
    Return new object as list of tuples
'''
def favorites_query(query, search_body=False, site=main_site):

    vim.command('vnew __stackexchange__')

    # count the number of files
    num_of_files = len(os.listdir("{}/{}".format(data_dir, site)))
    question_number = 1
    lines = []

    for index in range(num_of_files):
        try:
            with open('{}/{}/page{}.json'.format(data_dir, site, index + 1)) as f:
                data = json.load(f)

            for item in data['items']:
                tags = item['tags']
                title = item['title']
                question_id = item['question_id']
                link = item['link']
                body = item['body']

                # search for query in both lowercase, and capitalized
                # most people don't type in all caps, right?
                query_cap = query.capitalize()
                query_lower = query.lower()

                if ( query_lower in tags or query_lower in title
                    or query_cap in tags or query_cap in title ):
                    
                    vim.current.buffer.append("Q{}. {}".format(question_number, title))
                    #lines.append("Q{}. {}".format(question_number, title))
                    #_output_preview_text(lines)
                    #print(title)
                    #print(link)
                    #print(question_number)
                    question_number += 1
                    #print("---------------------------------")
                    continue

                if search_body:
                    if(query_lower in body or query_cap in body):
                        #print(title)
                        #print(link)
                        #print(question_number)
                        question_number += 1
                        #print("---------------------------------")

        except Exception as e:
            print(e)


def fetch_all_favorites_offline(site=main_site):

    # count the number of files
    num_of_files = len(os.listdir("{}/{}".format(data_dir, site)))
    question_number = 1

    if num_of_files == 0:
        print("Fetch data first!")
        return

    for index in range(num_of_files):
        try:
            with open('{}/{}/page{}.json'.format(data_dir, site, index + 1)) as f:
                data = json.load(f)

            for item in data['items']:
                tags = item['tags']
                title = item['title']
                question_id = item['question_id']
                link = item['link']
                body = item['body']
                
                print(title)
                print(link)
                print(question_number)
                question_number += 1
                print("---------------------------------")

        except Exception as e:
            print(e)


def fetch_favorites(site=main_site):
    # fetch if has_more is true then append items to file
    data = {}
    data['items'] = []
    has_more = 'True'
    page = 1
    
    while has_more:
        f=open("{}/{}/page{}.json".format(data_dir, site, page), "w+")
        # filter is to retrieve body of question too.
        favorites_url = '/me/favorites?page=%d&pagesize=100&order=desc&sort=activity&site=%s&access_token=%s&key=%s&filter=!9Z(-wwYGT' % (page, site, access_token, key)
        favorites = requests.get(main_url + favorites_url)
        favorites_json = favorites.json()
        has_more = favorites_json['has_more']
        json.dump(favorites_json, f)
        f.close()
        print("Has More {}, Number of Items {}".format(has_more, len(favorites_json['items'])))
        page += 1
        time.sleep(1) # delay to avoid getting kicked out of the api by too many quick requests
    

def say_hello(name):
    vim.current.buffer.append("Hello {}".format(name))


def close_buffer(buffer_name=None):
    #vim.command('bd! %s'.format(buffer_name))
    vim.command('bd! __stackexchange__')



#favorites('vim')
#favorites_query('git')
#favorites_query('pip')
#fetch_all_favorites_offline()
#fetch_favorites()

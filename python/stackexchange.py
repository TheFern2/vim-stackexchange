import requests
import secrets
import json
import time
from os.path import normpath, join
import imp
import os
import errno
import sys
import re
from HTMLParser import HTMLParser
import uuid
import vim

# class QuestionInfo:
#     def __init__(self, question_number):
#         self.question_number = question_number
#         self.question_line = 
#         self.body_start_line
#         self.body_end_line = 

class Question:
    def __init__(self, site, title, line_no, id, link):
        self.site = site
        self.title = title
        self.line_no = line_no
        self.id = id
        self.link = link

vim.current.buffer.append("hello loaded plugin")
questions_lst = {}

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
    temp_data_dir = normpath(join(plugin_root_dir, '..', 'temp'))
else:
    data_dir = '../data'

main_url = 'http://api.stackexchange.com/2.2'
main_site = 'stackoverflow'
client_id = '17697'
key = 'BptNntl7JkmV6xrE3tLaEA(('

access_token = secrets.access_token

def search(query, site=main_site):
    search_url = '/search/excerpts?order=desc&sort=activity&q=%s&site=%s' % (query, site) 
    questions = requests.get(main_url + search_url)
    return questions


def favorites_query(query, site=main_site, search_body=False):
    '''
        Filter favorites based on a query, search on tags, title, and body.
        Append questions to newly created buffer
    '''

    # get list of current buffers
    # if one from the dict doesn't match
    # then free up memory

    new_uuid = uuid.uuid1()
    questions_lst[str(new_uuid)] = []
    vim.command('e {}/{}'.format(temp_data_dir, str(new_uuid)))
    # vim.current.buffer.append('Current site: {}, search_body: {}'.format(site, search_body))

    # count the number of files
    num_of_files = len(os.listdir("{}/{}".format(data_dir, site)))
    question_number = 1
    # lines = []

    for index in range(num_of_files):
        # vim.current.buffer.append("Number of files: {}".format(num_of_files))
        try:
            with open('{}/{}/page{}.json'.format(data_dir, site, index + 1)) as f:
                data = json.load(f)

            # vim.current.buffer.append("Python version {}.{}".format(sys.version_info.major, sys.version_info.minor))

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
                    #vim.current.buffer.append(" {}".format(test_body))
                    #lines.append("Q{}. {}".format(question_number, title))
                    #_output_preview_text(lines)
                    #print(title)
                    #print(link)
                    #print(question_number)
                    question_number += 1
                    questions_lst[str(new_uuid)].append(Question(site, title, question_number, question_id, link))
                    #print("---------------------------------")
                    continue

                if search_body:
                    if(query_lower in body or query_cap in body):
                        #print(title)
                        #print(link)
                        #print(question_number)
                        question_number += 1
                        questions_lst[str(new_uuid)].append(Question(site, title, question_number, question_id, link))
                        #print("---------------------------------")

        except Exception as e:
            print('favorites_query() error: {}'.format(e))


def open_question():
    cb = vim.current.buffer
    current_window = vim.current.window
    pos = current_window.cursor
    curr_line = pos[0] - 2
    buff_name = os.path.basename(cb.name)

    vim.command('vnew __question__')
    vim.current.buffer.append('Curr buffer name {}'.format(cb.name))

    if curr_line >= 0 and curr_line <= len(questions_lst[buff_name]):
        # vim.command('vnew __question_{}__'.format(questions_lst[cb.name][curr_line].id))
        # prob put link at top
        vim.current.buffer.append(questions_lst[buff_name][curr_line].link)
        vim.current.buffer.append('')
        vim.current.buffer.append(questions_lst[buff_name][curr_line].title)
        vim.current.buffer.append('')
        fetch_question_answers(questions_lst[buff_name][curr_line].site, questions_lst[buff_name][curr_line].id)


def fetch_question_answers(site, id):
    answers_url = '/questions/%d/answers?order=desc&sort=activity&site=%s&filter=!nKzQURF6Y5' % (id, site)
    
    try:
        answers = requests.get(main_url + answers_url)
        answers_json = answers.json()
    except Exception:
        print("Failed to fetch question {}".format(id))
        sys.exit()

    vim.current.buffer.append('')
    # vim.current.buffer.append('How many answers {}'.format(len(answers_json['items'])))

    items = answers_json['items']
    for index, item in enumerate(items):
        vim.current.buffer.append('')
        vim.current.buffer.append('Answer {}'.format(index + 1))
        # clean_text = remove_html_tags(item['body'])
        parser = HTMLParser()
        clean_text = parser.unescape(item['body'])
        clean_text = remove_html_tags(clean_text)
        split_lines = clean_text.split('\n')
        vim.current.buffer.append(split_lines)


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


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
        
        # filter is to retrieve body of question too.
        favorites_url = '/me/favorites?page=%d&pagesize=100&order=desc&sort=activity&site=%s&access_token=%s&key=%s&filter=!9Z(-wwYGT' % (page, site, access_token, key)
        try:
            favorites = requests.get(main_url + favorites_url)
            favorites_json = favorites.json()
            f=open("{}/{}/page{}.json".format(data_dir, site, page), "w+")
            json.dump(favorites_json, f)
            f.close()
        except Exception:
            print("Failed to fetch questions {}".format(id))
            sys.exit()
        has_more = favorites_json['has_more']        
        print("Has More {}, Number of Items {}".format(has_more, len(favorites_json['items'])))
        page += 1
        time.sleep(1) # delay to avoid getting kicked out of the api by too many quick requests
    

def say_hello(name="John"):
    vim.current.buffer.append("Hello {}".format(name))


def close_buffer():
    #vim.command('bd! %s'.format(buffer_name))
    vim.command('bd!')



#favorites('vim')
#favorites_query('git')
#favorites_query('pip')
#fetch_all_favorites_offline()
#fetch_favorites()

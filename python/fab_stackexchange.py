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
import uuid
import shutil
import vim

try:
    from html.parser import HTMLParser  # Python 3
except ModuleNotFoundError:
    from HTMLParser import HTMLParser  # Python 2

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

questions_lst = {}  # uuid -> [Question]
plugin_root_dir = vim.eval('s:plugin_root_dir')
data_dir = normpath(join(plugin_root_dir, '..', 'data'))
temp_data_dir = normpath(join(plugin_root_dir, '..', 'temp'))

if not os.path.exists(temp_data_dir):
    os.mkdir(temp_data_dir)
else:
    shutil.rmtree(temp_data_dir)
    os.mkdir(temp_data_dir)

if not os.path.exists(data_dir):
    os.mkdir(data_dir)
    

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
        Append questions to a list, file will be created on plugin dir/temp
        And opened in a new buffer
    '''
    new_uuid = uuid.uuid1()
    questions_lst[str(new_uuid)] = []
    perform_query(query, site, new_uuid, search_body)


def perform_query(query, site, new_uuid, search_body):
    parser = HTMLParser()
    json_path = "{}/{}".format(data_dir, site)
    json_files = [f for f in os.listdir(json_path) if os.path.isfile(os.path.join(json_path, f))]
    question_number = 1
    lines = []

    for file in json_files:
        try:
            with open(os.path.join(json_path, file)) as f:
                data = json.load(f)
        except Exception as e:
            print('favorites_query() error: {}'.format(e))

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
                
                # vim.current.buffer.append("Q{}. {}".format(question_number, title))
                clean_title = parser.unescape(title)
                clean_title = remove_html_tags(clean_title)
                lines.append("Q{}. {}\n".format(question_number, clean_title))
                question_number += 1
                questions_lst[str(new_uuid)].append(Question(site, clean_title, question_number, question_id, link))
                continue

            if(query_lower in body and search_body or query_cap in body and search_body):
                clean_title = parser.unescape(title)
                clean_title = remove_html_tags(clean_title)
                lines.append("Q{}. {}\n".format(question_number, clean_title))
                question_number += 1
                questions_lst[str(new_uuid)].append(Question(site, clean_title, question_number, question_id, link))


    # output to file
    with open('{}/{}'.format(temp_data_dir, str(new_uuid)), 'w') as out_file:
        out_file.writelines(lines)
    vim.command('edit {}/{}'.format(temp_data_dir, str(new_uuid)))       


def open_question():
    cb = vim.current.buffer
    current_window = vim.current.window
    pos = current_window.cursor
    curr_line = pos[0] - 1
    buff_name = os.path.basename(cb.name)
    lines = []

    if curr_line >= 0 and curr_line <= len(questions_lst[buff_name]):
        lines.append(questions_lst[buff_name][curr_line].link + "\n\n")
        lines.append("Question: " + questions_lst[buff_name][curr_line].title + "\n\n")
        answer_lines = fetch_question_answers(questions_lst[buff_name][curr_line].site, questions_lst[buff_name][curr_line].id)
        lines.extend(answer_lines)
        lines.append('{}'.format(sys.version_info))

        # output to file
        new_uuid = uuid.uuid1()
        string_lines = []

        if sys.version_info.major >= 3:
            for line in lines:
                try:
                   string_lines.append(line.decode('utf-8'))
                except (UnicodeDecodeError, AttributeError):
                    string_lines.append(line)
        else:
            string_lines = lines

        with open('{}/{}'.format(temp_data_dir, str(new_uuid)), 'w') as out_file:
            out_file.writelines(string_lines)

        vim.command('edit {}/{}'.format(temp_data_dir, str(new_uuid)))


def fetch_question_answers(site, id):
    answers_url = '/questions/%d/answers?order=desc&sort=activity&site=%s&filter=!nKzQURF6Y5' % (id, site)
    lines = []
    
    try:
        answers = requests.get(main_url + answers_url)
        answers_json = answers.json()
    except Exception:
        print("Failed to fetch question {}".format(id))
        sys.exit()

    items = answers_json['items']
    items.sort(key=lambda x: x['score'], reverse=True)
    for index, item in enumerate(items):
        if item['is_accepted']:
            lines.append('Answer {} Accepted, Score {}\n\n'.format(index + 1, item['score']))
        else:
            lines.append('Answer {}, Score {}\n\n'.format(index + 1, item['score']))
        parser = HTMLParser()
        clean_text = parser.unescape(item['body'])
        clean_text = remove_html_tags(clean_text)       
        split_lines = clean_text.split('\n')
        for line in split_lines:
            if sys.version_info.major >= 3:
                lines.append(line.encode('utf-8') + b'\n')
            else:
                lines.append(line.encode('utf-8') + '\n')

    return lines


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def clean_data_dir():
    pass


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

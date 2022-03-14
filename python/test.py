import requests
import secrets
import os
import errno
import json
import time
import sys
import uuid
from HTMLParser import HTMLParser
import uuid

main_url = 'http://api.stackexchange.com/2.2'
main_site = 'stackoverflow'
client_id = '17697'
key = 'BptNntl7JkmV6xrE3tLaEA(('
data_dir = '../data'
temp_data_dir = '../temp'
access_token = secrets.access_token

questions_lst = {}  # uuid -> [Question]
query_lst = {}      # query -> uuid

class Question:
    def __init__(self, site, title, line_no, id, link):
        self.site = site
        self.title = title
        self.line_no = line_no
        self.id = id
        self.link = link


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

def favorites_query(query, site=main_site, search_body=False):
    '''
        Filter favorites based on a query, search on tags, title, and body.
        Append questions to newly created buffer
    '''

    # get list of current buffers
    # if one from the dict doesn't match
    # then free up memory

    if query in query_lst:
        #vim.command('edit {}/{}'.format(temp_data_dir, query_lst[query]))
        print('Query file found {}/{}'.format(temp_data_dir, query_lst[query]))
    else:
        new_uuid = uuid.uuid1()
        questions_lst[str(new_uuid)] = []
        query_lst[str(new_uuid)] = query
        perform_query(query, site, new_uuid, search_body)


def perform_query(query, site, new_uuid, search_body):
    num_of_files = len(os.listdir("{}/{}".format(data_dir, site)))
    question_number = 1
    lines = []

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
                    
                    # vim.current.buffer.append("Q{}. {}".format(question_number, title))
                    lines.append("Q{}. {}".format(question_number, title))
                    # lines.append('test')
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
                        lines.append("Q{}. {}".format(question_number, title))
                        # lines.append('test2')
                        question_number += 1
                        questions_lst[str(new_uuid)].append(Question(site, title, question_number, question_id, link))


            # output to file
            with open('{}/{}'.format(temp_data_dir, str(new_uuid)), 'w') as out_file:
                out_file.writelines(lines)
            # vim.command('edit {}/{}'.format(temp_data_dir, str(new_uuid)))
            print('Query file created {}/{}'.format(temp_data_dir, str(new_uuid)))

        except Exception as e:
            print('perform_query() error: {}'.format(e))

def open_question():
    cb = vim.current.buffer
    current_window = vim.current.window
    pos = current_window.cursor
    curr_line = pos[0] - 1
    buff_name = os.path.basename(cb.name)
    lines = []

    # vim.command('vnew __question__')
    # vim.current.buffer.append('Curr buffer name {}'.format(cb.name))

    if curr_line >= 0 and curr_line <= len(questions_lst[buff_name]):
        # vim.command('vnew __question_{}__'.format(questions_lst[cb.name][curr_line].id))
        # prob put link at top
        lines.append(questions_lst[buff_name][curr_line].link)
        lines.append(questions_lst[buff_name][curr_line].title)
        answer_lines = fetch_question_answers(questions_lst[buff_name][curr_line].site, questions_lst[buff_name][curr_line].id)
        lines.extend(answer_lines)

        # output to file
        new_uuid = uuid.uuid1()
        with open('{}/{}'.format(temp_data_dir, str(new_uuid)), 'w') as out_file:
            out_file.writelines(lines)
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

    # vim.current.buffer.append('')
    # vim.current.buffer.append('How many answers {}'.format(len(answers_json['items'])))

    items = answers_json['items']
    for index, item in enumerate(items):
        lines.append('Answer {}'.format(index + 1))
        # clean_text = remove_html_tags(item['body'])
        parser = HTMLParser()
        clean_text = parser.unescape(item['body'])
        clean_text = remove_html_tags(clean_text)       
        split_lines = clean_text.split('\n')
        lines.extend(split_lines)
        # vim.current.buffer.append(split_lines)

    return lines


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


#fetch_favorites()
# fetch_question_answers('askubuntu', 229589)
favorites_query('cron', 'askubuntu')

favorites_query('cron', 'askubuntu')
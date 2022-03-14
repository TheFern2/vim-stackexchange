# My dev notes

http://vimdoc.sourceforge.net/htmldoc/if_pyth.html
https://vimhelp.org/if_pyth.txt.html

https://stackoverflow.com/questions/11405996/how-can-i-use-python-to-replace-html-escape-characters

## Favorites are fetched from online to an offline cache

favorites_url = '/me/favorites?page=%d&pagesize=100&order=desc&sort=activity&site=%s&access_token=%s&key=%s&filter=!9Z(-wwYGT' % (page, site, access_token, key)

## Queries are done in the offline cache

## Flow of getting data

- Retrieve favorites per site
- When cmd to open a question is triggered
    - Retrieve question id answers ids
    - Then retrieve answers by those ids

# Get Answers per question id

/questions/{ids}/answers
/2.2/questions/56683/answers?order=desc&sort=activity&site=askubuntu&filter=!nKzQURF6Y5
!nKzQURF6Y5 

## TODO

- open new question and answers in new buffer - More or less done
- add from date to query - fromdate is post creation and edit, not favorited date :(
- query all sites
- fan out question body
- dataclass to keep track of question start end lines
- favorite / unfavorite question
- data and temp dirs creation in code - done

## March 13 2022

new query
- Open new queries in new buffers, s_ex_uuid
- might be easier to save queries to files in plugin temp dir

- test in python3

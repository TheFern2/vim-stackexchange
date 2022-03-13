# My dev notes

http://vimdoc.sourceforge.net/htmldoc/if_pyth.html
https://vimhelp.org/if_pyth.txt.html

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

- open new question and answers in new buffer (WIP)
- add from date to query
- query all sites
- fan out question body
- dataclass to keep track of question start end lines
- favorite / unfavorite question
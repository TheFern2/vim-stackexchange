## vim-stackexchange

> SO changed their web pages to say bookmarks now, after being called favorites for so many years. Funny enough not too long after I started working on this project they changed the name. The API 2.2 still says favorites, for me they will always be favorites.

A Vim plugin for searching questions in any stackexchange site.
It can also download all your favorites for any site, and be able to filter them. Say goodbye to your browser while you are in vim!

## Requirements

- vim (I've tested on neovim, let me know if is not compatible with vim)
- python2
- requests package

## Setup

You'll need a token key in order to take advantage of this plugin, some requests can get by without token but is very limited. Is quite easy to get setup. Login to stackoverflow or any site from stackexchange, then copy and paste the below link.

```
https://stackexchange.com/oauth/dialog?client_id=17697&scope=no_expiry,write_access&redirect_uri=https://stackexchange.com/oauth/login_success/
```

If you were logged in, you'll get an access token back in the url.

Inside the python folder, create a `secrets.py` file and replace with your token:

```
access_token="your_access_token"
```

https://api.stackexchange.com/docs/authentication#scope
https://api.stackexchange.com/docs/write

## Install plugin with vim-plug

For now it is locally managed, I haven't tested the official way. Add `vim-stackexchange` to your vim configuration.

```
" Unmanaged plugin (manually installed and updated)
Plug '~/git/sample-plugin'
Plug '~/git/vim-stackexchange'

```

## Vim Commands

These are the current vim commands:

- SEFetchFavorites (stackoverflow is the default site). This command will fetch all your favorites, and store them in the `plugin_dir/data/site`

Examples:

```
:SEFetchFavorites
:SEFetchFavorites askubuntu
```

- SEFavoritesQuery (stackoverflow is the default site. This will search on your local favorites without fetching online)

Examples:

```
:SEFavoritesQuery query
:SEFavoritesQuery query askubuntu
```

- CloseBuffer (Just closes the buffer vim-stackexchange opened, same as `q!`)

## Query Examples

After running fetch commands for stackoverflow, and askubuntu.

Stackoverflow query of python favorites:

![stackoverflow](/images/stackoverflow.png)

Askubuntu query of cron favorites:

![askubuntu](/images/askubuntu.png)

## DONE

- Fetching favorites from any stackexchange site, tested on stackoverflow, askubuntu
  - Data is saved under plugin directory
- Query a search, and show in a new buffer

## TODO

- Fan out to show full question with a shortcut
- Open full question and answers on another buffer
- Polish commands for favorites

## Documentation

http://vimdoc.sourceforge.net/htmldoc/if_pyth.html

# NB: Not ready for release. Still work in progress.

# hackmd2jekyll

## What is this?

1. crawl your hackmd notes automatically
2. generate static site using jekyll
3. deploy to your website ( now support heroku... )

TODO
1. support Github Page

## Example

Example site

hackmd: https://hackmd.io/MYDmFYHYE4DZILQBMBmSDMCAsIkFMEBDEcTcfYLWY2AI2miA?view

heroku: http://oalieno-blog.herokuapp.com/

## Install

the project is just python script ready to execute, but you need to install something first

#### jekyll

follow the instructions on https://jekyllrb.com/ to setup jekyll

#### heroku

follow the instructions on https://andycroll.com/ruby/serving-a-jekyll-blog-using-heroku/ to upload your site to heroku

if you got this error: `... does not have a valid date in the YAML front matter`

solution : `exclude: [..., vendor]` in `_config.yml` ( from https://github.com/jekyll/jekyll/issues/2938 )

## Config

edit `config.py` for some custom value

time_gap: update frequency ( second )

links_hash: your target list hackmd-hash

upload_script: currently just `upload-heroku.sh`

## Get start

**each note in hackmd is identify by a hash ( the one in the url ), we call it hackmd-hash**

put all your notes hackmd-hash like this: https://hackmd.io/MYDmFYHYE4DZILQBMBmSDMCAsIkFMEBDEcTcfYLWY2AI2miA?view

Your markdown on hackmd should look like this ( title and date is mandatory )

```markdown
---
title: my_title
date: 2017-08-31
...
---
your contents goes here
...
```

```
git clone https://github.com/OAlienO/hackmd2jekyll.git
python server.py
```

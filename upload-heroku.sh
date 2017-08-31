#!/bin/bash

cd ..
git add .
git commit -m "auto upload by hackmd2jekyll"
git push heroku master

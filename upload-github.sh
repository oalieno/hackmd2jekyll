#!/bin/bash

cd ..
jekyll build
cd _site
git add .
git commit -m "auto upload by hackmd2jekyll"
git push origin master

#!/bin/bash

git init
git add .
git commit -m "First commit"

git remote add origin https://github.com/shubhobm/unicef-dssg.git
# Sets the new remote
git remote -v
# Verifies the new remote URL

git push -u origin master

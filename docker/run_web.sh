#!/bin/bash

# http://stratus3d.com/blog/2019/11/29/bash-errexit-inconsistency/
# error then exit app
set -o errexit
# https://stackoverflow.com/a/49267647
# if system have any error then return fail
set -o pipefail
# https://stackoverflow.com/a/63583926
# not raise error if not variable
set -o nounset


#python manage.py migrate
#python manage.py runserver_plus 0.0.0.0:8000
python3 manage.py runserver 0.0.0.0:8000 --insecure
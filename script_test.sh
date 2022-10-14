#!/bin/bash

python3 manage.py migrate
pytest ./news/tests.py
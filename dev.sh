#! /usr/bin/env bash

gunicorn --reload wsgi:app

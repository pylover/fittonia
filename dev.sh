#! /usr/bin/env bash

gunicorn --timeout 9999 --reload fittonia:app

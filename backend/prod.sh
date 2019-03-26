#!/usr/bin/env bash

gunicorn -b localhost:9001 app:app

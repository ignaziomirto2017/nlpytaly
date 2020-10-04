#!/usr/bin/env bash

source venv/Scripts/activate
pytest -v --doctest-modules nlpytaly 
read
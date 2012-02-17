#!/bin/bash

dir=$(dirname $0)
dir=$(realpath $dir)
dir=$(realpath "$dir/..")

export DJANGO_SETTINGS_MODULE='settings'
export PYTHONPATH=$dir
echo $PYTHONPATH
make html
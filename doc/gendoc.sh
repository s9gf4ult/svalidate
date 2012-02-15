#!/bin/bash

dir=$(dirname $0)
dir=$(realpath $dir)
dir=$(realpath "$dir/..")

export PYTHONPATH=$dir
echo $PYTHONPATH
make html
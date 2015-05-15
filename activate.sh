#!/bin/bash
#
# Usage: source activate.sh
#

export VENV=`pwd`/env34
source $VENV/bin/activate
alias mypip='$VENV/bin/pip3.4'
alias mypython='$VENV/bin/python3.4'

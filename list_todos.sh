#!/bin/bash

source "$(dirname "$0")/common.inc"

#-----------------------------------------------------------

print_help() {
    cat <<EOF
list_todos.sh
=============

  list_todos.sh

Extract and list the TODOs of this project
EOF
}

#-----------------------------------------------------------

FALSE_POSITIVES=()
FALSE_POSITIVES+=('` (without quotes)')
FALSE_POSITIVES+=(' * 2>/dev/null')
FALSE_POSITIVES+=('\(.*\)$/* \3\n        \1 (line:\2)/')
FALSE_POSITIVES+=('lie and throw away */')

#-----------------------------------------------------------

if [ "$1" == "--help" ]
then
    print_help
    exit 1
fi

#-----------------------------------------------------------

filter() {
    if [ $# -gt 0 ]
    then
        local FILTER="$1"
        shift
        grep -v -F "$FILTER" | filter "$@"
    else
        cat
    fi
}

#-----------------------------------------------------------

grep -rnF ' TODO: ' * 2>/dev/null \
    | filter "${FALSE_POSITIVES[@]}" \
    | sed -e 's/^\([^:]*\):\([0-9]*\):.* TODO: \(.*\)$/* \3\n        \1 (line:\2)/' \


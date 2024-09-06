#!/bin/bash
# source ./scripts/get_weights_completion.sh

_get_weights_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local weights_file="weights.json"

    if [[ -f $weights_file ]]; then
        local options=$(jq -r 'paths(scalars) as $p | getpath($p) | select(. != null)' $weights_file | sort -u | tr '\n' ' ')
        COMPREPLY=($(compgen -W "$options" -- "$cur"))
    fi
}

complete -F _get_weights_completion ./scripts/get_weights.py

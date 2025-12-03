#!/usr/bin/bash

# -----> Terminal escape codes for markup
RED=$(tput setaf 1)
WARN=$(tput setaf 3)
NORMAL=$(tput sgr0)
BOLD=$(tput bold)
BRIGHT=$(tput bold)

modules=(
    $(git status --porcelain | awk -F'/' '{ print $1 }' | awk '{ print $2 }' | uniq)
)

actions=(
    'DEV'
    'ADD'
    'FIX'
    'MIG'
    'DEL'
    'ADM'
    'WIP'
)

# -----> Overly complex pure-bash multiselect function...
function multiselect {
    # helpers for terminal print control and key input
    ESC=$( printf "\033")
    cursor_blink_on()   { printf "$ESC[?25h"; }
    cursor_blink_off()  { printf "$ESC[?25l"; }
    cursor_to()         { printf "$ESC[$1;${2:-1}H"; }
    print_inactive()    { printf "$1"; }
    print_active()      { printf "$ESC[7m$1$ESC[27m"; }
    get_cursor_row()    { IFS=';' read -sdR -p $'\E[6n' ROW COL; echo ${ROW#*[}; }

    local return_value=$1
    local -n options=$2

    local selected=()
    for ((i=0; i<${#options[@]}; i++)); do
        selected+=("false")
        printf "\n"
    done

    # determine current screen position for overwriting the options
    local lastrow=`get_cursor_row`
    local startrow=$(($lastrow - ${#options[@]}))

    # ensure cursor and input echoing back on upon a ctrl+c during read -s
    trap "cursor_blink_on; stty echo; printf '\n'; exit" 2
    cursor_blink_off

    key_input() {
        local key
        IFS= read -rsn1 key 2>/dev/null >&2
        if [[ $key = ""      ]]; then echo enter; fi;
        if [[ $key = $'\x20' ]]; then echo space; fi;
        if [[ $key = "k" ]]; then echo up; fi;
        if [[ $key = "j" ]]; then echo down; fi;
        if [[ $key = $'\x1b' ]]; then
            read -rsn2 key
            if [[ $key = '[A' || $key = 'k' ]]; then echo up;    fi;
            if [[ $key = '[B' || $key = 'j' ]]; then echo down;  fi;
        fi
    }

    print_options() {
        # print options by overwriting the last lines
        local idx=0
        for option in "${options[@]}"; do
            cursor_to $(($startrow + $idx))
            if [ $idx -eq $1 ]; then
                print_active "$option"
            else
                print_inactive "$option"
            fi
            ((idx++))
        done
    }

    local active=0
    while true; do
        print_options $active

        # user key control
        case `key_input` in
            enter) print_options -1; break;;
            up)
                ((active--));
                if [ $active -lt 0 ]; then
                    active=$((${#options[@]} - 1));
                fi;;
            down)
                ((active++));
                if [ $active -ge ${#options[@]} ]; then
                    active=0;
                fi;;
        esac
    done

    # cursor position back to normal
    cursor_to $startrow
    for ((i=0; i<${#options[@]}; i++)); do
        printf "   \n"
    done
    cursor_to $startrow
    echo "${options[$active]}"
    cursor_blink_on

    eval $return_value='("${active}")'
}

function docommit {
    # -----> Repo selection prompt with best-guess preselection
    local return_value=$1
    local modulename=$2
    echo "action for module ${modulename}"
    # -----> Check
    multiselect result actions
    msg="[${actions[$result]}] ${modulename} - "
    echo "commit message for ${modulename}: "
    read commit_msg
    echo ""
    eval $return_value='("${msg}${commit_msg^}")'
}

for module in "${modules[@]}"; do
    docommit result $module
    git add $module && git commit -m "$result"
done

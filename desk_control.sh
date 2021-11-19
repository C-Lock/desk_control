#!/bin/bash
####
# Author: C-Lock
# This code is the primary method of non-app based control for the desk.
# use -h, --h to identify valid commands
# while this script is fully functional, it is expected to be wrapped by another utility
# i.e. api, web-server, cron-job, etc.
####
#This bluetooth address is (most likely) unique to my desk. 
bt_addr="34:e3:1a:12:A5:D3"
#Refer to README.md for instructions to find your own...but if you can't even find your own address...why are you reading my code?

function adjust_desk(){
    gatttool -b $1 --char-write-req -a 0x0025 -n $2
}

function show_help(){
    echo -e "Welcome to the desk_control.sh Help Menu!"
    echo -e "Use this script to command your UPLIFT Desk (with BT unit JCP35N-BLT) to follow your whims!"
    echo -e "Valid options are required."
    echo -e "Options:\n\thelp, -h, --h)\t This menu!"
    echo -e "\tl)\treduce desk height by 1 unit (~.3\")"
    echo -e "\tr)\tincrease desk height by 1 unit(~.3\")"
    echo -e "\ts)\tMove the Desk to either 'sit' or 'stand' position (additional argument required)"
    echo -e "\t\toptions: 'sit' or 'stand'"
    echo -e "EXAMPLE: 'desk_control.sh -s sit' will set the desk to position 1"
}


while getopts "hlrs:" arg; do
    case $arg in

        h)
            show_help
            ;;
        l) # lower desk
            adjust_desk $bt_addr f1f10200027e #The Desk shall bow before you! But a slight, polite bow of only ~.3"
            break
            ;;
        r) # raise desk
            adjust_desk $bt_addr f1f10100017e #The Desk shall RISE! by approximately .3inch
            break
            ;;
        s) # setting
            setting=$OPTARG
            case $setting in
                sit)
                    adjust_desk $bt_addr f1f10500057e
                    ;;
                stand)
                    adjust_desk $bt_addr f1f10600067e
                    ;;
            esac
            ;;
        *)
            show_help
            break
            ;;
    esac
done
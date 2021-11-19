#!/bin/bash
####
# Author: C-Lock
# This code is the primary method of non-app based control for the desk.
# use -h, --h to identify valid commands
# while this script is fully functional, it is expected to be wrapped by another utility
# i.e. api, web-server, cron-job, etc.
####
#This bluetooth address is (most likely) unique to my desk. 
bt_addr="48:70:1E:32:A7:D1"
#Refer to README.md for instructions to find your own...but if you can't even find your own address...why are you reading my code?

function raise_desk(){ #The Desk shall RISE! by approximately .3inch
    gatttool -b $1 --char-write-req -a 0x0025 -n f1f10100017e
}

function lower_desk(){ #The Desk shall bow before you! But a slight, polite bow of only ~.3"
    gatttool -b $1 --char-write-req -a 0x0025 -n f1f10200027e
}

function setting_one(){ #This is the setting "1" you've previously saved using the physical buttons
    gatttool -b $1 --char-write-req -a 0x0025 -n f1f10500057e
}

function setting_two(){ #This is the setting one higher than "1".
    gatttool -b $1 --char-write-req -a 0x0025 -n f1f10600067e
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
        l)
            lower_desk $bt_addr
            break
            ;;
        r)
            raise_desk $bt_addr
            break
            ;;
        s)
            setting=$OPTARG
            case $setting in
                sit)
                    setting_one $bt_addr
                    ;;
                stand)
                    setting_two $bt_addr
                    ;;
            esac
            ;;
        *)
            show_help
            break
            ;;
    esac
done
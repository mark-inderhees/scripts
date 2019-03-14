#!/bin/bash

dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver'" |
    while read x; do
        case "$x" in 
            # *"boolean true"*) echo SCREEN_LOCKED;;
            *"boolean false"*) resetmsmice;;  
        esac
    done


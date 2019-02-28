#!/bin/bash

if [[ sudo -n python control_script.py ]] ; then
    echo 'Executing control_script with sudo...'
else
    echo 'Unable to sudo non-interactively. Running control_script without sudo.'
    python control_script.py
fi



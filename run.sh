#!/bin/bash

cd capability_testing/

if sudo -n python -c '' ; then
    echo 'Executing control_script with sudo...'
   sudo -n python control_script.py
else
    echo 'Unable to sudo non-interactively. Running control_script without sudo.'
    python control_script.py
fi



#!/bin/bash

KLIPPER_PATH="${HOME}/klipper"
TOOL_CHANGER_PATH="${HOME}/klipper/printer/config/tool_management/tool_changer"

set -eu
export LC_ALL=C


function preflight_checks {
    if [ "$EUID" -eq 0 ]; then
        echo "[PRE-CHECK] This script must not be run as root!"
        exit -1
    fi

    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F 'klipper.service')" ]; then
        printf "[PRE-CHECK] Klipper service found! Continuing...\n\n"
    else
        echo "[ERROR] Klipper service not found, please install Klipper first!"
        exit -1
    fi
}

function check_download {
    # local autotunedirname autotunebasename
    # autotunedirname="$(dirname ${AUTOTUNETMC_PATH})"
    # autotunebasename="$(basename ${AUTOTUNETMC_PATH})"

    # if [ ! -d "${AUTOTUNETMC_PATH}" ]; then
    #     echo "[DOWNLOAD] Downloading Autotune TMC repository..."
    #     if git -C $autotunedirname clone https://github.com/andrewmcgr/klipper_tmc_autotune.git $autotunebasename; then
    #         chmod +x ${AUTOTUNETMC_PATH}/install.sh
    #         printf "[DOWNLOAD] Download complete!\n\n"
    #     else
    #         echo "[ERROR] Download of Autotune TMC git repository failed!"
    #         exit -1
    #     fi
    # else
    #     printf "[DOWNLOAD] Autotune TMC repository already found locally. Continuing...\n\n"
    # fi
}

function link_extension {
    echo "[INSTALL] Linking extension to Klipper..."
    ln -srfn "${TOOL_CHANGER_PATH}/tool.py" "${KLIPPER_PATH}/klippy/extras/tool.py"
    ln -srfn "${TOOL_CHANGER_PATH}/dock.py" "${KLIPPER_PATH}/klippy/extras/dock.py"
}

function restart_klipper {
    echo "[POST-INSTALL] Restarting Klipper..."
    sudo systemctl restart klipper
}


printf "\n======================================\n"
echo "- Tool Changer install script -"
printf "======================================\n\n"


# Run steps
preflight_checks
check_download
link_extension
restart_klipper

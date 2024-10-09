#!/bin/bash

KLIPPER_PATH="${HOME}/klipper"
KYMERON_PATH="${HOME}/Kymeron"

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
    local kymeron_dir_name kymeron_base_name
    kymeron_dir_name="$(dirname ${KYMERON_PATH})"
    kymeron_base_name="$(basename ${KYMERON_PATH})"

    if [ ! -d "${KYMERON_PATH}" ]; then
        echo "[DOWNLOAD] Downloading Kymeron repository..."
        if git -C $carriage_changer_dir_name clone https://github.com/DavidPeterWatson/Kymeron.git $kymeron_base_name; then
            chmod +x ${KYMERON_PATH}/install.sh
            printf "[DOWNLOAD] Download complete!\n\n"
        else
            echo "[ERROR] Download of Kymeron git repository failed!"
            exit -1
        fi
    else
        printf "[DOWNLOAD] Kymeron repository already found locally. Continuing...\n\n"
    fi
}

function link_extension {
    echo "[INSTALL] Linking extension to Klipper..."
    ln -srfn "${KYMERON_PATH}/extras/emergency_stop.py" "${KLIPPER_PATH}/klippy/extras/emergency_stop.py"
    # ln -srfn "${KYMERON_PATH}/klipper" "${KLIPPER_PATH}/printer_data/klipper"
}

function restart_klipper {
    echo "[POST-INSTALL] Restarting Klipper..."
    sudo systemctl restart klipper
}


printf "\n======================================\n"
echo "- Kymeron install script -"
printf "======================================\n\n"


# Run steps
preflight_checks
check_download
link_extension
restart_klipper

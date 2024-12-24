#!/bin/bash

KLIPPER_PATH="${HOME}/klipper"
KYMERON_PATH="${HOME}/kymeron"
PRINTER_DATA_PATH="${HOME}/printer_data"

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
        echo "[DOWNLOAD] Downloading kymeron repository..."
        if git -C $kymeron_dir_name clone https://github.com/DavidPeterWatson/kymeron.git $kymeron_base_name; then
            chmod +x ${KYMERON_PATH}/install.sh
            printf "[DOWNLOAD] Download complete!\n\n"
        else
            echo "[ERROR] Download of kymeron git repository failed!"
            exit -1
        fi
    else
        printf "[DOWNLOAD] kymeron repository already found locally. Continuing...\n\n"
    fi
}

function link_extension {
    echo "[INSTALL] Linking extension to Klipper..."
    ln -srfn "${KYMERON_PATH}/extras/emergency_stop.py" "${KLIPPER_PATH}/klippy/extras/emergency_stop.py"
    ln -srfn "${KYMERON_PATH}/extras/brush.py" "${KLIPPER_PATH}/klippy/extras/brush.py"
    ln -srfn "${KYMERON_PATH}/extras/wiggle_retraction.py" "${KLIPPER_PATH}/klippy/extras/wiggle_retraction.py"
    ln -srfn "${KYMERON_PATH}/extras/extruder_management.py" "${KLIPPER_PATH}/klippy/extras/extruder_management.py"
    ln -srfn "${KYMERON_PATH}/extras/carriage_changer.py" "${KLIPPER_PATH}/klippy/extras/carriage_changer.py"
    ln -srfn "${KYMERON_PATH}/extras/carriage.py" "${KLIPPER_PATH}/klippy/extras/carriage.py"
    ln -srfn "${KYMERON_PATH}/extras/berth.py" "${KLIPPER_PATH}/klippy/extras/berth.py"
    ln -srfn "${KYMERON_PATH}/extras/dock.py" "${KLIPPER_PATH}/klippy/extras/dock.py"
    ln -srfn "${KYMERON_PATH}/extras/tool_probe.py" "${KLIPPER_PATH}/klippy/extras/tool_probe.py"
    ln -srfn "${KYMERON_PATH}/extras/bed_probe.py" "${KLIPPER_PATH}/klippy/extras/bed_probe.py"
    ln -srfn "${KYMERON_PATH}/extras/multi_fan.py" "${KLIPPER_PATH}/klippy/extras/multi_fan.py"
    ln -srfn "${KYMERON_PATH}/extras/gcode_shell_command.py" "${KLIPPER_PATH}/klippy/extras/gcode_shell_command.py"
    ln -srfn "${KYMERON_PATH}/kymeron_config" "${PRINTER_DATA_PATH}/config"
}

function restart_klipper {
    echo "[POST-INSTALL] Restarting Klipper..."
    sudo systemctl restart klipper
}


printf "\n======================================\n"
echo "- kymeron install script -"
printf "======================================\n\n"


# Run steps
preflight_checks
check_download
link_extension
restart_klipper

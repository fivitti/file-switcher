# -*- coding: utf-8 -*-
from __future__ import print_function
import filecmp
import os
import shutil
import sys
import RPi.GPIO as GPIO

# === Confguration ===
pin_to_filename_mapping = {
    23: "hdmi.config",
    24: "video.config"
}
boot_config_filename = "boot.config"
boot_directory = "/boot"
# === End configuration ===

def get_pins():
    return pin_to_filename_mapping.keys()

def init():
    '''
    GPIO setup
    We accept that pin is selected when
    the current flows through it
    '''
    GPIO.setmode(GPIO.BCM)

    pins = get_pins()

    for pin in pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def get_selected_pin():
    pins = get_pins()

    for pin in pins:
        if GPIO.input(pin):
            return pin
    
    return None

def are_the_same_files(first_path, second_path):
    return filecmp.cmp(first_path, second_path)

def replace_files(source_path, target_path):
    shutil.copyfile(source_path, target_path)

def restart():
    '''Only Linux is supported'''
    os.system('reboot now')

def cleanup():
    GPIO.cleanup()

def set_correct_configuration():
    '''Return True when configuration file is changed and need restart'''
    selected_pin = get_selected_pin()
    if selected_pin is None:
        print('None pin is selected')
        return False

    boot_config_path = os.path.join(boot_directory, boot_config_filename)

    target_configuration_filename = pin_to_filename_mapping[selected_pin]
    target_configuration_path = os.path.join(boot_directory, target_configuration_filename)

    if are_the_same_files(boot_config_path, target_configuration_path):
        print('Not change the pin state - configuration are the same')
        return False

    replace_files(target_configuration_path, boot_config_path)

    print('Change configuration to {}'.format(target_configuration_filename))
    return True

def execute():
    try:
        init()
        need_restart = set_correct_configuration()
    finally:
        cleanup()

    if need_restart:
        restart()

if __name__ == '__main__':
    execute()
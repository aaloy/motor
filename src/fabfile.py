#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from fabric. api import *
import datetime

CHROOT_DIR = '/var/lib/schroot/mount/app1-source'
APP_DIR = '/var/pywww/motorh'
env.hosts = ['kiwi4.apsl.net']


def get_num_operacion():
    """Genera un número de operación"""
    num = datetime.datetime.now().toordinal()
    ms = datetime.datetime.now().microsecond
    return "%06d%06d" % (num, ms)

def update():
    num = get_num_operacion()
    sudo('chroot %s mv %s/db.sqlite %s/db.sqlite.%s' % (CHROOT_DIR, APP_DIR, APP_DIR, num))
    sudo('chroot %s svn up %s' % (CHROOT_DIR, APP_DIR))
    sudo('chroot %s chown motor.django %s/db.sqlite' % (CHROOT_DIR, APP_DIR))
    sudo('chroot %s djangoservice -e motorh stop' % CHROOT_DIR)
    sudo('chroot %s djangoservice -e motorh start' % CHROOT_DIR)
    sudo('chroot %s djangoservice -e motorh status' % CHROOT_DIR)

def status():
        sudo('chroot %s djangoservice' % CHROOT_DIR)

def restart():
        sudo('chroot %s djangoservice -e motorh restart' % CHROOT_DIR)

def chown():
        sudo('chroot %s chown -R motor.django %s' % (CHROOT_DIR, APP_DIR))

def stop():
    sudo('chroot %s djangoservice -e motorh stop' % CHROOT_DIR)

def start():
    sudo('chroot %s djangoservice -e motorh start' % CHROOT_DIR)

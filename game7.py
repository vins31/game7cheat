#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re
import mechanize
from getpass import getpass
from time import sleep

br = mechanize.Browser()

def createAccount(br, nickname, password):
    br.open("http://game7.inpt.fr/registration")
    br.form = list(br.forms())[0]
    br.form.find_control("lastname").value = nickname
    br.form.find_control("firstname").value = nickname
    br.form.find_control("email").value = nickname+"@hotmail.com"
    br.form.find_control("birth").value = "01/01/1990"
    br.form.find_control("city").value = "Toulouse"
    br.form.find_control("country").value = "France"
    br.form.find_control("nickname").value = nickname
    br.form.find_control("password").value = password
    br.form.find_control("passwordconf").value = password

    for control in br.form.controls:
       if control.type == "submit":
           control.disabled = True

    return br.submit()
    


def createManyAccounts():
    prefix = raw_input("nickanme prefix? ")
    number = int(raw_input("number of accounts? "))
    password = getpass("password? ")
    for i in range(41, number):
        print "Creating account", i
        createAccount(br, prefix+str(i), password)
        sleep(5)



createManyAccounts()
#answer = createAccount(br, "pipo2", "pipo2pipo2")
#print answer.read()


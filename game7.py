#!/usr/bin/python2
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from getpass import getpass
import mechanize
import re
from time import sleep


class AccountCreator:
    def __init__(self):
        self.br = mechanize.Browser()
        self.createManyAccounts()
    
    def createAccount(nickname, password):
        self.br.open("http://game7.inpt.fr/registration")
        self.br.form = list(self.br.forms())[0]
        self.br.form.find_control("lastname").value = nickname
        self.br.form.find_control("firstname").value = nickname
        self.br.form.find_control("email").value = nickname+"@hotmail.com"
        self.br.form.find_control("birth").value = "01/01/1990"
        self.br.form.find_control("city").value = "Toulouse"
        self.br.form.find_control("country").value = "France"
        self.br.form.find_control("nickname").value = nickname
        self.br.form.find_control("password").value = password
        self.br.form.find_control("passwordconf").value = password
        return self.br.submit()
    

    def createManyAccounts(self):
        prefix = raw_input("nickname prefix? ")
        number = int(raw_input("number of accounts? "))
        password = getpass("password? (minimum 8 chars) ")
        for i in range(number):
            print "Creating account", i
            self.createAccount(self.br, prefix+str(i), password)
            sleep(2)

class Production:
    def __init__(self):
        self.pierre   = 0
        self.gold     = 0
        self.argent   = 0
        self.cuivre   = 0
        self.metal    = 0
    def __str__(self):
        return "Pierre %d, Or %d, Argent %d, Cuivre %d, Métal %d" % (self.pierre, self.gold, self.argent, self.cuivre, self.metal)

class Account:
    def __init__(self, nickname, password):
        self.br = mechanize.Browser()
        self.nickname = nickname
        self.password = password
        self.production = Production()
        # Connect
        res = self.connectAccount()
        
        
    def connectAccount(self):
        res = self.br.open("http://game7.inpt.fr/home")
        self.br.form = list(self.br.forms())[0]
        self.br.form.find_control("nickname").value = self.nickname
        self.br.form.find_control("password").value = self.password
        res =  self.br.submit()
        self.getProduction(res.get_data())
        
    def getProduction(self, page):
        soup = BeautifulSoup(page)
        nav = soup.find("ul", { "class" : "nav" })
        for prod in nav.findAll("a"):
            item = prod.contents[0].split(" : ")
            if item[0] == u"Pierre":
                self.production.pierre = int(item[1])
            if item[0] == u"Or":
                self.production.gold = int(item[1])
            if item[0] == u"Argent":
                self.production.argent = int(item[1])
            if item[0] == u"Cuivre":
                self.production.cuivre = int(item[1])
            if item[0] == u"Métal":
                self.production.metal = int(item[1])
        print "%s : %s" % (self.nickname, self.production)
                

    def goToBatiments(self):
        res =  self.br.open("http://game7.inpt.fr/building")
        self.getProduction(res.get_data())
        return res
        
    def goToCommerce(self):
        res =  self.br.open("http://game7.inpt.fr/market")
        self.getProduction(res.get_data())
        return res
        
    def logout(self):
        res =  self.br.open("http://game7.inpt.fr/connection?action=logout")
        return res
        
    def acceptTransaction(self, page, clientAccount):
        soup = BeautifulSoup(page)
        for transaction in soup.findAll("tr", { "class" : "info" }):
            if transaction.text.find(clientAccount) != -1:
                print "Transaction found"
                link = transaction.a.get("href")
                res = self.br.follow_link(url=link)
                print "Transaction accepted"
                break

    def doMyTransaction(self, clientAccount):
        res = self.goToCommerce()
        self.acceptTransaction(res.get_data(), clientAccount)
        
    def createTransaction(self, production):
        res = self.goToCommerce()
        self.br.form = list(self.br.forms())[0]
        self.br.form.find_control("offer_stone").value = "1"
        self.br.form.find_control("offer_gold").value = "0"
        self.br.form.find_control("offer_argent").value = "0"
        self.br.form.find_control("offer_cuivre").value = "0"
        self.br.form.find_control("offer_metal").value = "0"
        self.br.form.find_control("request_stone").value = str(production.pierre)
        self.br.form.find_control("request_gold").value = str(production.gold)
        self.br.form.find_control("request_argent").value = str(production.argent)
        self.br.form.find_control("request_cuivre").value = str(production.cuivre)
        self.br.form.find_control("request_metal").value = str(production.metal)
        res =  self.br.submit()
        self.getProduction(res.get_data())
        
        
class FatherAccount(Account):
    def __init__(self, nickname, password):
        Account.__init__(self, nickname, password)
        
    def createSlaveTransaction(self, slaveProduction):
        self.createTransaction(slaveProduction)
        
        
        
class SlaveAccount(Account):
    def __init__(self, nickname, password, fatherAccount):
        if nickname == fatherAccount.nickname:
            raise Exception('Same User')
        self.fatherAccount = fatherAccount
        Account.__init__(self, nickname, password)
        
    def giveProduction(self):
        self.fatherAccount.createSlaveTransaction(self.production)
        self.doMyTransaction(self.fatherAccount.nickname)
        self.fatherAccount.goToBatiments()
        print "Transaction given"
        
        
def getSlaveRessources():
    nickname = raw_input("nickname of the father account? ")
    password = getpass("password of the fath account? (minimum 8 chars) ")
    prefix = raw_input("nickname slaves prefix? ")
    slavePassword = getpass("password of the slaves ? (minimum 8 chars) ")
    start = int(raw_input("number of the first slave accounts? "))
    end = int(raw_input("number of the last slave accounts? "))
    
    for i in range(start, end):
        try:
            father = FatherAccount(nickname, password)
            slave = SlaveAccount("%s%d" % (prefix,i), slavePassword, father)
            slave.giveProduction()
            # La déconnexion permet d'éviter de rencontrer le bug 
            # des "ressources non rajoutées"
            father.logout()
            slave.logout()
        except:
            print "A problem occured with %s%d" % (prefix,i)

if __name__ == "__main__":
    getSlaveRessources()
    
        

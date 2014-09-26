import urllib
import sys


class AvtomatiBase():
    def __init__(self, url="http://celtra-jackpot.com/1/"):
        self.avtomati = []
        self.url = url  #url streznika
        self.pulls = 0  #koliko potegov smo ze izvedli
        self.nMachines = self.getNMachines()
        self.maxPulls = self.getPulls()

    def getPulls(self):
        """
        :return: poslje zahtevek na streznik in vrne stevilo potegov, ki so na voljo
        """
        return int(urllib.urlopen(self.url+"pulls").read())

    def getNMachines(self):
        """
        :return: poslje zahtevek na streznik in vrne stevilo avtomatov, ki so na voljo
        """
        return int(urllib.urlopen(self.url+"machines").read())

    def pull(self, machine):
        """
        :param machine: st igralnega avtomata
        :return: vrne rezultat potega
        """
        self.pulls += 1
        return int(urllib.urlopen("%s\%d\%d" % (self.url, machine, self.pulls)))


class Avtomati(AvtomatiBase):
    pass

if __name__ == "__main__":
    if len(sys.argv)>1:
        Avtomati(sys.argv[1]+"/")
    else:
        Avtomati()

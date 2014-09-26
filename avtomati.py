import urllib
import sys


class Avtomati():
    def __init__(self, url="http://celtra-jackpot.com/1/"):
        self.avtomati = []
        self.url = url
        self.req = 0
        self.pulls = 0
        self.nMachines = self.getNMachines()
        self.maxPulls = self.getPulls()

    def getPulls(self):
        return int(urllib.urlopen(self.url+"pulls").read())

    def getNMachines(self):
        return int(urllib.urlopen(self.url+"machines").read())

    def pull(self, machine):
        self.pulls += 1
        return int(urllib.urlopen("%s\%s\%s" % (self.url, machine, self.pulls)))


if __name__ == "__main__":
    if len(sys.argv)>1:
        Avtomati(sys.argv[1]+"/")
    else:
        Avtomati()

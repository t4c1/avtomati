import urllib
import sys


class Avtomati():
    def __init__(self, url=""):
        self.avtomati = []
        if url:
            self.url = url
        else:
            self.url = "http://celtra-jackpot.com/1/"
        self.req = 0
        self.pulls = 0

    def getPulls(self):
        return int(urllib.urlopen(self.url+"pulls").read())

    def getNMachines(self):
        return int(urllib.urlopen(self.url+"machines").read())

    def pull(self, machine):
        self.pulls += 1
        return int(urllib.urlopen("%s\%s\%s" % (self.url, machine, self.pulls)))


if __name__ == "__main__":
    if sys.argv:
        Avtomati(sys.argv[0]+"/")
    else:
        Avtomati()

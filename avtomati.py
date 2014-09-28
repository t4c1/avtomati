import urllib
import sys


class AvtomatiBase():
    def __init__(self, url="http://celtra-jackpot.com/1"):
        self.url = url  # url streznika
        self.pulls = 0  # koliko potegov smo ze izvedli
        self.nMachines = self.getNMachines()
        self.maxPulls = self.getPulls()

    def start(self):
        pass

    def getPulls(self):
        """
        :return: stevilo potegov, ki so na voljo
        """
        return int(urllib.urlopen(self.url+"/pulls").read())

    def getNMachines(self):
        """
        :return: stevilo avtomatov, ki so na voljo
        """
        return int(urllib.urlopen(self.url+"/machines").read())

    def pull(self, machine):
        """
        poteg rocice na igralnem avtomatu
        :param machine: st igralnega avtomata
        :return: vrne rezultat potega
        """
        self.pulls += 1
        url = "%s/%d/%d" % (self.url, machine, self.pulls)
        print url
        return int(urllib.urlopen(url).read())


class Avtomati(AvtomatiBase):
    def __init__(self, url="http://celtra-jackpot.com/1"):
        AvtomatiBase.__init__(self, url)
        self.machines = [list(i) for i in enumerate([0]*self.nMachines)]
        print self.nMachines,self.maxPulls,self.machines
        self.start()

    def start(self):
        for i in xrange(self.maxPulls):
            machine = self.choose()
            if self.pull(machine[0]+1):
                self.machines[machine[0]][1] += 1

    def choose(self):
        return max(self.machines, key=lambda x: x[1])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        a = Avtomati(sys.argv[1])
    else:
        a = Avtomati()
    print a.machines

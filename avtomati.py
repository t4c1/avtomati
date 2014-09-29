from __future__ import division
import urllib
import sys
import random

testing=1

class AvtomatiBase():
    def __init__(self, url="http://celtra-jackpot.com/1"):
        self.url = url  # url streznika
        self.pulls = 0  # koliko potegov smo ze izvedli
        self.nMachines = self.getNMachines()
        self.maxPulls = self.getPulls()
        self.machines = [[i,0,0] for i in range(self.nMachines)]  # naredimo seznam oblike[[<zap st.>,<st. uspesnih potegov>,<st. vseh potegov>], <naslednji avtomat> ...]

    def start(self):
        pass

    def getPulls(self):
        """
        :return: stevilo potegov, ki so na voljo
        """
        if testing:
            return 1000
        return int(urllib.urlopen(self.url+"/pulls").read())

    def getNMachines(self):
        """
        :return: stevilo avtomatov, ki so na voljo
        """
        if testing:
            return 2
        return int(urllib.urlopen(self.url+"/machines").read())

    def pull(self, machine,iter=0):
        """
        poteg rocice na igralnem avtomatu
        :param machine: st igralnega avtomata
        :return: vrne rezultat potega
        """
        self.pulls += 1
        if testing:
            chance=random.random()
            if machine==1:
                if chance<0.4:
                    return 1
            elif machine==2:
                if chance<0.6:
                    return 1
            return 0

        url = "%s/%d/%d" % (self.url, machine, self.pulls)
        #print url
        try:
            return int(urllib.urlopen(url).read())
        except IOError,err:
            if err[0]==10060 and iter<3: #3 poskusi, ce pride do napake pri povezavi na streznik
                return self.pull(machine,iter+1)
            else:
                #print err[0],err[1],err
                raise



class Avtomati(AvtomatiBase):
    def __init__(self, url="http://celtra-jackpot.com/1"):
        AvtomatiBase.__init__(self, url)
        self.start()

    def start(self):
        for i in xrange(self.maxPulls):
            machine = max(self.machines, key=self.weight)
            self.machines[machine[0]][2] += 1
            if self.pull(machine[0]+1):
                self.machines[machine[0]][1] += 1

    def weight(self,x):
        #TODO: ugibanje spremembe verjetnosti
        n,successful,all=x
        if all==0:
            all=0.1
        success_rate = successful / all
        end_f=self.pulls/self.maxPulls
        inaccurate_f=1/all**0.5
        return success_rate + inaccurate_f


def run():
    if len(sys.argv) > 1:
        a = Avtomati(sys.argv[1])
    else:
        a = Avtomati("http://celtra-jackpot.com/1")
    return a

def test():
    for i in range(10):
        a=Avtomati("http://celtra-jackpot.com/%d" %(i+1,))
        print a.maxPulls,a.nMachines
        print [(s/al,s,al) for n,s,al in a.machines]
        print


if __name__ == "__main__":
    test()



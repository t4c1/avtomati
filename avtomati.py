from __future__ import division
import urllib
import sys
import random

testing = 1
testing_pulls = 0
testing_machines = []


class AvtomatiBase():
    def __init__(self, url="http://celtra-jackpot.com/1"):
        self.url = url  # url streznika
        self.pulls = 0  # koliko potegov smo ze izvedli
        self.nMachines = self.getNMachines()
        self.maxPulls = self.getPulls()
        self.machines = [[i,[],0.5,0] for i in range(self.nMachines)]  # naredimo seznam oblike[[<zap st.>,[seznam vseh potegov],trenutna verjetnost,zaporednih neizbir], <naslednji avtomat> ...]

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

    def pull(self, machine, iter=0):
        """
        poteg rocice na igralnem avtomatu
        :param machine: st igralnega avtomata
        :return: vrne rezultat potega
        """
        self.pulls += 1

        url = "%s/%d/%d" % (self.url, machine, self.pulls)
        #print url
        try:
            return int(urllib.urlopen(url).read())
        except IOError,err:
            if err[0] == 10060 and iter < 3:  # 3 poskusi, ce pride do napake pri povezavi na streznik
                return self.pull(machine, iter+1)
            else:
                #print err[0],err[1],err
                raise


class Avtomati(AvtomatiBase):
    def __init__(self, url="http://celtra-jackpot.com/1"):
        AvtomatiBase.__init__(self, url)
        #konstante algoritma
        self.run_factor = 0.1
        self.run_factor2 = 0.2
        self.innac_factor = 0.5
        self.last_len = 10
        self.rate_w = 1
        self.innac_w = 1
        self.run_w = 1
        self.run_w2 = 1
        self.last_w = 1
        self.unlucky_factor=0.5
        self.unlucky_w=0.2
        self.faster_factor=2

        #self.start()

    def start(self):
        #pozene algoritem
        for i in xrange(self.maxPulls):
            machine = max(self.machines, key=self.weight)
            ##self.machines[machine[0]][2] += 1
            machine[3]=0
            for m in self.machines:
                if m!=machine:
                    m[3]+=1
            res = self.pull(machine[0]+1)
            self.machines[machine[0]][1].append(res)
                ##self.machines[machine[0]][1] += 1

    def weight(self, x):
        #TODO: ugibanje spremembe verjetnosti
        all = len(x[1])
        successful = sum(x[1])
        if all == 0:
            all = 0.1

        rate = successful / all  #delez uspesnih
        running_avg=0.5  # tekoce povprecje uspesnih
        rfm=10/(-x[3]-(10/(self.faster_factor-1)))+self.faster_factor
        for result in x[1]:
            running_avg=running_avg*(1-(self.run_factor*rfm))+(self.run_factor*rfm)*result
        inacc=1 / int(all+1) ** self.innac_factor  #faktor nenatancnosti
        unlucky=x[3]**self.unlucky_factor
        return inacc*self.innac_w + running_avg*self.run_w + unlucky*self.unlucky_w


def run():
    if len(sys.argv) > 1:
        a = Avtomati(sys.argv[1])
        a.start()
    else:
        a = Avtomati("http://celtra-jackpot.com/1")
        a.start()
    return a


if __name__ == "__main__":
    run()



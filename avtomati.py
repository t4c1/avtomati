from __future__ import division
import urllib
import sys
import random

testing=1
testing_pulls=0
testing_machines=[]

class AvtomatiBase():
    def __init__(self, url="http://celtra-jackpot.com/1"):
        self.url = url  # url streznika
        self.pulls = 0  # koliko potegov smo ze izvedli
        self.nMachines = self.getNMachines()
        self.maxPulls = self.getPulls()
        self.machines = [[i,[]] for i in range(self.nMachines)]  # naredimo seznam oblike[[<zap st.>,[seznam vseh potegov]], <naslednji avtomat> ...]

    def start(self):
        pass

    def getPulls(self):
        """
        :return: stevilo potegov, ki so na voljo
        """
        if testing:
            return testing_pulls
        return int(urllib.urlopen(self.url+"/pulls").read())

    def getNMachines(self):
        """
        :return: stevilo avtomatov, ki so na voljo
        """
        if testing:
            return len(testing_machines)
        return int(urllib.urlopen(self.url+"/machines").read())

    def pull(self, machine,iter=0):
        """
        poteg rocice na igralnem avtomatu
        :param machine: st igralnega avtomata
        :return: vrne rezultat potega
        """
        self.pulls += 1
        if testing:
            roll=random.random()
            prev=0
            for start, chance in testing_machines[machine-1]:
                if self.pulls<start:
                    prev=chance
                else:
                    if roll<chance:
                        return 1
                    else:
                        return 0
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
        #pozene algoritem
        for i in xrange(self.maxPulls):
            machine = max(self.machines, key=self.weight)
            ##self.machines[machine[0]][2] += 1
            res=self.pull(machine[0]+1)
            self.machines[machine[0]][1].append(res)
                ##self.machines[machine[0]][1] += 1

    def weight(self,x):
        #TODO: ugibanje spremembe verjetnosti
        all=len(x[1])
        successful=sum(x[1])
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
    global testing,testing_pulls,testing_machines
    testing=1
    testing_pulls,testing_machines=makeTestCase()
    for i in range(3):
        a=Avtomati("http://celtra-jackpot.com/%d" %(i+1,))
        print "potegov:",a.maxPulls,", avtomatov:",a.nMachines
        for (n,s),machine in zip(a.machines,testing_machines):
            print "%5d %5d  %.3f   %s"%(sum(s),len(s),sum(s)/len(s),str(machine))
        #print [(sum(s)/len(s),sum(s),len(s)) for n,s in a.machines]
        #print testing_machines
        print "uspesnih:", sum([sum(s) for n,s in a.machines])
        print


def makeTestCase():
    machines=[]
    cases=random.randint(500,3000)
    for i in range(random.randint(2,10)):
        machines.append([])
        n=random.randint(1,cases//200)
        for j in range(n):
            machines[-1].append([j*cases//n,random.random()])
    return cases,machines

if __name__ == "__main__":
    a=test()



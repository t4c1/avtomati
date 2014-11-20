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

    def pull(self, machine, iter=0):
        """
        poteg rocice na igralnem avtomatu
        :param machine: st igralnega avtomata
        :return: vrne rezultat potega
        """
        self.pulls += 1
        if testing:
            roll = random.random()
            prev = 0
            #print testing_machines[machine-1]
            for start, chance in testing_machines[machine-1]:
                if self.pulls < start:
                    break
                prev = chance
            if roll<prev:
                return 1
            else:
                return 0

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
        last_rate = sum(x[1][:self.last_len])/self.last_len if len(x[1]) > self.last_len else rate  #delez uspesnih med nekaj zadnjimi potegi
        running_avg=0.5  # tekoce povprecje uspesnih
        running_avg2=0.5  # "hitrejse" tekoce povprecje
        rfm=10/(-x[3]-(10/(self.faster_factor-1)))+self.faster_factor
        for result in x[1]:
            running_avg=running_avg*(1-(self.run_factor*rfm))+(self.run_factor*rfm)*result
            #running_avg2=running_avg2*(1-self.run_factor2)+self.run_factor2*result
        inacc=1 / int(all+1) ** self.innac_factor  #faktor nenatancnosti
        unlucky=x[3]**self.unlucky_factor
        return rate*self.rate_w + inacc*self.innac_w + running_avg*self.run_w + running_avg2*self.run_w2 + last_rate*self.last_w + unlucky*self.unlucky_w


def makeTestCase():
    machines=[] #[[[zacetek obmocja,verjetnost uspesnega potega] ... naslednje obmocje] ... naslednji avtomat]
    cases=random.randint(500,3000)
    for i in range(random.randint(2,10)):
        machines.append([])
        n=random.randint(1,cases//200)
        for j in range(n):
            machines[-1].append([j*cases//n,random.random()])
    return cases,machines

def run():
    if len(sys.argv) > 1:
        a = Avtomati(sys.argv[1])
    else:
        a = Avtomati("http://celtra-jackpot.com/1")
    return a

def avg(it,key=lambda x:x):
    return  sum([key(i) for i in it])/len(it)

def test():
    global testing,testing_pulls,testing_machines
    testing=1
    ##for caseNum in range(5):
        ##testing_pulls,testing_machines=makeTestCase
    for testing_pulls,testing_machines in [
                                            #[1000,[[[0,0.9],[300,0.7]],[[0,0.8]]]],
                                            [1000,[[[0,0.3], [100,0.9]], [[0,0.7]], [[0,0.5]], [[0,0.1],[800,1]], ]],
                                            #[1000,[[[0,0.2]],[[0,0.8]],[[0,0.9]],[[0,0.15]]]],

                                            ]: #konfiguracije avtomatov
        configs=[{"run_factor":0.3,"run_factor2":0.1,"innac_factor":2,"last_len":10,"rate_w":0,"innac_w":0,"run_w":1,"run_w2":0,"last_w":0,"unlucky_factor":0.42,"unlucky_w":0.05,"faster_factor":2},
                 #{"run_factor":0.5,"run_factor2":0.2,"innac_factor":2,"last_len":10,"rate_w":0,"innac_w":1,"run_w":1,"run_w2":0,"last_w":0},
                 ]
        for n in range(0,10):  # naredimo testne konfiguracije
            configs.append({i:configs[0][i] for i in configs[0]})
            #configs[-1]["run_factor"]=0.15+n/35.0
            #configs[-1]["unlucky_w"]=0.01+n/200
            #configs[-1]["unlucky_factor"]=0.3+n/50
            #configs[-1]["faster_factor"]=1.1+n/3
        del configs[0]
        for config in configs:
            res=[]
            for i in range(100): #st poizkusov s posamezno konfiguracijo
                print i,
                a=Avtomati("http://celtra-jackpot.com/%d" %(i+1,))
                a.run_factor=config["run_factor"]
                a.run_factor2=config["run_factor2"]
                a.innac_factor=config["innac_factor"]
                a.last_len=config["last_len"]
                a.rate_w=config["rate_w"]
                a.innac_w=config["innac_w"]
                a.run_w=config["run_w"]
                a.run_w2=config["run_w2"]
                a.last_w=config["last_w"]
                a.unlucky_factor=config["unlucky_factor"]
                a.unlucky_w=config["unlucky_w"]
                a.faster_factor=config["faster_factor"]
                a.start()
                res.append(a)
            print "\n",config
            print "potegov:",avg(res,lambda a: a.maxPulls),", avtomatov:",a.nMachines
            print "uspesnih:", sum([sum(s) for n,s,v,u in sum([i.machines for i in res],[])])/len(res)
            m=[[] for i in a.machines]
            for a in res:
                for n,i in enumerate(m):
                    i.extend(a.machines[n][1])
            print "uspesnih potegov razmerje utez"
            for n,(s, machine) in enumerate(zip(m,testing_machines)):
                print "%6.1f  %6.1f   %.3f    %.3f    %s"%(sum(s)/len(res),len(s)/len(res),sum(s)/len(s) if len(s) else -1,avg([i.weight(i.machines[n]) for i in res]),str(machine)), a.machines[n]
            print "*"*50, "naslednja konfiguracija","*"*50
        print "#"*50, "naslednji primer", "#"*50


if __name__ == "__main__":
    test()



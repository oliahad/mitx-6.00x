# 6.00 Problem Set 9
from ps8b_precompiled_27 import *
import numpy
import random
import pylab
#from ps8b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    delay=[0,75,150,300]
    for d in delay:
        Tpop=[]
        steps=150+d
        for z in range(numTrials):
            final,finalR=0,0
            virus=ResistantVirus(0.1,0.05,{'guttagonol': False},0.005)
            viruses=[virus]*100
            p=TreatedPatient(viruses,1000)
            for each in range(steps):
                if each==d:
                    p.addPrescription('guttagonol')
                final=p.update()
                finalR=p.getResistPop(['guttagonol'])
            Tpop.append((final+finalR)/2)
        pylab.title('DelayedSimulation -> '+str(d))
        pylab.xlabel('Final Virus Population')
        pylab.ylabel('Number of Trials')
        pylab.hist(Tpop,bins=10)
        pylab.show()

#simulationDelayedTreatment(100)




#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    delay=[0,75,150,300]
    for d in delay:
        Tpop=[]
        steps=300+d
        for z in range(numTrials):
            final,finalR=0,0
            virus=ResistantVirus(0.1,0.05,{'guttagonol': False, 'grimpex': False},0.005)
            viruses=[virus]*100
            p=TreatedPatient(viruses,1000)
            for each in range(steps):
                if each==150:
                    p.addPrescription('guttagonol')
                if each==150+d:
                    p.addPrescription('grimpex')
                final=p.update()
                finalR=p.getResistPop(['guttagonol','grimpex'])
            Tpop.append((final+finalR)/2)
        pylab.title('DelayedSimulation -> '+str(d))
        pylab.xlabel('Final Virus Population')
        pylab.ylabel('Number of Trials')
        pylab.hist(Tpop,bins=10)
        pylab.show()
#simulationTwoDrugsDelayedTreatment(100)

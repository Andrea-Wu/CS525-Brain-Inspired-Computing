from random import random

import math

TRAIN_LOOP = 3

TIME_PER_NEURON = 100 #time is a social construct. We don't need units!
TIME_DIFF = 0.01
LOW_CURR = 2e-3
HIGH_CURR = 5e-3


ON_TRAIN = 1
OFF_TRAIN = -100

CASE1_RATE = -1
CASE3_RATE = -1

negativeWeightCtr = 0

CTR = 100

def currToRate(curr):
    m = 3124.674377412921
    b = 1.3024903596836612e-05   

    rate = (m * curr) + b
    return rate

def rateToCurr(rate):
    m = 3124.674377412921
    b = 1.3024903596836612e-05   
    curr = (rate - b) / m
    return curr

class TrainingNeuron:
    def __init__(self, student):
        self.train = []
        self.curr = 0

    def updateCurrent(self, curr):
        self.curr = curr

        #calculate a "constant" current of spikes
        rate = currToRate(curr)
        timeDiff = 1/rate

        #set the spike train
        self.train = []
        self.train.append(0)
        self.train.append(timeDiff)

    def updateCurrWithRate(self, rate):
        #calculate current
        self.curr = rateToCurr(rate)
        
        #calculate a "constant" current of spikes
        timeDiff = 1/rate

        #set the spike train
        self.train = []
        self.train.append(0)
        self.train.append(timeDiff)



class Neuron:
    def __init__(self):
        self.input = [] #this will contain objects of type "synapse"
        self.output = [] #this will contain objects of type "synapse"
        self.time = 0 #this is the neuron's internal clock, aka how all neurons synchronize themselves
        self.avgRate = 0
        self.train = []

    def runEulers(self):
        #get current- run performWeightedSum
        current = self.performWeightedSum()

        #Constants from the 1st assignment
        V_t = -0.040 #threshold voltage
        R_m = 10e6 #resistance constant
        C_m = 8e-3 #capacitance constant
        zeroed_time = 0

        while True:
            V_curr = -0.080
            while True:
                dV_dt = (current - (V_curr / R_m)) / C_m
                V_curr = V_curr + dV_dt * TIME_DIFF
                zeroed_time = zeroed_time + TIME_DIFF

                if V_curr > V_t:
                    #print("spike")
                    self.train.append(self.time + zeroed_time)
                    #this means that a spike happened
                    break 
                if zeroed_time > TIME_PER_NEURON:
                    break

            if zeroed_time > TIME_PER_NEURON:
                    break

    def calculateAvgRate(self):
        if len(self.train) > 1:
    

            self.avgRate = 1/(self.train[1] - self.train[0])
        else: 
            self.avgRate = 0

    def updateWeights(self):
        for synapse in self.input:
            if isinstance(synapse.pre, TrainingNeuron):
                continue

            #perform oja's rule
            #constants:
            L_R = 9e-6 #LEARNING_RATE

            #get avg rate of curr neuron and avg rate of prev neuron
            #TODO: switch v_i and v_j
            v_i = self.avgRate #Current (post-synaptic)
            v_j = synapse.pre.avgRate #Prev (pre-synaptic)
            
            print("pre-update " + str(synapse.weight))
            
            #run eulers on the synapse weight
            totalTime = 0
            while True:
                dw_dt =  (L_R * ((v_i * v_j) - (synapse.weight * (v_i**2)))) 
                synapse.weight += dw_dt * TIME_DIFF
                totalTime += TIME_DIFF
                if totalTime >= TIME_PER_NEURON:
                    break
        
            print("post-update " + str(synapse.weight))

    def updateNeuron(self):
        self.runEulers()
        self.calculateAvgRate()
        self.updateWeights()
        self.time += TIME_PER_NEURON
        print("avgRate: " + str(self.avgRate))


    def performWeightedSum(self):
        totalCurrent = 0
        for synapse in self.input:
    
            #LINE CORRESPONDING TO SPIKE RATE vs CURRENT EQUATION 
            #y = 3124.674377412921x + 1.3024903596836612e-05     
            #is the equation, where y = spike rate, x = current
            m = 3124.674377412921
            b = 1.3024903596836612e-05   

            if len(synapse.pre.train) > 1:
                spike_0_time =  synapse.pre.train[0]
                spike_1_time = synapse.pre.train[1]

                rate = 1/(spike_1_time - spike_0_time) 
                current = (rate - b)/m
            else:
                current = 0
            
            current = current * synapse.weight
            totalCurrent += current
        return totalCurrent




class Synapse:
    def __init__(self, pre, post):
        self.pre = pre
        self.post = post
        self.weight = random() / math.sqrt(32) 


def fullyConnect(arr1, arr2):
    for n1 in arr1:
        for n2 in arr2:
            newSynapse = Synapse(n1, n2)
            n1.output.append(newSynapse)
            n2.input.append(newSynapse)

def makeSynapsesNegative(neur):
    for syn in neur.output:
        syn.weight *= -1


def main():
    global CASE1_RATE
    global CASE3_RATE

    layer1 = []
    layer2 = []
    layer3 = []

    #I'M NOT SURE IF WEIGHTS HAVE TO INITIALLY ADD UP TO 1?

    #create 2 neurons in the 1st layer
    for i in range(2):
        layer1.append(Neuron())

    #create 8 neurons in the 2nd layer
    for i in range(8):
        layer2.append(Neuron())

    #create 2 neurons in 3rd layer
    for i in range(2):
        layer3.append(Neuron())

    #fully connect all layers of NN
    fullyConnect(layer1, layer2)
    fullyConnect(layer2, layer3)

    makeSynapsesNegative(layer2[0]) 
    makeSynapsesNegative(layer2[1])
    print("LAYER 1")
    for neuron in layer1:
        for synapse in neuron.output:
            print(synapse.weight)

    print("LAYER 2")
    for neuron in layer2:
        for synapse in neuron.output:
            print(synapse.weight)
    #attach "training neurons" to 1st and 3rd layers

    #LAYER1
    #create input neurons
    trainA = TrainingNeuron(None)
    trainB = TrainingNeuron(None)
    
    #create input synapses
    synA = Synapse(trainA, layer1[0])
    synB = Synapse(trainB, layer1[1])
    
    #set weight for input synapses: #TODO i'm just guessing values for now
    synA.weight = 1
    synB.weight = 1

    #attach synapses to postsynaptic neurons
    layer1[0].input.append(synA)
    layer1[1].input.append(synB)

            
    #LAYER3        
    #create training neurons
    trainLow = TrainingNeuron(None)
    trainHigh = TrainingNeuron(None)

    CASE1_RATE = currToRate(6.4e-5)
    CASE3_RATE = currToRate(6.4e-5)

    print("R1: " + str(CASE1_RATE))
    print("R3: " + str(CASE3_RATE))

    #create training synapses
    synLow = Synapse(trainLow, layer3[0])
    synHigh = Synapse(trainHigh, layer3[1])

    print("TESTING")
    runNet(layer1, layer2, layer3, synLow, synHigh, trainA, trainB, trainLow, trainHigh, case=3, ctr=1)

    #attach synapses to postsynaptic neurons
    layer3[0].input.append(synLow)
    layer3[1].input.append(synHigh)
    
    
    #neural net time with training neurons!
    for r in range(20):
        runNet(layer1, layer2, layer3, synLow, synHigh, trainA, trainB, trainLow,trainHigh,case=3,ctr=1)
        runNet(layer1, layer2, layer3, synLow, synHigh, trainA, trainB, trainLow,trainHigh,case=1,ctr=1)
    
    #pop the training neurons and see if the net stil works (assuming last on list)
    for neuron in layer3:
        neuron.input.pop()

    print("trained results:")
    #neural net time without training neurons!
    print("case 1")
    runNet(layer1, layer2, layer3, synLow, synHigh, trainA, trainB, trainLow, trainHigh, case=1, ctr=1)
    print("case 3")
    runNet(layer1, layer2, layer3, synLow, synHigh, trainA, trainB, trainLow, trainHigh, case=3, ctr=1)



def runNet(layer1, layer2, layer3, synLow, synHigh, trainA, trainB, trainLow, trainHigh, case, ctr):
   #TODO maybe my input weights aren't different enough? experiment

    global CASE1_RATE
    global CASE3_RATE
    
    if case == 1:
        #A = 1, B = 1
        trainA.updateCurrent(HIGH_CURR)
        trainB.updateCurrent(HIGH_CURR)
        synLow.weight = ON_TRAIN
        synHigh.weight = OFF_TRAIN
        trainHigh.updateCurrWithRate(CASE1_RATE)
        trainLow.updateCurrWithRate(CASE1_RATE)
        print("ASS: " + str(trainHigh.curr))
    elif case == 2:
        #A = 1, B = 0
        trainA.updateCurrent(HIGH_CURR)
        trainB.updateCurrent(LOW_CURR)
        synLow.weight = OFF_TRAIN
        synHigh.weight = ON_TRAIN
    elif case == 3:
        #A = 0, B = 1
        trainA.updateCurrent(LOW_CURR)
        trainB.updateCurrent(HIGH_CURR)
        synLow.weight = OFF_TRAIN
        synHigh.weight = ON_TRAIN
        trainHigh.updateCurrWithRate(CASE3_RATE)
        trainLow.updateCurrWithRate(CASE3_RATE)
        print("HOLE: " + str(trainHigh.curr))
    else:
        #A = 0, B = 0
        trainA.updateCurrent(LOW_CURR)
        trainB.updateCurrent(LOW_CURR)
        synLow.weight =  ON_TRAIN
        synHigh.weight = OFF_TRAIN

    for i in range(ctr):
        print("LAYER1")
        for n in layer1:
            #print("layer1 neuron")
            n.updateNeuron()

        print("LAYER2")
        for n in layer2:
            #print("layer2 neuron")
            n.updateNeuron()

        print("LAYER3")
        for n in layer3:
            #print("layer3 neuron")
            n.updateNeuron()

        deleteTrain(layer1)
        deleteTrain(layer2)
        deleteTrain(layer3)
    
        #update training weights
        if case == 1:
            CASE1_RATE = max(layer3[0].avgRate,layer3[1].avgRate) * 0.7
            print("CASE1_RATE: " + str(CASE1_RATE))
        elif case == 3:
            CASE3_RATE = max(layer3[0].avgRate,layer3[1].avgRate) * 0.7
            print("CASE3_RATE: " + str(CASE3_RATE))
        print("TRAIN_WEIGHT: " + str(trainHigh.curr))

    
        #update the training current

        #print("case " + str(case) + " low: " + str(layer3[0].avgRate) + " high: " + str(layer3[1].avgRate))

def deleteTrain(layer):
    for neu in layer:
        neu.train = []

if __name__ == "__main__":
    main()


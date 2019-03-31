from random import random

import math

TRAIN_LOOP = 3

TIME_PER_NEURON = 100 #time is a social construct. We don't need units!
TIME_DIFF = 0.01
LOW_CURR = 2e-3
HIGH_CURR = 5e-3




case_rates = {}

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
            L_R = 9e-7 #LEARNING_RATE

            #get avg rate of curr neuron and avg rate of prev neuron
            #TODO: switch v_i and v_j
            v_i = self.avgRate #Current (post-synaptic)
            v_j = synapse.pre.avgRate #Prev (pre-synaptic)
            
            #print("pre-update " + str(synapse.weight))
            
            #run eulers on the synapse weight
            totalTime = 0
            while True:
                dw_dt =  (L_R * ((v_i * v_j) - (synapse.weight * (v_i**2)))) 
                synapse.weight += dw_dt * TIME_DIFF
                totalTime += TIME_DIFF
                if totalTime >= TIME_PER_NEURON:
                    break
        
            #print("post-update " + str(synapse.weight))

    def updateNeuron(self):
        self.runEulers()
        self.calculateAvgRate()
        self.updateWeights()
        self.time += TIME_PER_NEURON
        print("avgRate: " + str(self.avgRate))

    def forwardProp(self): #this is like updateNeuron but without updating
        self.runEulers()
        self.calculateAvgRate()
        print("averageRate: " + str(self.avgRate))


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
        self.weight = 0.05


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
    global case_rates

    layer1 = []
    layer2 = []
    layer3 = []

    #I'M NOT SURE IF WEIGHTS HAVE TO INITIALLY ADD UP TO 1?

    #create 2 neurons in the 1st layer
    for i in range(2):
        layer1.append(Neuron())

    #create 8 neurons in the 2nd layer. 
    #layer2[0] will be the OR neuron, layer2[1] will be the NAND
    for i in range(2):
        layer2.append(Neuron())

    #create 1 neuron in 3rd layer
    for i in range(1):
        layer3.append(Neuron())

    #fully connect all layers of NN
    fullyConnect(layer1, layer2)
    fullyConnect(layer2, layer3)

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

    #LAYER2 train
    trainNAND = TrainingNeuron(None)
    trainOR = TrainingNeuron(None)
    synOR = Synapse(trainOR, layer2[0])
    synNAND = Synapse(trainNAND, layer2[1])
    synOR.weight = 1
    synNAND.weight = 1
    layer2[0].input.append(synOR)
    layer2[1].input.append(synNAND)

    #LAYER3 train
    trainAND = TrainingNeuron(None)
    synAND = Synapse(trainAND, layer3[0])
    synAND.weight = 1
    layer3[0].input.append(synAND)
    
    #neural net time with training neurons!
    runNet(layer1,layer2,layer3,trainA, trainB, trainNAND,trainOR,trainAND,case=1,ctr=400)
    runNet(layer1,layer2,layer3,trainA, trainB, trainNAND,trainOR,trainAND,case=2,ctr=400)
    runNet(layer1,layer2,layer3,trainA, trainB, trainNAND,trainOR,trainAND,case=3,ctr=400)
    runNet(layer1,layer2,layer3,trainA, trainB, trainNAND,trainOR,trainAND,case=4,ctr=400)
    #pop the training neurons and see if the net stil works (assuming last on list)
    for neuron in layer3:
        neuron.input.pop()

    print("TRAINED:")
    #neural net time without training neurons!
    print("C1")
    runNetStatic(layer1, layer2, layer3, trainA,trainB,trainNAND,trainOR,trainAND,case=1,ctr=1)
    print("C2")
    runNetStatic(layer1, layer2, layer3, trainA,trainB,trainNAND,trainOR,trainAND,case=2,ctr=1)
    print("C3")
    runNetStatic(layer1, layer2, layer3, trainA,trainB,trainNAND,trainOR,trainAND,case=3,ctr=1)
    print("C4")
    runNetStatic(layer1, layer2, layer3, trainA,trainB,trainNAND,trainOR,trainAND,case=4,ctr=1)

def runNet(layer1, layer2, layer3, trainA, trainB, trainNAND, trainOR, trainAND, case, ctr):
   #TODO maybe my input weights aren't different enough? experiment

    global case_rates
    
    if case == 1:
        #A = 1, B = 1
        trainA.updateCurrent(HIGH_CURR)
        trainB.updateCurrent(HIGH_CURR)
        trainNAND.updateCurrent(LOW_CURR) 
        trainOR.updateCurrent(HIGH_CURR)
        trainAND.updateCurrent(LOW_CURR)
    elif case == 2:
        #A = 1, B = 0
        trainA.updateCurrent(HIGH_CURR)
        trainB.updateCurrent(LOW_CURR)
        trainNAND.updateCurrent(HIGH_CURR) 
        trainOR.updateCurrent(HIGH_CURR)
        trainAND.updateCurrent(HIGH_CURR)
    elif case == 3:
        #A = 0, B = 1
        trainA.updateCurrent(LOW_CURR)
        trainB.updateCurrent(HIGH_CURR)
        trainNAND.updateCurrent(HIGH_CURR) 
        trainOR.updateCurrent(HIGH_CURR)
        trainAND.updateCurrent(HIGH_CURR)
    else:
        #A = 0, B = 0
        trainA.updateCurrent(LOW_CURR)
        trainB.updateCurrent(LOW_CURR)
        trainNAND.updateCurrent(HIGH_CURR) 
        trainOR.updateCurrent(LOW_CURR)
        trainAND.updateCurrent(LOW_CURR)
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
        #update the training current

        #print("case " + str(case) + " low: " + str(layer3[0].avgRate) + " high: " + str(layer3[1].avgRate))

def runNetStatic(layer1, layer2, layer3, trainA, trainB, trainNAND, trainOR, trainAND, case, ctr):
   #TODO maybe my input weights aren't different enough? experiment

    global case_rates
    
    if case == 1:
        #A = 1, B = 1
        trainA.updateCurrent(HIGH_CURR)
        trainB.updateCurrent(HIGH_CURR)
        trainNAND.updateCurrent(LOW_CURR) 
        trainOR.updateCurrent(HIGH_CURR)
        trainAND.updateCurrent(LOW_CURR)
    elif case == 2:
        #A = 1, B = 0
        trainA.updateCurrent(HIGH_CURR)
        trainB.updateCurrent(LOW_CURR)
        trainNAND.updateCurrent(HIGH_CURR) 
        trainOR.updateCurrent(HIGH_CURR)
        trainAND.updateCurrent(HIGH_CURR)
    elif case == 3:
        #A = 0, B = 1
        trainA.updateCurrent(LOW_CURR)
        trainB.updateCurrent(HIGH_CURR)
        trainNAND.updateCurrent(HIGH_CURR) 
        trainOR.updateCurrent(HIGH_CURR)
        trainAND.updateCurrent(HIGH_CURR)
    else:
        #A = 0, B = 0
        trainA.updateCurrent(LOW_CURR)
        trainB.updateCurrent(LOW_CURR)
        trainNAND.updateCurrent(HIGH_CURR) 
        trainOR.updateCurrent(LOW_CURR)
        trainAND.updateCurrent(LOW_CURR)
    for i in range(ctr):
        print("LAYER1")
        for n in layer1:
            #print("layer1 neuron")
            n.forwardProp()

        print("LAYER2")
        for n in layer2:
            #print("layer2 neuron")
            n.forwardProp()

        print("LAYER3")
        for n in layer3:
            #print("layer3 neuron")
            n.forwardProp()

        deleteTrain(layer1)
        deleteTrain(layer2)
        deleteTrain(layer3)

def deleteTrain(layer):
    for neu in layer:
        neu.train = []

if __name__ == "__main__":
    main()


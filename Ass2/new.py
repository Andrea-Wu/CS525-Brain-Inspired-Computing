class Neuron:
    def __init__(self):
        self.input = [] #this will contain objects of type "synapse"
        self.output = [] #this will contain objects of type "synapse"
        self.time = 0 #this is the neuron's internal clock, aka how all neurons synchronize themselves
    
    def runEulers(self):
        #get current- run performWeightedSum

    def performWeightedSum(self):
        totalCurrent = 0
        for synapse in self.input:
    
            #LINE CORRESPONDING TO SPIKE RATE vs CURRENT EQUATION 
            #y = 3124.674377412921x + 1.3024903596836612e-05     
            #is the equation, where y = spike rate, x = current
            m = 3124.674377412921
            b = 1.3024903596836612e-05   

            spike_0_time =  synapse.train[0]
            spike_1_time = synapse.train[1]

            rate = 1/(spike_1_time - spike_0_time) #i'm not actually sure this is right
            current = (rate - b)/m
            
            current = current * synapse.weight
            totalCurrent += current
        return totalCurrent




class Synapse:
    def __init__(self, pre, post, weight):
        self.pre = pre
        self.post = post
        self.weight = weight
        self.train = [] #this will store a list of timestamps that correspond with a spike
        

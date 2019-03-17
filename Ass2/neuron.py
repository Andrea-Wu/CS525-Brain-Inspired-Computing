class neuron:
    """
    needs:
        array of forward connected neuron objects (synapse)
        separate array of backward connected neurons
            -corresponding connection values for each connected neuron

        

        a "stabilizer?" that keeps the neuron's spike active for a while (because they're not all going to spike at exactly the same time)
        -or rather, each neuron keeps an internal clock. We can hack it so that it seems like the computations are acting in parallel, but they're actually not. 

    
        threshold for spike
        spike must propagate forward to connected neurons
        
        every time a neuron fires, it's backwards neurons are checked to see if they fire too

    """
    def __init__(self):





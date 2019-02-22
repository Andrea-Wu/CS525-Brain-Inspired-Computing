import matplotlib.pyplot as plt

def eulers():
    #perform euler's method on the equation
    #this is my first time coding an equation. wtf
    #after every loop, store the data point
    #we need a threshold. 

    V_t = 1 #threshold voltage
    CURRENT = 0.1
    R_m = 1 #resistance constant
    C_m = 1 #capacitance constant
    TIME_DIFF = 0.2
    time = 0

    plotX = []
    plotY = []

    numSpikes = 0
    while num_spikes < 10:
        V_curr = 0
        while True:

            plotY.append(V_curr)
            plotX.append(time)
            dV_dt = (CURRENT - ( V_curr / R_m)) / C_m
            V_curr = V_curr + dV/dt * TIME_DIFF
            time = time+ TIME_DIFF

            if V_curr > V_t:
                break 
        numSpikes+=1

    plt.plot(plotX, plotY)

if __name__ == "__main__":
    eulers()

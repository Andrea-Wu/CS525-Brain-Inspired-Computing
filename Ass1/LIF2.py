import matplotlib.pyplot as plt

def eulers():
    #perform euler's method on the equation
    #this is my first time coding an equation. wtf
    #after every loop, store the data point
    #we need a threshold. 

    V_t = -0.040 #threshold voltage #-0.055
    CURRENT = 1e-5
    R_m = 10e6 #resistance constant
    C_m = 8e-3 #capacitance constant
    TIME_DIFF = 0.01
    time = 0

    plotX = []
    plotY = []

    timeStamp = []
    timeStamp.append(0)

    numSpikes = 0
    CAP = 30

    marker1 = True
    marker2 = True
    while numSpikes < CAP:
        print(numSpikes)

        if numSpikes >= CAP/3 and numSpikes < (2*CAP)/3: 
            if marker1:
                marker1 = False
                timeStamp.append(time)
            print("WHAT")
            CURRENT = 2e-5
        elif numSpikes >= (2*CAP)/3:
            if marker2:
                marker2 = False
                timeStamp.append(time)
            print("WOOOO")
            CURRENT = 5e-3


        V_curr = -0.080
        while True:
            plotY.append(V_curr)
            plotX.append(time)
            dV_dt = (CURRENT - ( V_curr / R_m)) / C_m
            V_curr = V_curr + dV_dt * TIME_DIFF
            time = time+ TIME_DIFF

            if V_curr > V_t:
                break 
        numSpikes+=1
        print("spiked")

    timeStamp.append(time)
    
    #calculate rates:
    diff1 = timeStamp[1] - timeStamp[0]
    diff2 = timeStamp[2] - timeStamp[1]
    diff3 = timeStamp[3] - timeStamp[2]

    rates = []
    rates.append(10/diff1)
    rates.append(10/diff2)
    rates.append(10/diff3)

    xValCurr = [1e-5, 2e-5, 5e-3]

    #plt.plot(plotX, plotY)
    plt.plot(xValCurr, rates)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.show()

if __name__ == "__main__":
    eulers()

import matplotlib.pyplot as plt

def eulers():
    #perform euler's method on the equation
    #this is my first time coding an equation. wtf
    #after every loop, store the data point
    #we need a threshold. 

    V_t = 1 #threshold voltage
    CURRENT = 2
    R_m = 1 #resistance constant
    C_m = 1 #capacitance constant
    TIME_DIFF = 0.2
    time = 0

    plotX = []
    plotY = []

    numSpikes = 0
    while numSpikes < 10:
        print("loooop")
        V_curr = 0
        while True:
            print(V_curr)
            plotY.append(V_curr)
            plotX.append(time)
            dV_dt = (CURRENT - ( V_curr / R_m)) / C_m
            print(dV_dt)
            V_curr = V_curr + dV_dt * TIME_DIFF
            time = time+ TIME_DIFF

            if V_curr > V_t:
                break 
        numSpikes+=1

    plt.plot(plotX, plotY)
    plt.show()

if __name__ == "__main__":
    eulers()

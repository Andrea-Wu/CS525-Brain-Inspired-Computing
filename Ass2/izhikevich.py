import matplotlib.pyplot as plt

def eulers():
    #perform euler's method on the equation
    #this is my first time coding an equation. wtf
    #after every loop, store the data point
    #we need a threshold. 

    V_t = 30 #threshold voltage- 30mV = 0.03V
    CURRENT = 5
    TIME_DIFF = 0.01
    time = 0

    a = 0.02 #smaller values = slower recovery
    b= 0.2 #sensitivity of recovery variable to fluctuations of membrane potential
    c = -65 #after-spike reset of membrane potential
    d = 2 #after-spike increase of u

    plotX = []
    plotY = []

    numSpikes = 0
    u = 0 #for scoping
    while numSpikes < 6:

        """
        if numSpikes > 1:
            CURRENT = 5.8e-2
        elif numSpikes > 3:
            CURRENT = 6.5e-2
        """
    
        V_curr = c #-65 mV
        if numSpikes == 0:
            u = b * V_curr #initial value is apparently b * v 
        else:
            u = u + d #u <- u + d

        while True:
            print("loopz")
            plotY.append(V_curr)
            plotX.append(time)

            du_dt = a * ((b * V_curr) -u) 
            dV_dt = ((0.04 * (V_curr**2)) + (5 * V_curr) + 140 - u + CURRENT)
            print("dV_dt is " + str(dV_dt))
            print("u is " + str(u))
            print("old V_curr: " +str(V_curr))
            V_curr = V_curr + dV_dt * TIME_DIFF
            print("new V_curr: " + str(V_curr))
            u = u + du_dt * TIME_DIFF
            time = time+ TIME_DIFF
            if V_curr > V_t:
                print("V_curr is: " + str(V_curr))
                print("V_t is: " + str(V_t))
                break 
        numSpikes+=1
        print("spiked")

    plt.plot(plotX, plotY)
    plt.show()
    print("wtf")

if __name__ == "__main__":
    eulers()

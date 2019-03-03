import matplotlib.pyplot as plt
import math

def eulers():
    #perform euler's method on the equation
    #this is my first time coding an equation. wtf
    #after every loop, store the data point
    #we need a threshold. 

    V_t = 100 #threshold voltage #-0.055
    CURRENT = 3e-1
    TIME_DIFF = 0.0001
    time = 0

    #CONSTANTS!!
    alpha_n = lambda v: ((0.01 * (v + 50)))/(1 - math.exp((-1 * (v+50))/10))
    beta_n = lambda v: 0.125 * math.exp((-1 * (v + 60))/80)
    alpha_m = lambda v: (0.1 *(v + 35))/(1 - math.exp((-1 * (v+35))/10))
    beta_m = lambda v: 4.0 * math.exp(-0.0556 * (v + 60))
    alpha_h = lambda v: 0.07 * math.exp(-0.05 * (v + 60))
    beta_h = lambda v: 1 / (1 + math.exp(-0.1 * (v + 30)))

    C_m = 0.01
    E_Na = 55.17
    E_K = -72.14
    E_I = -49.42
    g_Na = 1.2
    g_K = 0.36 
    g_I = 0.003

    plotX = []
    plotY = []

    numSpikes = 0
    while numSpikes < 1:
        V_curr = -65
        n = 0.05 #placeholder 0
        m = 0.33 #placecholder 0
        h = 0.59 #placeholder 0

        loopz = 0
        while True:
            plotY.append(V_curr)
            plotX.append(time)

            dn_dt = alpha_n(V_curr)*(1 - n) - beta_n(V_curr)*n
            dm_dt = alpha_m(V_curr)*(1 - m) - beta_m(V_curr)*m 
            dh_dt = alpha_h(V_curr)*(1 - h) - beta_h(V_curr)*h
            dv_dt = (1 / C_m)* (CURRENT - (g_Na * (m**3) * h * (V_curr - E_Na)) - (g_K * (n**4) * (V_curr - E_K)) - (g_I * (V_curr - E_I)))

            n = n + dn_dt * TIME_DIFF
            m = m + dm_dt * TIME_DIFF
            h = h + dh_dt * TIME_DIFF
            V_curr = V_curr + dv_dt * TIME_DIFF

            time = time+ TIME_DIFF

            #if V_curr > V_t:
            #    break 
            loopz +=1 
            if loopz > 500000:
                break
        numSpikes+=1
        print("spiked")

    plt.plot(plotX, plotY)
    plt.show()

if __name__ == "__main__":
    eulers()
